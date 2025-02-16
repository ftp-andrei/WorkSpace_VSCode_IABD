// Simulacion real
// https://www.youtube.com/watch?v=JEipwJKkugg

//INCLUIR LA LIBRERIA
#include <Servo.h>


//Variables Servo
int pinBoton = 2;
int pinServo = 11;
int estado = false;
Servo motorServo; // objeto servo
//Variables zumbador
int ButtonState = false;
int Buzzer = 8;

void setup()
{
  // Zumbador + LEDS
  pinMode(7, INPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(Buzzer, OUTPUT);
  // Servo
  pinMode(pinBoton, INPUT);
  // Asociamos el objeto al pin
  motorServo.attach(pinServo);
  // Configuramos para detectar cambios
  attachInterrupt(digitalPinToInterrupt(pinBoton), moverServo, CHANGE);

}

void loop()
{	
  // Zumbador-LEDS
	ButtonState = digitalRead(7);
  if(ButtonState == HIGH){
    digitalWrite(9, HIGH);
	digitalWrite(10, HIGH);
    // tone (Buzzer,150,1000);
    playScream();
    delay(1000);
  }
  else{
    digitalWrite(9, LOW);
    digitalWrite(10, LOW);
  }
  
  // Servo
  if(estado){
    motorServo.write(180);
  }else{
    motorServo.write(0);
  }
  delay(200);
}

// Funcion mover servo
void moverServo(){
  estado = !estado;
}

void playScream() {
  // Simular un grito con tonos altos y cambios rápidos
  tone(Buzzer, 2000, 200); // Tonos altos por 200ms
  delay(200);
  tone(Buzzer, 2500, 200);
  delay(200);
  tone(Buzzer, 3000, 300);
  delay(300);
  noTone(Buzzer); // Apagar buzzer
}