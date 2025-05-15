import asyncio
import httpx

async def ask_math_solver():
    while True:
        question = input("Enter a math question (or type 'exit'): ")
        if question.lower() == "exit":
            break
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/", json={
                "jsonrpc": "2.0",
                "method": "math/solve",
                "params": {"question": question},
                "id": 1
            })
            print("Answer:", response.json().get("result", {}).get("answer"))

if __name__ == "__main__":
    asyncio.run(ask_math_solver())
