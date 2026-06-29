from agno.agent import Agent #Importa a classe Agent do módulo agno.agent
from agno.media import Image
from agno.models.openai import OpenResponses, OpenAIResponses
from pathlib import Path

#Definição de API
API = ""

#Qual é o caminho que esta a imagem.
imagem_caminho = Path("amostra.jpg")

#Configuração do agente
agenteVisao = Agent(
    model = OpenAIResponses(
        id = "gpt-5.2",
    api_key = API,),
    markdown=True,
)

#Converte a imagem em Bytes
imagemEmBytes = imagem_caminho.read_bytes()

agenteVisao.print_response(
    "Me fale sobre esta imagem.",
    images=[Image(content=imagemEmBytes)]
)