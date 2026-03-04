import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extract import extract_from_transcript
from generate_agent import generate_agent_spec, save_agent_spec

DATA_DIR = "data"

SKIP_ACCOUNTS = []  # All accounts need onboarding update

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def compute_changelog(v1, v2, account_id):
    changes = []
    for key in v2:
        if key in ["version", "updated_at", "account_id"]:
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

def run_pipeline_b():
    print("\n🚀 PIPELINE B — Processing all onboarding transcripts...\n")

    all_files = os.listdir(DATA_DIR)
    onboarding_files = sorted([f for f in all_files if "onboarding" in f.lower() and f.endswith(".txt")])

    success = 0
    failed = 0

    for filename in onboarding_files:
        acc_id = filename.replace("onboarding_", "").replace(".txt", "")

        if acc_id in SKIP_ACCOUNTS:
            print(f"⏭️  Skipping {acc_id}\n")
            continue

        print(f"📄 Processing {filename} → {acc_id}")

        # Check v1 exists
        v1_path = f"outputs/accounts/{acc_id}/v1/account_memo.json"
        if not os.path.exists(v1_path):
            print(f"  ❌ No v1 memo found for {acc_id}, skipping\n")
            failed += 1
            continue

        v1_memo = load_json(v1_path)

        # Read onboarding transcript
        with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
            transcript = f.read()

        # Extract updates from onboarding transcript
        updates = extract_from_transcript(transcript, acc_id)

        if not updates:
            print(f"  ❌ Extraction failed for {acc_id}\n")
            failed += 1
            continue

        # Merge v1 + updates into v2
        v2_memo = {**v1_memo, **updates}
        v2_memo["account_id"] = acc_id
        v2_memo["version"] = "v2"
        v2_memo["updated_at"] = datetime.utcnow().isoformat() + "Z"

        # Save v2 memo
        v2_folder = f"outputs/accounts/{acc_id}/v2"
        os.makedirs(v2_folder, exist_ok=True)

        with open(f"{v2_folder}/account_memo.json", "w") as f:
            json.dump(v2_memo, f, indent=2)
        print(f"  ✅ Saved: {v2_folder}/account_memo.json")

        # Generate and save changelog
        changelog = compute_changelog(v1_memo, v2_memo, acc_id)
        with open(f"{v2_folder}/changelog.json", "w") as f:
            json.dump(changelog, f, indent=2)
        print(f"  ✅ Saved: {v2_folder}/changelog.json ({changelog['total_changes']} changes)")

        # Generate and save v2 agent spec
        v2_spec = generate_agent_spec(v2_memo, "v2")
        save_agent_spec(v2_spec, acc_id, "v2")

        print(f"  ✅ {acc_id} — v2 complete\n")
        success += 1

    print(f"✅ Pipeline B complete! {success} succeeded, {failed} failed.")
    print("📁 Check outputs/accounts/<id>/v2/ for results.\n")

if __name__ == "__main__":
    run_pipeline_b()
