import requests
import uuid

base_url = "http://127.0.0.1:5000"

# Discover the agent
res = requests.get(f"{base_url}/.well-known/agent.json")
if res.status_code != 200:
    raise Exception("Failed to discover agent.")
agent_info = res.json()
print(f"Connected to: {agent_info['name']} – {agent_info['description']}")

while True:
    user_input = input("\nEnter a math expression or equation (or 'exit' to quit): ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    task_id = str(uuid.uuid4())
    task_payload = {
        "id": task_id,
        "message": {
            "role": "user",
            "parts": [
                {"text": user_input}
            ]
        }
    }

    response = requests.post(f"{base_url}/tasks/send", json=task_payload)
    if response.status_code != 200:
        print(f"Task failed: {response.text}")
        continue

    response_data = response.json()
    messages = response_data.get("messages", [])
    if messages:
        final_reply = messages[-1]["parts"][0]["text"]
        print("Agent says:", final_reply)
    else:
        print("No response received.")
