#define BOTAO 27

void setup() {
  pinMode(BOTAO, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  if (digitalRead(BOTAO) == LOW) {
    Serial.println("CAPTURAR");
    delay(500); // debounce simples
  }
}