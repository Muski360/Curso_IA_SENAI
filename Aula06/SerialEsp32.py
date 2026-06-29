import serial
import serial.tools.list_ports
import time
import AgenteVisaoESP32 as agente
from pathlib import Path
from openai import OpenAI
from playsound import playsound


def listar_portas_serial() -> list:
    # Retorna a lista de portas seriais disponíveis
    return [porta.device for porta in serial.tools.list_ports.comports()]


def abrir_porta_serial(
    porta: str,
    baudrate: int = 115200,
    timeout: float = 1.0
) -> serial.Serial:
    porta_serial = serial.Serial(porta, baudrate, timeout=timeout)
    time.sleep(2)
    return porta_serial


def escrever_para_esp(porta_serial: serial.Serial, mensagem: str) -> None:
    if not porta_serial.is_open:
        raise serial.SerialException("A porta serial não está aberta.")

    payload = mensagem.strip() + "\n"
    porta_serial.write(payload.encode("utf-8"))
    porta_serial.flush()


def ler_porta_serial(porta_serial: serial.Serial) -> str:
    if not porta_serial.is_open:
        raise serial.SerialException("A porta serial não está aberta.")

    linha = porta_serial.readline().decode(
        "utf-8",
        errors="ignore"
    ).strip()

    return linha

def agente_fala(inputTexto: str):
    print(f"Texto gerado: {inputTexto}")

    cliente = OpenAI(api_key=agente.API)

    nome_audio = f"texto_{int(time.time() * 1000)}.mp3"
    audio = Path(__file__).with_name(nome_audio)

    try:
        with cliente.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=inputTexto,
        ) as resposta:
            resposta.stream_to_file(str(audio))

        print(f"Áudio gerado: {audio.name}")
        print("Tocando agora...")

        playsound(str(audio))

        print("Áudio finalizado.")

    finally:
        # Tenta apagar depois, mas se o Windows ainda estiver segurando, ignora
        try:
            if audio.exists():
                audio.unlink()
        except PermissionError:
            print("Aviso: o Windows ainda está usando o áudio, não consegui apagar agora.")


print("Portas seriais disponíveis:")

for porta in listar_portas_serial():
    print(porta)

porta_escolhida = "COM7"
baudrate = 115200

try:
    connection_porta_serial = abrir_porta_serial(
        porta_escolhida,
        baudrate
    )

    print(
        f"Conectado em {porta_escolhida} "
        f"com {baudrate} bps"
    )

except Exception as e:
    print("Erro ao abrir porta:", e)
    exit()

try:
    while True:
        agente.escutar_arduino(connection_porta_serial)
        objeto = agente.agente_OP()

        if objeto == "GARRAFA":
            escrever_para_esp(connection_porta_serial, "LED19")
            input_texto = "Objeto GARRAFA identificado. Acendendo LED19."

        elif objeto == "CELULAR":
            escrever_para_esp(connection_porta_serial, "LED18")
            input_texto = "Objeto CELULAR identificado. Acendendo LED18."

        elif objeto == "MOUSE":
            escrever_para_esp(connection_porta_serial, "LED17")
            input_texto = "Objeto MOUSE identificado. Acendendo LED17."

        elif objeto == "BOLINHA":
            escrever_para_esp(connection_porta_serial, "LED16")
            input_texto = "Objeto BOLINHA identificado. Acendendo LED16."

        elif objeto == "TECLADO":
            escrever_para_esp(connection_porta_serial, "LED4")
            input_texto = "Objeto TECLADO identificado. Acendendo LED4."

        else:
            escrever_para_esp(connection_porta_serial, "LED15")
            input_texto = "Nenhum objeto foi identificado. Acendendo LED15."

        print("Enviado. Aguardando resposta...")

        resposta_esp = ler_porta_serial(connection_porta_serial)

        if resposta_esp:
            print(f"ESP32 retornou: {resposta_esp}")
            agente_fala(input_texto)
        else:
            print(
                "Nenhuma resposta recebida "
                "dentro do timeout"
                )

except KeyboardInterrupt:
    print("\nEncerrando...")

finally:
    if "connection_porta_serial" in locals():
        connection_porta_serial.close()

    print("Porta serial fechada.")