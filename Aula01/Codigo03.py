from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb


#Defina a sua chave API da OpenAI aqui
API = ""

agenteMemo = Agent(
    model=OpenAIChat(
        id = "gpt-4.1",
        api_key = API,
        instructions= "Você é o Michael Jackson"
                      "Você sempre responde com "
                      "seu grito caracteristo as perguntas "
                      "dos usuarios"
                      "E no final das perguntas diz Billi Jean"
    ),
    db = SqliteDb(db_file="agent.db"),
    num_history_runs= 3,
    add_history_to_context= True,
    markdown=True
)

while True:
    pergunta = input("\nDigite uma pergunta: ")
    if pergunta.lower() == "sair":
        break
    agenteMemo.print_response(pergunta)