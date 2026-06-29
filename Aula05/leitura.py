import serial
import serial.tools.list_ports
import time
import AgenteESP32 as agente


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


print("Portas seriais disponíveis:")

for porta in listar_portas_serial():
    print(porta)

porta_escolhida = "COM4"
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
        agente.imagem_Camera()
        agente.agenteOP()

        if agente.ok is True:
            comando = "LIGAR"

            escrever_para_esp(
                connection_porta_serial,
                comando
            )

            print("Enviado. Aguardando resposta...")

            resposta = ler_porta_serial(
                connection_porta_serial
            )

            if resposta:
                print(f"ESP32 retornou: {resposta}")
            else:
                print(
                    "Nenhuma resposta recebida "
                    "dentro do timeout"
                )

        elif agente.ok is False:
            comando = "DESLIGAR"

            escrever_para_esp(
                connection_porta_serial,
                comando
            )

            print("Enviado. Aguardando resposta...")

            resposta = ler_porta_serial(
                connection_porta_serial
            )

            if resposta:
                print(f"ESP32 retornou: {resposta}")
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