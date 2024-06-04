#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int potPin = A0; // Pin analógico donde está conectado el potenciómetro
const int buttonPin = 7; // Pin digital donde está conectado el botón
const int jamaicaPin = 2; // Pin digital asociado a la bebida Jamaica
const int naranjaPin = 3; // Pin digital asociado a la bebida Naranja
const int limonPin = 4; // Pin digital asociado a la bebida Limon

LiquidCrystal_I2C lcd(0x27, 16, 2); // Configura la pantalla LCD con la dirección I2C 0x27 y tamaño 16x2

int lastSensorValue = 0; // Variable para almacenar el último valor leído del potenciómetro
int selectedDrink = 0; // Variable para almacenar el tipo de bebida seleccionada (0: Jamaica, 1: Naranja, 2: Limon)
bool isDispensing = false; // Variable para indicar si se está dispensando una bebida

// Función para actualizar la pantalla LCD con un mensaje
void updateLCD(String message) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(message);
}

// Función para seleccionar la bebida
void selectDrink(int sensorValue) {
  if (sensorValue <= 341) {
    selectedDrink = 0; // Almacena el tipo de bebida seleccionada como Jamaica
    updateLCD("Jamaica");
  } else if (sensorValue <= 682) {
    selectedDrink = 1; // Almacena el tipo de bebida seleccionada como Naranja
    updateLCD("Naranja");
  } else {
    selectedDrink = 2; // Almacena el tipo de bebida seleccionada como Limon
    updateLCD("Limon");
  }
}

void setup() {
  lcd.init(); // Inicializa la pantalla LCD
  lcd.backlight(); // Activa la luz de fondo de la pantalla LCD
  pinMode(buttonPin, INPUT_PULLUP); // Configura el pin del botón como entrada con resistencia pull-up interna
  pinMode(jamaicaPin, OUTPUT); // Configura el pin de Jamaica como salida
  pinMode(naranjaPin, OUTPUT); // Configura el pin de Naranja como salida
  pinMode(limonPin, OUTPUT); // Configura el pin de Limon como salida

  // Asegúrate de que los pines están desactivados al inicio
  digitalWrite(jamaicaPin, LOW);
  digitalWrite(naranjaPin, LOW);
  digitalWrite(limonPin, LOW);
}

void loop() {
  int sensorValue = analogRead(potPin); // Lee el valor del potenciómetro (entre 0 y 1023)
  
  // Actualiza la pantalla LCD solo si el valor del potenciómetro cambia significativamente
  if (!isDispensing && abs(sensorValue - lastSensorValue) > 10) { // Cambia 10 según sea necesario
    lastSensorValue = sensorValue; // Actualiza el último valor leído del potenciómetro
    selectDrink(sensorValue);
  }

  // Verifica si se ha presionado el botón
  if (!isDispensing && digitalRead(buttonPin) == LOW) {
    isDispensing = true; // Establece que se está dispensando
    updateLCD("Dispensando:");
    lcd.setCursor(0, 1);
    switch (selectedDrink) {
      case 0:
        digitalWrite(jamaicaPin, HIGH); // Activa el pin de Jamaica
        lcd.print("Jamaica");
        break;
      case 1:
        digitalWrite(naranjaPin, HIGH); // Activa el pin de Naranja
        lcd.print("Naranja");
        break;
      case 2:
        digitalWrite(limonPin, HIGH); // Activa el pin de Limón
        lcd.print("Limon");
        break;
    }
    delay(5000); // Dispensar por 5 segundos
    
    // Desactivar todos los pines de las bebidas
    digitalWrite(jamaicaPin, LOW); 
    digitalWrite(naranjaPin, LOW); 
    digitalWrite(limonPin, LOW); 

    isDispensing = false; // Reinicia el estado de dispensación
    updateLCD("Elige bebida");
  }

  delay(100); // Espera un momento antes de volver a leer el potenciómetro
}
