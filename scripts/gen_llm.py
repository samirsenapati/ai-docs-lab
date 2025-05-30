import os
from pathlib import Path
from openai import OpenAI

import httpx
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=httpx.Client(verify=False)  # ⛔ disables SSL verification
)


input_path = Path("../docs/generated/log_summary.md")
output_path = Path("../docs/drafts/incident_narrative.md")

prompt = input_path.read_text()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "You are a senior technical writer. Convert log summaries into incident narratives and RCA documentation."
        },
        {
            "role": "user",
            "content": f"Here is the log summary:\n\n{prompt}\n\nPlease generate a professional incident report."
        }
    ]
)

output_path.write_text(response.choices[0].message.content.strip())
print("✅ Draft generated at docs/drafts/incident_narrative.md")
