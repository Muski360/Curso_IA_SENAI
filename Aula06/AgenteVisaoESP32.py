from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIResponses

import cv2

from pathlib import Path

API = ""

objetos1 = ["garrafa de água", "garrafa plástica", "garrafa", "garrafa térmica", "garrafa metálica"]
objetos2 = ["celular", "telefone", "aparelho celular", "smartphone"]
objetos3 = ["mouse"]
objetos4 = ["bola de ping pong", "bolinha de ping pong", "bola de tênis de mesa", "bolinha de tênis de mesa", "bola pequena", "bola", "bolinha", "bolinha branca", "bola branca"]
objetos5 = ["teclado"]

def agente_OP():
    caminhoImagem = Path("Foto.png")

    agenteWebCAM = Agent(
        model = OpenAIResponses(
            id = "gpt-5.2",
            api_key = API,
        ),
        markdown = False,
        instructions="""
    Você é um agente de visão computacional.

    Sua tarefa é identificar APENAS o objeto que está dentro do círculo azul da imagem.

    REGRAS OBRIGATÓRIAS:    

    1. Considere somente o objeto localizado dentro do círculo azul.
    2. Ignore completamente qualquer objeto fora do círculo azul.
    3. Caso uma pessoa esteja segurando um objeto dentro do círculo azul, identifique apenas esse objeto.
    4. Sua resposta deve conter APENAS UMA das seguintes palavras:

    GARRAFA
    CELULAR
    MOUSE
    BOLINHA
    TECLADO
    DESCONHECIDO

    5. Não escreva frases.
    6. Não escreva explicações.
    7. Não escreva pontuação.
    8. Não escreva texto adicional.
    9. Não use markdown.
    10. Se houver dúvida ou o objeto não pertencer a uma das categorias permitidas, responda apenas:

    DESCONHECIDO

    EXEMPLOS DE RESPOSTAS VÁLIDAS:
    GARRAFA
    CELULAR
    MOUSE
    BOLINHA
    TECLADO
    DESCONHECIDO

    EXEMPLOS DE RESPOSTAS INVÁLIDAS:
    "É uma garrafa"
    "Vejo um celular"
    "O objeto é um mouse"
    "Provavelmente uma bolinha"
    """)

    byte = caminhoImagem.read_bytes()

    resposta = agenteWebCAM.run(
        "Identifique o objeto dentro do círculo azul. Retorne apenas GARRAFA, CELULAR, MOUSE, BOLINHA, TECLADO OU DESCONHECIDO",
        images=[Image(content=byte)]
    )

    return resposta.content.strip().upper()

def escutar_arduino(porta_serial):
    while True:
        if porta_serial.in_waiting:
            comando = porta_serial.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            print(f"Recebido do ESP32: {comando}")

            if comando == "CAPTURAR":
                abrir_camera()
                return True

def abrir_camera():
    webcam = cv2.VideoCapture(0)

    if not webcam.isOpened():
        print("Erro: não foi possível abrir a webcam.")
        return

    janela = "Tirando foto"
    frameROI = None

    for i in range(3, -1, -1):
        validacao, frame = webcam.read()

        if not validacao:
            print("Erro: não foi possível capturar frame da webcam.")
            break

        imagem = cv2.flip(frame, 1)

        frameROI = cv2.circle(
            imagem,
            center=(320, 230),
            radius=100,
            color=(255, 0, 0),
            thickness=2,
            lineType=cv2.LINE_AA
        )

        cv2.putText(
            frameROI,
            f"Foto em {i}",
            (240, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2,
            cv2.LINE_AA
        )

        cv2.imshow(janela, frameROI)
        cv2.waitKey(1000)

    if frameROI is not None:
        cv2.imwrite("Foto.png", frameROI)
        print("Foto salva como Foto.png")

    webcam.release()
    cv2.destroyWindow(janela)