# A2A Math Solver Agent

This project demonstrates a Math Solver using A2A protocol between two agents:
- **Math Solver Agent**: Understands natural language questions.
- **Calculator Agent**: Executes arithmetic using expressions.

## How to Run
1. Start Calculator Agent:
```bash
uvicorn calculator_agent.server:app --port 8001
```

2. Start Math Solver Agent:
```bash
uvicorn math_solver_agent.server:app --port 8000
```

3. Run CLI:
```bash
python main.py
```

Try questions like:
- What is 5 + 3?
- What is 12 * 4?
