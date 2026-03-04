import os

mock_demos = {
    "ACC-002": """
Demo Call Transcript - Greenfield HVAC Services

Rep: Thanks for joining today. Can you tell me about your business?
Client: Sure, we're Greenfield HVAC Services based in Austin, Texas. We do heating and cooling installs, repairs, and maintenance.
Rep: What are your business hours?
Client: Monday through Friday, 7am to 6pm Central Time.
Rep: What counts as an emergency for you?
Client: If a furnace goes out in winter, AC failure in summer for vulnerable people, or a gas leak. Those are immediate.
Rep: Who handles emergency calls after hours?
Client: Our on-call tech. His number is 512-334-7890.
Rep: What about non-emergency after hours?
Client: They leave a message, we call back next business day.
Rep: Any systems we need to integrate with?
Client: We use ServiceTitan for job management.
Rep: Great. Office address?
Client: 4821 Burnet Road, Austin TX 78756.
""",

    "ACC-003": """
Demo Call Transcript - Riverside Fire Protection

Rep: Tell me about Riverside Fire Protection.
Client: We handle fire suppression systems, sprinkler installs, and annual inspections in the Seattle area.
Rep: Business hours?
Client: Monday to Friday, 8am to 5pm Pacific Time. Sometimes Saturday mornings but not always.
Rep: What's an emergency for you?
Client: Active sprinkler discharge, fire alarm going off, or a suppression system failure at a facility.
Rep: After-hours emergency routing?
Client: Call goes to our dispatch line at 206-881-2200. If no answer, page the on-call technician.
Rep: Any integration constraints?
Client: We use ServiceTrade. Never create sprinkler jobs automatically — those need manual review.
Rep: Address?
Client: 1150 Harbor Ave SW, Seattle WA 98126.
""",

    "ACC-004": """
Demo Call Transcript - Pinnacle Electrical Contractors

Rep: Great to meet you. Tell me about your company.
Client: We're Pinnacle Electrical, based in Phoenix Arizona. Commercial and residential electrical work.
Rep: Hours of operation?
Client: Seven days a week actually. 7am to 7pm Mountain Time on weekdays, 8am to 4pm on weekends.
Rep: Emergencies?
Client: Power outages affecting a whole building, electrical fires, exposed live wiring. Those are critical.
Rep: Emergency contact?
Client: Our operations manager Sarah. Number is 480-223-5567.
Rep: Non-emergency after hours?
Client: Voicemail only, we return calls next morning.
Rep: Integrations?
Client: Nothing specific yet. We're evaluating options.
Rep: Office address?
Client: 9302 E Camelback Rd, Scottsdale AZ 85251.
""",

    "ACC-005": """
Demo Call Transcript - BlueSky Plumbing and Drain

Rep: Thanks for the call today. Tell me about BlueSky.
Client: We're a plumbing company out of Denver Colorado. Residential mostly, some light commercial.
Rep: What are your hours?
Client: Monday through Saturday, 8am to 6pm Mountain Time.
Rep: What qualifies as an emergency?
Client: Burst pipes, sewage backup, no hot water for elderly or families with infants, major leaks.
Rep: Who takes emergency calls overnight?
Client: We have a rotating on-call plumber. The dispatch number is 720-445-3310.
Rep: Any systems you use?
Client: Just QuickBooks for invoicing. Nothing fancy.
Rep: Address?
Client: 2240 Blake Street, Denver CO 80205.
"""
}

mock_onboardings = {
    "ACC-002": """
Onboarding Call Transcript - Greenfield HVAC Services

Rep: Let's lock in the final configuration. Confirming hours are 7am to 6pm Monday to Friday Central?
Client: Actually make it 7:30am. We don't start answering until then.
Rep: Got it. Emergency definition — furnace failure, AC failure for vulnerable, gas leak?
Client: Add flooding from HVAC unit to that list too.
Rep: Emergency number still 512-334-7890?
Client: Yes but add a fallback — if no answer in 45 seconds, try 512-334-7891.
Rep: Transfer timeout?
Client: 45 seconds, then apologize and log it.
Rep: ServiceTitan — any constraints?
Client: Do not auto-create jobs. Always flag for dispatcher review first.
Rep: After hours non-emergency?
Client: Collect name, number, issue description. We will follow up within 2 hours next business day.
""",

    "ACC-003": """
Onboarding Call Transcript - Riverside Fire Protection

Rep: Confirming Seattle location, Monday to Friday 8 to 5 Pacific?
Client: Correct. Add that we're closed on all federal holidays.
Rep: Emergency routing — dispatch at 206-881-2200, fallback page on-call tech?
Client: Yes. Also, for active sprinkler discharge specifically, always collect the facility address before transferring.
Rep: ServiceTrade constraint — no auto sprinkler jobs?
Client: Correct. Also, never create inspection jobs automatically either. Both need manual review.
Rep: Transfer timeout?
Client: 30 seconds. If it fails, tell the caller we've paged the on-call team and they'll respond within 10 minutes.
Rep: Anything else?
Client: If a caller mentions the words 'chemical suppression' or 'clean agent' route directly to senior tech line at 206-992-4400.
""",

    "ACC-004": """
Onboarding Call Transcript - Pinnacle Electrical Contractors

Rep: Confirming 7 days a week — weekdays 7am to 7pm, weekends 8am to 4pm Mountain?
Client: Yes that's right.
Rep: Emergency contact Sarah at 480-223-5567?
Client: Updated actually — Sarah left. New contact is Marcus at 480-223-6001.
Rep: Same emergency types — outages, electrical fires, live wiring?
Client: Add generator failure for commercial clients to that list.
Rep: Transfer timeout?
Client: 60 seconds. Then take a message and assure callback within 30 minutes.
Rep: Any integrations finalized?
Client: We decided on ServiceTitan. Do not create electrical panel jobs automatically, needs review.
""",

    "ACC-005": """
Onboarding Call Transcript - BlueSky Plumbing and Drain

Rep: Confirming Monday to Saturday, 8am to 6pm Mountain?
Client: Change Saturday to 9am to 2pm only.
Rep: Emergency types confirmed — burst pipes, sewage backup, no hot water for vulnerable, major leaks?
Client: Yes and add gas smell near water heater as emergency too.
Rep: On-call dispatch at 720-445-3310?
Client: Still correct.
Rep: Transfer timeout?
Client: 40 seconds. If fail, log it and tell them someone will call back within 20 minutes.
Rep: QuickBooks — any constraints for the pipeline?
Client: No auto invoice creation. That's manual only.
"""
}

# Save all files to data/
os.makedirs("data", exist_ok=True)

for acc_id, transcript in mock_demos.items():
    with open(f"data/demo_{acc_id}.txt", "w", encoding="utf-8") as f:
        f.write(transcript.strip())
    print(f"✅ Created demo_{acc_id}.txt")

for acc_id, transcript in mock_onboardings.items():
    with open(f"data/onboarding_{acc_id}.txt", "w", encoding="utf-8") as f:
        f.write(transcript.strip())
    print(f"✅ Created onboarding_{acc_id}.txt")

print("\n✅ All mock data created in /data folder!")
