from app.agents.subagent_1.agent import SubAgent1
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
import GlobalConstants
from app.utils import getPromptTemplate

agents = {
    SubAgent1 : {
        "name": "Name of Sub Agent",
        "description": "Description of Sub Agent"
    }
}



def getMemory(userId):
    message_history = SQLChatMessageHistory(
        connection=GlobalConstants.SQL_CONNECTION_STRING,
        session_id=userId,
        table_name="chat_history",
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=message_history,
        return_messages=True,
        output_key="output",
    )
    return memory


def getLLM():
    llm = ChatOpenAI(
            temperature=0,
            model=GlobalConstants.LLM_MODEL,
            openai_api_key=GlobalConstants.LLM_API_KEY,
        )    

    return llm


def createRouterAgent(userId):
    subAgents = []
    for agent in agents:
        subAgents.append(agent(agentJson=agents[agent], userId=userId))
    print(subAgents)
    memory = getMemory(userId=userId)
    prompt = getPromptTemplate(GlobalConstants.MAIN_AGENT_SYSTEM_MESSAGE)
    llm = getLLM()    
    agent = create_openai_tools_agent(llm=llm, tools=subAgents, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=subAgents,
        verbose=GlobalConstants.IS_DEBUG_MODE,
        memory=memory,
        max_iterations=GlobalConstants.MAX_AGENT_ITERATIONS
    )
    return agent_executor    