/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 8 May 2014
  by Scott Fitzgerald
  modified 2 Sep 2016
  by Arturo Guadalupi
  modified 8 Sep 2016
  by Colby Newman

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Blink
*/

#define DELAY       80  // период для обычной скорости
#define DELAY_SLOW  150 // период для медленной скорости

// дискретные сигналы управления шаговым двигателем
#define ENA_PIN     8
#define DIR_X_PIN   5
#define STEP_X_PIN  2
#define DIR_Y_PIN   6
#define STEP_Y_PIN  3

#define ENDSTOP_X   9      // дискретный вход концевика датчика оборотов

#define RX_BUF_SIZE    50u // размер буфера приёма UART

#define BAUD_RATE    9600u // скорость обмена UART

enum eState
{
  NONE,
  START,
  RUN,
  ENDSTOP,
  WAIT_FOR_CMD,
  STOPPED
};

enum eCMD
{
  CMD_START,
  CMD_STOP,
  CMD_NONE
};

String STOP_STR  = "STOP";
String START_STR = "START";

eState State = NONE;    // режим работы устройства
eCMD CMD     = CMD_NONE;

int _delay;        // продолжительность шага двигателя
int steps_cnt = 0; // счётчик шагов
int steps_per_rev_cnt = 0; // счётчик шагов на оборот
int revs_cnt = 0;  // счётчик оборотов

int RxBufferCnt = 0;
uint8_t RxBuffer[RX_BUF_SIZE];
String RxStr = "";

void SeteState(eState state);
bool IsEndStop(void);
void MotorEnable(void);
void MotorDisable(void);
void MotorTakeStep(void);
void CommandReaceiver(void);

// the setup function runs once when you press reset or power the board
void setup() 
{
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(ENA_PIN, OUTPUT);
  pinMode(DIR_X_PIN, OUTPUT);
  pinMode(STEP_X_PIN, OUTPUT);
  pinMode(ENDSTOP_X, INPUT);
  // pinMode(DIR_Y_PIN, OUTPUT);
  // pinMode(STEP_Y_PIN, OUTPUT);

  digitalWrite(ENA_PIN, LOW);
  digitalWrite(DIR_X_PIN, LOW);
  digitalWrite(ENDSTOP_X, HIGH);
  // digitalWrite(DIR_Y_PIN, LOW);

  Serial.begin(BAUD_RATE);

  Serial.println("");
  Serial.println("-----------------------------");

  SeteState(NONE);

  Serial.println("setup()");
  Serial.print("BAUD_RATE:");
  Serial.println(BAUD_RATE);
  Serial.println("Start program!");
}



// the loop function runs over and over again forever
void loop() 
{

  switch(State)
  {
    case NONE:
      MotorDisable();
      SeteState(WAIT_FOR_CMD);
      break;
    case START:
      _delay = DELAY_SLOW;
      MotorEnable();
      if(IsEndStop())
      {
        MotorTakeStep();
      }
      else
      {
        SeteState(RUN);
      }
      break;
    case RUN:
      _delay = DELAY;
      MotorTakeStep();
      if(IsEndStop())
      { 
        SeteState(ENDSTOP);
        // MotorDisable();
        Serial.print("steps_per_rev_cnt:");Serial.println(steps_per_rev_cnt);
        steps_per_rev_cnt = 0;
      }
      break;
    case ENDSTOP:
      _delay = DELAY_SLOW;
      MotorTakeStep();
      if(steps_per_rev_cnt > 400)
      {
        MotorDisable();
        SeteState(WAIT_FOR_CMD);
        Serial.print("steps_cnt:");Serial.println(steps_cnt);
        Serial.print("steps_per_rev_cnt:");Serial.println(steps_per_rev_cnt);
        // steps_per_rev_cnt = 0;
        Serial.print("revs_cnt:");Serial.println(++revs_cnt);
        Serial.println("ENDSTOP");
      }
      break;
    case WAIT_FOR_CMD:
      if(CMD == CMD_START)
      {
        CMD = CMD_NONE;
        SeteState(START);
      }
      break;
    default:
      break;
  }

  CommandReaceiver();
}
// -----------------------------------------------------------------------------
// Функция смены режима работы
// -----------------------------------------------------------------------------
void SeteState(eState state)
{
  State = state;
  Serial.print("Set new state:");

  switch(state)
  {
    case NONE:
      Serial.println("NONE");
      break;
    case START:
      Serial.println("START");
      break;
    case WAIT_FOR_CMD:
      Serial.println("WAIT_FOR_CMD");
      break;
    case RUN:
      Serial.println("RUN");
      break;
    case ENDSTOP:
      Serial.println("ENDSTOP");
      break;
    case STOPPED:
      Serial.println("STOPPED");
      break;
    default:
      Serial.print("default:");
      Serial.println(state);
      break;
  }
}
// -----------------------------------------------------------------------------
// Функции управления мотором
// -----------------------------------------------------------------------------
bool IsEndStop(void)
{
  return (digitalRead(ENDSTOP_X) == 0);
}
// -----------------------------------------------------------------------------
void MotorEnable(void)
{
  digitalWrite(ENA_PIN, LOW);
}
// -----------------------------------------------------------------------------
void MotorDisable(void)
{
  digitalWrite(ENA_PIN, HIGH);
}
// -----------------------------------------------------------------------------
void MotorTakeStep(void)
{
  digitalWrite(LED_BUILTIN, HIGH);
  digitalWrite(STEP_X_PIN, HIGH);
  delayMicroseconds(_delay);

  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(STEP_X_PIN, LOW);
  delayMicroseconds(_delay);

  ++steps_cnt;
  ++steps_per_rev_cnt;
}
// -----------------------------------------------------------------------------
// Функция приёма команд
// -----------------------------------------------------------------------------
void CommandDetector(String cmd)
{
  if(cmd == STOP_STR)
  {
    CMD = CMD_STOP;
    Serial.println("cmd == STOP_STR");
  }
  if(cmd == START_STR)
  {
    CMD = CMD_START;
    Serial.println("cmd == START_STR");
  }
}
// -----------------------------------------------------------------------------
void CommandReaceiver(void)
{
  if( Serial.available() )
  {
    while(Serial.available())
    {
      char inChar = Serial.read();

      if(inChar == '\n')
      {
        Serial.println("RECEIVED");
        Serial.println(inChar);
        Serial.println(RxStr);
        CommandDetector(RxStr);
        RxStr = "";
      }
      else
      {
        RxStr += inChar; // Serial.readString();
      }
    }
  }
}
// -----------------------------------------------------------------------------
