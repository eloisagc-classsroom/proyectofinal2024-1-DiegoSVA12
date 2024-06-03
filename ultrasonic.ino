const int Trigger1 = 2;
const int Echo1 = 3;
const int Trigger2 = 6;
const int Echo2 = 5;
const int Trigger3 = 8;
const int Echo3 = 9;

void setup() {
  Serial.begin(9600); // Inicializa la comunicación serial con el HC-05 a 9600 baud
  pinMode(Trigger1, OUTPUT);
  pinMode(Echo1, INPUT);
  digitalWrite(Trigger1, LOW);

  pinMode(Trigger2, OUTPUT);
  pinMode(Echo2, INPUT);
  digitalWrite(Trigger2, LOW);

  pinMode(Trigger3, OUTPUT);
  pinMode(Echo3, INPUT);
  digitalWrite(Trigger3, LOW);
}

void loop() {
  long t1, t2, t3;
  long d1, d2, d3;

  // Sensor 1
  digitalWrite(Trigger1, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trigger1, LOW);
  t1 = pulseIn(Echo1, HIGH);
  d1 = t1 / 59;

  // Sensor 2
  digitalWrite(Trigger2, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trigger2, LOW);
  t2 = pulseIn(Echo2, HIGH);
  d2 = t2 / 59;

  // Sensor 3
  digitalWrite(Trigger3, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trigger3, LOW);
  t3 = pulseIn(Echo3, HIGH);
  d3 = t3 / 59;

  // Enviar ambas distancias en formato CSV
  Serial.print(d1);
  Serial.print(",");
  Serial.print(d2);
  Serial.print(",");
  Serial.println(d3);

  delay(1000);
}
