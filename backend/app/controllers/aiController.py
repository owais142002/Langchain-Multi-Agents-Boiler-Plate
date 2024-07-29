from adrf.decorators import api_view
import json
import uuid
import app.agents.routerAgent as MainAgentService
from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)    
        userId = data.get("user_id")
        query = data.get("query")

        agent = MainAgentService.createRouterAgent(userId)
        memory = MainAgentService.getMemory(userId)
        chat_history = memory.buffer_as_messages    
        print(chat_history)

        response = agent.invoke(
            {"input": query, "chat_history": chat_history},
            {"tags": [userId, query]},
        )    
        return JsonResponse(
                        {
                            "output":response["output"]
                        },
                        status=status.HTTP_200_OK,
                    )    