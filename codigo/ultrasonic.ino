// Definición de pines para los tres sensores ultrasónicos
const int Trigger1 = 2;
const int Echo1 = 3;
const int Trigger2 = 6;
const int Echo2 = 5;
const int Trigger3 = 8;
const int Echo3 = 9;

void setup() {
  Serial.begin(9600); // Inicializa la comunicación serial a 9600 baud
  // Configuración de los pines del Sensor 1
  pinMode(Trigger1, OUTPUT); // Establece el pin Trigger1 como salida
  pinMode(Echo1, INPUT); // Establece el pin Echo1 como entrada
  digitalWrite(Trigger1, LOW); // Asegura que el pin Trigger1 esté inicialmente en LOW

  // Configuración de los pines del Sensor 2
  pinMode(Trigger2, OUTPUT); // Establece el pin Trigger2 como salida
  pinMode(Echo2, INPUT); // Establece el pin Echo2 como entrada
  digitalWrite(Trigger2, LOW); // Asegura que el pin Trigger2 esté inicialmente en LOW

  // Configuración de los pines del Sensor 3
  pinMode(Trigger3, OUTPUT); // Establece el pin Trigger3 como salida
  pinMode(Echo3, INPUT); // Establece el pin Echo3 como entrada
  digitalWrite(Trigger3, LOW); // Asegura que el pin Trigger3 esté inicialmente en LOW
}

void loop() {
  long t1, t2, t3; // Variables para almacenar el tiempo de respuesta de cada sensor
  long d1, d2, d3; // Variables para almacenar la distancia calculada de cada sensor

  // Medición del Sensor 1
  digitalWrite(Trigger1, HIGH); // Envía un pulso de 10 microsegundos en el pin Trigger1
  delayMicroseconds(10); 
  digitalWrite(Trigger1, LOW); // Termina el pulso en el pin Trigger1
  t1 = pulseIn(Echo1, HIGH); // Mide el tiempo que tarda en recibir el eco en el pin Echo1
  d1 = t1 / 59; // Calcula la distancia en cm (el valor 59 es una constante de conversión)

  // Medición del Sensor 2
  digitalWrite(Trigger2, HIGH); // Envía un pulso de 10 microsegundos en el pin Trigger2
  delayMicroseconds(10); 
  digitalWrite(Trigger2, LOW); // Termina el pulso en el pin Trigger2
  t2 = pulseIn(Echo2, HIGH); // Mide el tiempo que tarda en recibir el eco en el pin Echo2
  d2 = t2 / 59; // Calcula la distancia en cm

  // Medición del Sensor 3
  digitalWrite(Trigger3, HIGH); // Envía un pulso de 10 microsegundos en el pin Trigger3
  delayMicroseconds(10); 
  digitalWrite(Trigger3, LOW); // Termina el pulso en el pin Trigger3
  t3 = pulseIn(Echo3, HIGH); // Mide el tiempo que tarda en recibir el eco en el pin Echo3
  d3 = t3 / 59; // Calcula la distancia en cm

  // Enviar las distancias medidas en formato CSV (valores separados por comas)
  Serial.print(d1); // Imprime la distancia medida por el Sensor 1
  Serial.print(","); // Imprime una coma para separar los valores
  Serial.print(d2); // Imprime la distancia medida por el Sensor 2
  Serial.print(","); // Imprime una coma para separar los valores
  Serial.println(d3); // Imprime la distancia medida por el Sensor 3 y un salto de línea

  delay(1000); // Espera 1 segundo antes de realizar la siguiente medición
}
