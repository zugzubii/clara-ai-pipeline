import json
import os
from datetime import datetime
from generate_agent import generate_agent_spec, save_agent_spec

def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)

def compute_changelog(v1, v2, account_id):
    """Compare v1 and v2 and log what changed"""
    changes = []
    
    for key in v2:
        if key in ["version", "updated_at"]:
            continue
        if v1.get(key) != v2.get(key):
            changes.append({
                "field": key,
                "old_value": v1.get(key),
                "new_value": v2.get(key),
                "reason": "Updated from onboarding call"
            })
    
    return {
        "account_id": account_id,
        "changed_at": datetime.utcnow().isoformat() + "Z",
        "from_version": "v1",
        "to_version": "v2",
        "total_changes": len(changes),
        "changes": changes
    }

def update_account(account_id, onboarding_transcript):
    """Main function: loads v1, extracts updates, saves v2"""
    
    from extract import extract_from_transcript
    
    # Load existing v1
    v1_path = f"outputs/accounts/{account_id}/v1/account_memo.json"
    if not os.path.exists(v1_path):
        print(f"❌ No v1 found for {account_id}")
        return
    
    v1_memo = load_json(v1_path)
    
    # Extract updates from onboarding transcript
    # Use a special onboarding prompt
    with open("prompts/extract_onboarding.txt") as f:
        onboarding_template = f.read()
    
    from groq import Groq
    from dotenv import load_dotenv
    load_dotenv()
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = onboarding_template\
        .replace("{{transcript}}", onboarding_transcript)\
        .replace("{{v1_memo}}", json.dumps(v1_memo, indent=2))
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```json"): raw = raw[7:]
    if raw.startswith("```"): raw = raw[3:]
    if raw.endswith("```"): raw = raw[:-3]
    raw = raw.strip()
    
    updates = json.loads(raw)
    
    # Merge: v1 base + onboarding updates
    v2_memo = {**v1_memo, **updates}
    v2_memo["version"] = "v2"
    v2_memo["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    # Save v2 memo
    v2_folder = f"outputs/accounts/{account_id}/v2"
    os.makedirs(v2_folder, exist_ok=True)
    with open(f"{v2_folder}/account_memo.json", "w") as f:
        json.dump(v2_memo, f, indent=2)
    
    # Generate and save changelog
    changelog = compute_changelog(v1_memo, v2_memo, account_id)
    with open(f"{v2_folder}/changelog.json", "w") as f:
        json.dump(changelog, f, indent=2)
    
    # Generate v2 agent spec
    v2_spec = generate_agent_spec(v2_memo, version="v2")
    save_agent_spec(v2_spec, account_id, version="v2")
    
    print(f"✅ v2 complete for {account_id} — {changelog['total_changes']} changes made")
    return v2_memo

