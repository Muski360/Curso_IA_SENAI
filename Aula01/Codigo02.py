from agno.agent import Agent
from agno.models.openai import OpenAIChat

#Defina sua chave API aqui
API = ""

agenteDeIA = Agent(
    model=OpenAIChat(
        id = "gpt-4.1",
        api_key = API,
        instructions="Você é um pirata chamado Davy Jones"
                     "você sempre responde como um marujo dos sete mares"
                     "Sempre començando com a palavra Glup e de a sua resposta"
                     "Você gosta de contar histórias sobre as aventuras nos mares"
    ),
    markdown=True
)

while True:
    pergunta = input("\nDigite sua pergunta ou sair p/ encerrar: ")
    if pergunta.lower() == "sair":
        break
    agenteDeIA.print_response(pergunta,stream=True)


