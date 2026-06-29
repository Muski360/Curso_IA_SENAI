from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIResponses

import cv2

from pathlib import Path

API = ""

objetos1 = ["garrafa de água", "garrafa plástica", "garrafa", "garrafa térmica", "garrafa metálica"]

ok = False

#Criar ferramenta da IA
def recomenda(objeto:str):
    global ok
    ok = False
    for obj in range(len(objetos1)):
        if objetos1[obj] == objeto:
            ok = True
            break
    if ok:
        return "LIGAR"

    ok = False
    return "DESLIGAR"

def imagem_Camera():
    webcam = cv2.VideoCapture(0)

    if webcam.isOpened():
        validacao, frame = webcam.read()
        while validacao:
            validacao, frame = webcam.read()
            imagem = cv2.flip(frame[:, :, :3], 1)
            frameROI = cv2.circle(imagem, center=(320, 230), radius = 80, color = (255, 0, 0), thickness = 2, lineType = cv2.LINE_AA)
            cv2.imshow(winname="Webcam", mat=frameROI)
            tecla = cv2.waitKey(5)
            if tecla == 27:
                break
        cv2.imwrite(filename = "Foto.png", img = frameROI)
        webcam.release()
        cv2.destroyAllWindows()

def agente_OP():
    caminhoImagem = Path("Foto.png")

    agenteWebCAM = Agent(
        model = OpenAIResponses(
            id = "gpt-5.2",
            api_key = API,
        ),
        markdown = True,
        tools=[recomenda],
        instructions="Você é um agente que somente reconhece os objetos que estão na imagem"
                     "e dentro do circulo azul, retornando apenas o objeto. Você deve retornar apenas uma palavra, de acordo com sua tool, ligar ou desligar"
                     "REGRAS:"
                     "NÃO FALAR SOBRE OS DEMAIS OBJETOS QUE ESTÃO FORA DO CIRCULO AZUL."
                     "FALAR do objeto que a pessoa esta segurando."
                     "Somente falar o que é objeto sem mais detalhes"
    )

    byte = caminhoImagem.read_bytes()

    agenteWebCAM.print_response(
        "Retorne apenas LIGAR ou DESLIGAR",
        images=[Image(content=byte)]
    )

cap.release()