from agno.agent import Agent
from agno.models.openai import OpenAIChat

#Aqui vc define sua chave API
API = ""

agente = Agent(
    model = OpenAIChat(
        id = "gpt-5.4-nano",
        api_key = API,
    ),
    markdown=True,
)

pergunta = "Onde fica a unidade do SENAI de Americana (centro) ou alguma unidade específica (ex.: “prédio/centro de treinamento?"
agente.print_response(pergunta, stream=True)

pergunta = "Qual curso tem nesta unidade"
agente.print_response(pergunta, stream=True)