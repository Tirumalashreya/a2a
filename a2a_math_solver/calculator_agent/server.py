from starlette.applications import Starlette
from starlette.routing import Route
from json_rpc.json_rpc import JSONRPCHandler
from calculator_agent.tasks import TASKS
from calculator_agent.agent_card import AGENT_CARD

rpc_handler = JSONRPCHandler(tasks=TASKS, agent_card=AGENT_CARD)

app = Starlette(debug=True, routes=[
    Route("/", rpc_handler.endpoint, methods=["POST"]),
    Route("/agent_card", rpc_handler.agent_card, methods=["GET"]),
])
