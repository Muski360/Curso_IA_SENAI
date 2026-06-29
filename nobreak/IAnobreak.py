from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.db.sqlite import SqliteDb

API = ""

# Configurar base de conhecimento para o Agente de IA

conhecimento = Knowledge(
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name = "instructions_pdf",
        embedder = OpenAIEmbedder(api_key=API),
    ),
)

"""
conhecimento.insert(
name = "documento",
path="instructions.pdf"
)
"""

agenteChatBot = Agent(
        model=OpenAIChat(
            id="gpt-5.2",
            api_key=API,
        ),
        markdown=True,
        learning=True,
        # Adicionando memória
        db=SqliteDb(db_file="agenteNoBreak.db"),
        add_history_to_context=True,
        num_history_runs=5,
        knowledge=conhecimento,
        search_knowledge=True,
        instructions = "Você é o chatbot da empresa Luffy e está conversando diretamente com o usuário, e não um intermediador. Responda sempre em primeira pessoa (utilizando 'eu'). Seu objetivo é responder às perguntas baseando-se única e exclusivamente nas informações do seu contexto interno. É estritamente proibido citar trechos diretamente ou mencionar termos como 'de acordo com o documento', 'com base no PDF', 'no texto fornecido' ou qualquer variação que indique que você está lendo um arquivo. Responda de forma natural, como se todo o conhecimento fosse seu por natureza. Se a resposta para a pergunta do usuário não estiver nas informações que você recebeu, responda educadamente que não sabe ou não tem essa informação, mantendo o mesmo estilo, sem inventar dados adicionais."
    )

while True:
    pergunta = input("\nDigite uma pergunta ou sair p/ encerrar o programa: ")
    if pergunta.lower() == "sair":
        print("Saindo do programa...")
        break
    agenteChatBot.print_response(
          pergunta
    )

