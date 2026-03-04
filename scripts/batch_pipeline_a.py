import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extract import extract_from_transcript, save_to_file
from generate_agent import generate_agent_spec, save_agent_spec

DATA_DIR = "data"

# These accounts are already processed, skip them
SKIP_ACCOUNTS = ["ACC-001"]

def run_pipeline_a():
    print("\n🚀 PIPELINE A — Processing all demo transcripts...\n")
    
    all_files = os.listdir(DATA_DIR)
    demo_files = sorted([f for f in all_files if "demo" in f.lower() and f.endswith(".txt")])
    
    success = 0
    failed = 0
    skipped = 0
    
    for filename in demo_files:
        acc_id = filename.replace("demo_", "").replace(".txt", "")
        
        if acc_id in SKIP_ACCOUNTS:
            print(f"⏭️  Skipping {acc_id} — already processed\n")
            skipped += 1
            continue
        
        filepath = os.path.join(DATA_DIR, filename)
        print(f"📄 Processing {filename} → {acc_id}")
        
        with open(filepath, "r", encoding="utf-8") as f:
            transcript = f.read()
        
        memo = extract_from_transcript(transcript, acc_id)
        
        if memo:
            save_to_file(memo, acc_id, "v1")
            spec = generate_agent_spec(memo, "v1")
            save_agent_spec(spec, acc_id, "v1")
            print(f"  ✅ {acc_id} — memo + agent spec saved\n")
            success += 1
        else:
            print(f"  ❌ {acc_id} — extraction failed, skipping\n")
            failed += 1
    
    print(f"✅ Pipeline A complete! {success} succeeded, {skipped} skipped, {failed} failed.")
    print("📁 Check outputs/accounts/ for results.\n")

if __name__ == "__main__":
    run_pipeline_a()
