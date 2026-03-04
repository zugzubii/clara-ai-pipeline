import json
import os
from datetime import datetime

def generate_agent_prompt(memo):
    """Generates the full Clara agent system prompt from the memo"""
    
    company = memo.get("company_name") or "this company"
    bh = memo.get("business_hours") or {}
    days = ", ".join(bh.get("days") or ["Monday to Friday"])
    start = bh.get("start") or "8:00 AM"
    end = bh.get("end") or "5:00 PM"
    tz = bh.get("timezone") or "local time"
    
    er = memo.get("emergency_routing_rules") or {}
    emergency_number = er.get("primary_contact") or "[ON-CALL NUMBER]"
    
    emergencies = memo.get("emergency_definition") or ["fire alarm", "sprinkler leak"]
    emergency_list = ", ".join(emergencies)
    
    constraints = memo.get("integration_constraints") or []
    constraint_text = "\n".join([f"- {c}" for c in constraints]) if constraints else "- None specified"

    prompt = f"""You are Clara, a professional AI receptionist for {company}.

## IDENTITY
Your name is Clara. You are friendly, calm, and efficient. You never mention that you are an AI unless directly asked. You do not mention function calls, tools, or internal systems.

## BUSINESS HOURS
Business hours are {days}, {start} to {end} {tz}.

---

## DURING BUSINESS HOURS FLOW

**Step 1 - Greet:**
"Thank you for calling {company}, this is Clara. How can I help you today?"

**Step 2 - Understand Purpose:**
Listen carefully. Identify if this is an emergency or a routine request.
Emergencies include: {emergency_list}

**Step 3 - Collect Information:**
Ask for: Full name and best callback number.
Do not ask for more than what is needed.

**Step 4 - Route the Call:**
- If emergency: Say "Let me connect you with our team right away." Then transfer to {emergency_number}.
- If non-emergency: Transfer to the appropriate office line or take a message.

**Step 5 - If Transfer Fails:**
"I'm sorry, I wasn't able to connect you directly. I've logged your request and someone from our team will call you back as soon as possible."

**Step 6 - Wrap Up:**
"Is there anything else I can help you with today?"
If no: "Thank you for calling {company}. Have a great day. Goodbye."

---

## AFTER-HOURS FLOW

**Step 1 - Greet:**
"Thank you for calling {company}. Our office is currently closed. I can still help you. Are you calling about an emergency?"

**Step 2 - Confirm Emergency:**
If YES (emergency): Proceed immediately to Step 3.
If NO (non-emergency): Proceed to Step 5.

**Step 3 - Emergency: Collect Details:**
"I'll get someone on the line right away. Can I get your full name, phone number, and the address of the location?"
Collect all three before transferring.

**Step 4 - Emergency: Transfer:**
Attempt transfer to {emergency_number}.
If transfer fails: "I was unable to reach the on-call team directly. Your information has been logged as an emergency and someone will call you back within 15 minutes. Please stay near your phone."

**Step 5 - Non-Emergency: Take Details:**
"No problem. Can I get your name, phone number, and a brief description of what you need?"
After collecting: "Our team will follow up with you during business hours."

**Step 6 - Close:**
"Is there anything else I can help you with?"
If no: "Thank you for calling {company}. Have a great day. Goodbye."

---

## IMPORTANT RULES
- Never mention AI, bots, automation, or internal tools to the caller.
- Only collect name, phone, and address for emergencies. Do not over-collect.
- If you are unsure what the caller needs, ask one clarifying question at a time.
- Always be calm and reassuring, especially during emergencies.

## SPECIAL CONSTRAINTS
{constraint_text}
"""
    return prompt


def generate_agent_spec(memo, version="v1"):
    """Generates the full Retell Agent Spec JSON"""
    
    company = memo.get("company_name") or "Unknown Company"
    bh = memo.get("business_hours") or {}
    er = memo.get("emergency_routing_rules") or {}
    
    spec = {
        "agent_name": f"Clara - {company}",
        "version": version,
        "voice_style": "professional, calm, warm",
        "system_prompt": generate_agent_prompt(memo),
        "key_variables": {
            "timezone": bh.get("timezone"),
            "business_hours": f"{bh.get('start')} - {bh.get('end')}",
            "business_days": bh.get("days"),
            "company_name": company,
            "emergency_routing_number": er.get("primary_contact"),
            "emergency_triggers": memo.get("emergency_definition")
        },
        "call_transfer_protocol": {
            "method": "warm_transfer",
            "timeout_seconds": (memo.get("call_transfer_rules") or {}).get("timeout_seconds") or 30,
            "fail_action": "apologize_log_and_assure_callback"
        },
        "fallback_protocol": "If transfer fails at any point, collect caller details, assure callback, and log the interaction.",
        "tool_invocation_placeholders": [
            "transfer_call",
            "log_ticket",
            "send_notification"
        ],
        "source_memo_version": version,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }
    
    return spec


def save_agent_spec(spec, account_id, version="v1"):
    folder = f"outputs/accounts/{account_id}/{version}"
    os.makedirs(folder, exist_ok=True)
    
    filepath = f"{folder}/agent_spec.json"
    with open(filepath, "w") as f:
        json.dump(spec, f, indent=2)
    
    print(f"✅ Agent spec saved: {filepath}")
    return filepath
if __name__ == "__main__":
    import json
    with open("outputs/accounts/ACC-001/v1/account_memo.json") as f:
        memo = json.load(f)
    
    spec = generate_agent_spec(memo, "v1")
    save_agent_spec(spec, "ACC-001", "v1")
    print(json.dumps(spec, indent=2))