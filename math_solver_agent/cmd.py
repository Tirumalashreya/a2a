import asyncio
import httpx

async def interactive_cli():
    print(" Math Solver Agent CLI")
    while True:
        user_input = input("\nEnter a math query (or 'exit'): ")
        if user_input.lower() in ['exit', 'quit']:
            break

        payload = {
            "jsonrpc": "2.0",
            "method": "a2a.task",
            "params": {"input": user_input},
            "id": "cli-1"
        }

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post("http://localhost:8000/a2a", json=payload)
                result = resp.json().get("result", {}).get("output", "No result.")
                print(" Answer:", result)
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    asyncio.run(interactive_cli())
