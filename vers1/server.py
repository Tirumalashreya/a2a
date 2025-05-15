from flask import Flask, request, jsonify
from sympy import simplify, sympify, solve, symbols
from sympy.parsing.sympy_parser import parse_expr

app = Flask(__name__)

@app.route("/.well-known/agent.json", methods=["GET"])
def agent_card():
    return jsonify({
        "name": "SymPyAgent",
        "description": "Solves symbolic math expressions and equations.",
        "url": "http://localhost:5000",
        "version": "1.0",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False
        }
    })

@app.route("/tasks/send", methods=["POST"])
def handle_task():
    try:
        task = request.get_json()
        task_id = task.get("id")
        user_input = task["message"]["parts"][0]["text"].strip()

        # Very simple parsing logic
        if "=" in user_input:
            # Handle equations like "x**2 - 4 = 0"
            expr_left, expr_right = user_input.split("=")
            x = symbols("x")
            solution = solve(parse_expr(expr_left) - parse_expr(expr_right), x)
            reply_text = f"Solution: {solution}"
        else:
            # Simplify expression like "sin(x)**2 + cos(x)**2"
            simplified = simplify(parse_expr(user_input))
            reply_text = f"Simplified: {simplified}"

    except Exception as e:
        reply_text = f"Error: {str(e)}"

    return jsonify({
        "id": task_id,
        "status": {"state": "completed"},
        "messages": [
            task["message"],
            {
                "role": "agent",
                "parts": [{"text": reply_text}]
            }
        ]
    })

if __name__ == "__main__":
    app.run(port=5000)
