import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load your prompt template
with open("prompts/extract_demo.txt", "r") as f:
    prompt_template = f.read()

def extract_from_transcript(transcript_text, account_id):
    """Takes a transcript and returns structured JSON"""
    
    prompt = prompt_template.replace("{{transcript}}", transcript_text)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1  # Low = more consistent output
    )
    
    raw_output = response.choices[0].message.content
    
    # Clean up the output (remove markdown code blocks if present)
    cleaned = raw_output.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()
    
    try:
        data = json.loads(cleaned)
        data["account_id"] = account_id
        data["version"] = "v1"
        return data
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error for {account_id}: {e}")
        return None

def save_to_file(data, account_id, version="v1"):
    """Saves the extracted data to the outputs folder"""
    folder = f"outputs/accounts/{account_id}/{version}"
    os.makedirs(folder, exist_ok=True)
    
    filepath = f"{folder}/account_memo.json"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved: {filepath}")
    return filepath

if __name__ == "__main__":
    # Test with a single file
    with open("data/demo_ACC-001.txt", "r") as f:
        transcript = f.read()
    
    result = extract_from_transcript(transcript, "ACC-001")
    if result:
        save_to_file(result, "ACC-001", "v1")
        print(json.dumps(result, indent=2))
