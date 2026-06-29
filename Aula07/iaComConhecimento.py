from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.lancedb import LanceDb, SearchType

API = ""

# Configurar base de conhecimento para o Agente de IA

conhecimento = Knowledge(
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name = "meu_pdf",
        embedder = OpenAIEmbedder(api_key=API),
    ),
)

"""
conhecimento.insert(
name = "documento",
path="meu_documento.pdf"
)
"""

agenteCursoIA = Agent(
    model = OpenAIChat(
        id = "gpt-4o",
        api_key = API,
    ),
    knowledge= conhecimento,
    search_knowledge= True,
    instructions= "Busque na base de conhecimento, para responder as perguntas sobre o documento",
    markdown=True
)

agenteCursoIA.print_response("Qual são os requisitos para que uma ingresse no curso?")