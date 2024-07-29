from langchain.tools import BaseTool
from app.agents.subagent_1.service.agentService import SubAgent1Service as subAgentService

class SubAgent1(BaseTool):
    name = ""
    description = ""
    userId = ""
    
    def __init__(self, agentJson, userId):
        super().__init__()
        self.name = agentJson["name"]
        self.description = agentJson["description"]
        self.userId = userId
        self.return_direct = False    
    
    def _run(self, input, run_manager) -> str:
        print(run_manager.tags)

        return "Return data to process by main agent's LLM"