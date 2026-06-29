import cv2
from pathlib import Path
from agno.db.sqlite import SqliteDb
from agno.media import Image
from agno.agent import Agent
from agno.models.openai import OpenAIResponses

objetos1 = ["garrafa de água", "garrafa"]

def recomendaciones(objeto:str):
    ok = False
    objeto.lower()
    for obj in range(len(objetos1)):
        if objetos1[obj] == objeto:
            ok = True
    if ok:
        return "Beba mais água"
    return "Não tenho recomendações p/ este objeto"




#API
API = ""

#Captura da imagem da WEBCAM do PC
webcam = cv2.VideoCapture(0)
if webcam.isOpened():
    validacao, frame = webcam.read()
    while validacao:
        validacao, frame = webcam.read()
        imagemCamera = cv2.flip(frame, 1)
        frameComRetangulo = cv2.rectangle(imagemCamera, (400,80), (200,400), (0,0,255), 3)
        cv2.imshow("Video da WebCAM", frameComRetangulo)
        chav = cv2.waitKey(5)
        if chav == 27: #ESC
            break
    cv2.imwrite("imagen.png", frame)
webcam.release()
cv2.destroyAllWindows()

caminhoImagem = Path("imagen.png")

agenteWebCAM = Agent(
    model = OpenAIResponses(
        id = "gpt-5.2",
        api_key = API,
    ),
    markdown = True,
    learning=True,
    #Adicionando memória
    db = SqliteDb(db_file="agenteImg.db"),
    add_history_to_context = True,
    num_history_runs= 5,
    tools=[recomendaciones],
    instructions="Você é um agente que somente reconhece os objetos que estão na imagem"
                 "e dentro do quadro vermelho."
                 "REGRAS:"
                 "NÃO FALAR SOBRE OS DEMAIS OBJETOS QUE ESTÃO FORA DO QUADRO VERMELHO."
                 "FALAR do objeto que a pessoa esta segurando."
                 "Somente falar o que é objeto sem mais detalhes"
)

byte = caminhoImagem.read_bytes()

# while True:
#     pergunta = input("\nDigite uma pergunta ou sair p/ encerrar o programa: ")
#     if pergunta.lower() == "sair":
#         print("Saindo do programa...")
#         break
#     agenteWebCAM.print_response(
#         pergunta,
#         images=[Image(content=byte)],
#     )

agenteWebCAM.print_response(
    "Me fale sobre esssa imagem e o resultado utilize a sua ferramenta e o que ela retorna",
    images=[Image(content=byte)],
)


