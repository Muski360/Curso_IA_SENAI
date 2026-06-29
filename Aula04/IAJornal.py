import cv2
from pathlib import Path
# -- Framework do agente Agno --
from agno.media import Image
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.db.sqlite import SqliteDb
from agno.tools.newspaper import NewspaperTools
from agno.tools.file import FileTools
# -- Framework da openAI --
from openai import OpenAI


# -- Tools do framework --

#Chave API
API = ""

#Visao computacional
webcam = cv2.VideoCapture(0)
if webcam.isOpened():
    validacao, frame = webcam.read()
    while validacao:
        validacao, frame = webcam.read()
        cv2.putText(frame,
                    "Leitor de jornal",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    2
                    )
        cv2.imshow("Leito", frame)
        bt = cv2.waitKey(5)
        if bt == 27:
            break
    cv2.imwrite("Jornal.png", frame)
webcam.release()
cv2.destroyAllWindows()

caminho = Path("Jornal.png")

agente_Que_Le_Jornal = Agent(
    model=OpenAIResponses(
        id = "gpt-5.5",
        api_key = API,
    ),
    markdown=True,
    db=SqliteDb(db_file="jornal.db"),
    add_history_to_context=True,
    num_history_runs=3,
    learning=True,
    tools=[NewspaperTools(),FileTools()]
)

imagemJornal = caminho.read_bytes()
agente_Que_Le_Jornal.print_response(
    input = "Extraia todo o texto da noticia do jornal e salve o texto no arquivo noticia.txt",
    images = [Image(content=imagemJornal)]
)

arquivo = Path("noticia.txt")
textoNoticia = arquivo.read_text(encoding="utf-8")
cliente = OpenAI(api_key=API)

agente_de_fala = cliente.audio.speech.create(
    model = "gpt-4o-mini-tts",
    voice="alloy",
    input = textoNoticia,
)

agente_de_fala.stream_to_file("texto.mp3")

audio = Path(__file__).with_name("texto.mp3")

with audio.open("rb") as f:
    agente_de_transcricao = cliente.audio.transcriptions.create(
        model = "gpt-4o-transcribe",
        file = audio,
    )
print(agente_de_transcricao.text)
