import os

from pathlib import Path
from dataclasses import dataclass
from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent

# 1. Configuração do Caminho do Banco de Dados
BASE_DIR = Path(__file__).resolve().parent
caminho_db = BASE_DIR / "chinook.db"

if not caminho_db.exists():
    raise FileNotFoundError('chinook.db não foi encontrado no diretório.')

# CORREÇÃO: Adicionado as chaves {} para interpolar a variável corretamente
db = SQLDatabase.from_uri(f"sqlite:///{caminho_db}")


# 2. Definição da Ferramenta (Tool) usando RunnableConfig para Contexto
@tool
def execute_sql(consulta: str, config: RunnableConfig) -> str:
    """
    Executa uma consulta SQL do tipo SELECT no banco de dados e retorna os resultados.
    Use esta ferramenta sempre que precisar consultar dados das tabelas.
    """
    # Recupera a instância do banco de dados que passamos na configuração do agente
    database: SQLDatabase = config["configurable"].get("db")

    if not database:
        return "Erro: O banco de dados não foi configurado no contexto de execução."

    try:
        # CORREÇÃO: SQLDatabase utiliza .run() em vez de .execute()
        resultado = database.run(consulta)
        return resultado
    except Exception as erro:
        return f"Erro ao executar a consulta: {erro}"


api_key = ""

os.environ["OPEN_API_KEY"] = api_key
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key, temperature=0)


# 4. Prompt do Sistema
prompt_sistema = """
Você é um analista de banco de dados SQL.
REGRAS:
    - Pense passo a passo;
    - Quando precisar de dados, chame a ferramenta 'execute_sql' com APENAS UMA consulta SELECT;
    - Somente Read-Only, NÃO faça INSERT, UPDATE, DELETE, ALTER, DROP, CREATE, REPLACE e TRUNCATE;
    - Limite de 5 linhas para a saída, a não ser que o usuário solicite mais linhas;
    - Se a ferramenta retornar um erro, revise o SQL e tente novamente;
    - Prefira colunas explícitas ao invés de SELECT * para evitar erros de sintaxe.
"""

# CORREÇÃO: Criação do agente utilizando o padrão oficial do LangGraph
agente_analista = create_react_agent(
    model=llm,
    tools=[execute_sql],
    state_modifier=prompt_sistema  # Define o prompt do sistema no LangGraph
),

# 5. Execução do Agente
pergunta = "Qual tabela tem mais registros?"

# CORREÇÃO: Passamos o contexto de tempo de execução através do dicionário 'configurable'
configuracao_execucao = {"configurable": {"db": db}}

for passos in agente_analista.stream(
        {"messages": [("user", pergunta)]},
        config=configuracao_execucao,
        stream_mode="values"
):
    # Imprime o conteúdo da última mensagem gerada no fluxo
    ultima_mensagem = passos["messages"][-1]
    print(f"[{ultima_mensagem.type.upper()}]: {ultima_mensagem.content}\n")