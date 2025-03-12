// https://www.youtube.com/watch?v=P42ICrgAtS4
// https://circuitjournal.com/how-to-use-the-dfplayer-mini-mp3-module-with-an-arduino
// en este video añade botones de parar, repetir, next.. etc
// https://www.youtube.com/watch?v=-tH52i9Jhew 
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

// Use pins 2 and 3 to communicate with DFPlayer Mini
static const uint8_t PIN_MP3_TX = 2;
static const uint8_t PIN_MP3_RX = 3;
SoftwareSerial softwareSerial(PIN_MP3_RX, PIN_MP3_TX);

// Create the Player object
DFRobotDFPlayerMini player;

void setup() {
  // Init USB serial port for debugging
  Serial.begin(9600);
  // Init serial port for DFPlayer Mini
  softwareSerial.begin(9600);

  // Start communication with DFPlayer Mini
  if (player.begin(softwareSerial)) {
    Serial.println("OK");

    // Set volume to maximum (0 to 30).
    player.volume(30);
    // Play the "0001.mp3" in the "mp3" folder on the SD card
    player.playMp3Folder(1);

  } else {
    Serial.println("Connecting to DFPlayer Mini failed!");
  }
}

void loop() {
}

/**
// Codigo para mover el robot con ruedas y motores
// https://www.youtube.com/watch?v=yHMt62_y8t8

// Codigo + GTP
// Definimos pines del L298N
// IN1, IN2, IN3, IN4: Control de dirección de los motores

const int IN1 = 4;
const int IN2 = 5;
const int IN3 = 6;
const int IN4 = 7;
const int ENA = 9;  // Velocidad motor izquierdo
const int ENB = 10; // Velocidad motor derecho

void setup() {
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    pinMode(ENA, OUTPUT);
    pinMode(ENB, OUTPUT);

    // Inicialmente apagamos motores
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}

// Función para mover adelante
void adelante() {
    analogWrite(ENA, 150); // Ajusta velocidad (0-255)
    analogWrite(ENB, 150);
    
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
}

// Función para detenerse
void detener() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}

void loop() {
    adelante();  // Mueve el robot adelante
    delay(2000); // Espera 2 segundos
    detener();   // Detiene el robot
    delay(1000); // Espera 1 segundo
}



 */