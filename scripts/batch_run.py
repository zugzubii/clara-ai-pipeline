import os
import json
from extract import extract_from_transcript, save_to_file
from generate_agent import generate_agent_spec, save_agent_spec
from update_v2 import update_account

DATA_DIR = "data"

def run_pipeline_a():
    """Process all demo transcripts"""
    print("\n🚀 PIPELINE A — Processing demo transcripts...\n")
    
    demo_files = sorted([f for f in os.listdir(DATA_DIR) if "demo" in f.lower()])
    
    for i, filename in enumerate(demo_files):
        account_id = f"ACC-{str(i+1).zfill(3)}"
        filepath = os.path.join(DATA_DIR, filename)
        
        print(f"Processing {filename} → {account_id}")
        
        with open(filepath, "r", encoding="utf-8") as f:
            transcript = f.read()
        
        memo = extract_from_transcript(transcript, account_id)
        if memo:
            save_to_file(memo, account_id, "v1")
            spec = generate_agent_spec(memo, "v1")
            save_agent_spec(spec, account_id, "v1")
        else:
            print(f"⚠️ Skipping {account_id} due to extraction error")
    
    print("\n✅ Pipeline A complete!\n")

def run_pipeline_b():
    """Process all onboarding transcripts"""
    print("\n🚀 PIPELINE B — Processing onboarding transcripts...\n")
    
    onboarding_files = sorted([f for f in os.listdir(DATA_DIR) if "onboarding" in f.lower()])
    
    for i, filename in enumerate(onboarding_files):
        account_id = f"ACC-{str(i+1).zfill(3)}"
        filepath = os.path.join(DATA_DIR, filename)
        
        print(f"Processing {filename} → {account_id}")
        
        with open(filepath, "r", encoding="utf-8") as f:
            transcript = f.read()
        
        update_account(account_id, transcript)
    
    print("\n✅ Pipeline B complete!\n")

if __name__ == "__main__":
    run_pipeline_a()
    run_pipeline_b()
    print("🎉 All done! Check outputs/accounts/ for results.")