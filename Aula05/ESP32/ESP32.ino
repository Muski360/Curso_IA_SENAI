#define BOTAO 27

#define LED_GARRAFA 19
#define LED_CELULAR 18
#define LED_MOUSE 17
#define LED_BOLINHA 16
#define LED_TECLADO 4
#define LED_DESCONHECIDO 15

bool botaoAnterior = HIGH;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(50);

  pinMode(BOTAO, INPUT_PULLUP);

  pinMode(LED_GARRAFA, OUTPUT);
  pinMode(LED_CELULAR, OUTPUT);
  pinMode(LED_MOUSE, OUTPUT);
  pinMode(LED_BOLINHA, OUTPUT);
  pinMode(LED_TECLADO, OUTPUT);
  pinMode(LED_DESCONHECIDO, OUTPUT);

  apagarTodosLeds();

  Serial.println("Sistema iniciado");
}

void loop() {
  bool estadoBotao = digitalRead(BOTAO);

  if (botaoAnterior == HIGH && estadoBotao == LOW) {
    Serial.println("CAPTURAR");
    delay(200);
  }

  botaoAnterior = estadoBotao;

  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    apagarTodosLeds();

    if (comando == "LED19") {
      digitalWrite(LED_GARRAFA, HIGH);
    }

    else if (comando == "LED18") {
      digitalWrite(LED_CELULAR, HIGH);
    }

    else if (comando == "LED17") {
      digitalWrite(LED_MOUSE, HIGH);
    }

    else if (comando == "LED16") {
      digitalWrite(LED_BOLINHA, HIGH);
    }

    else if (comando == "LED4") {
      digitalWrite(LED_TECLADO, HIGH);
    }

    else {
      digitalWrite(LED_DESCONHECIDO, HIGH);
    }

    Serial.println("COMANDO_RECEBIDO");
  }
}

void apagarTodosLeds() {
  digitalWrite(LED_GARRAFA, LOW);
  digitalWrite(LED_CELULAR, LOW);
  digitalWrite(LED_MOUSE, LOW);
  digitalWrite(LED_BOLINHA, LOW);
  digitalWrite(LED_TECLADO, LOW);
  digitalWrite(LED_DESCONHECIDO, LOW);
}