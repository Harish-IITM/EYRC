/*
*Team Id: <GG_2336>
*Author List: <Ajan,Dhiraj,Harish,Santhosh>
*File name: <GG_2336_Task_6>
*Theme: <GeoGuide>
*Functions : <straight(),stop_1(),left(),right()>
*Global Variables: <ir_pin_1,ir_pin_2,ir_pin_3,ir_pin_4,ir_pin_5,in1,in2,in3,in4,d1,d2,d3,d4,d5,k_1,k_2,l_1,l_2,c,stops,en_a,en_b,con,buzzer,j,func_call,msg,w_1>
*/







#include <WiFi.h>
int ir_pin_1=26;
int ir_pin_2=25;
int ir_pin_3=33;
int ir_pin_4=32;
int ir_pin_5=35;
int in1=2;
int in2=4;
int in3=5;
int in4=18;
int d1;
int d2;
int d3;
int d4;
int d5;
int k_1;
int k_2;
int l_1;
int l_2;
int c=0;
int stops=0;
int en_a =15;
int en_b=19;
int con=0;
int led=22;
int buzzer=23;
int j;
int func_call;
String msg;
unsigned long start_time,current_time;
int w_1;


const char* ssid = "Pixel";        
const char* password =  "djdhiraj";  
const uint16_t port = 8002;
const char * host = "192.168.89.1";
int e=0; 
WiFiClient client;
/*
*Function Name: setup()
*Input: -
*Output: -
*Logic: used for assinging input and output running only once
and also connecting to wifi.
*/

void setup(){
  pinMode(en_a,OUTPUT);
  pinMode(en_b,OUTPUT);
  pinMode(ir_pin_1,INPUT);
  pinMode(ir_pin_2,INPUT);
  pinMode(ir_pin_3,INPUT);
  pinMode(ir_pin_4,INPUT);
  pinMode(ir_pin_5,INPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(buzzer,OUTPUT);
  
  pinMode(led,OUTPUT);

  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
    }

  Serial.println("Connected to WiFi");
}

/*
*Function Name: straight()
*Input: -
*Output: l_1,l_2 which are the speed of the wheels just before reaching node 
*Logic: used for running bot in straight path along with line following
*Example call:l_1,l_2=straight();
*/





int straight(){
  k_1=505;
  k_2=500;
    if((d2+d3+d4>=1) and not (d2==1 and d3==1 and d4==1))
  {
    analogWrite(en_a,505+100*d4-100*d2);
    analogWrite(en_b,500+100*d2-100*d4);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    l_1=505+100*d4-100*d2;
    l_2=500+100*d2-100*d4;
    delay(5);
  }



    else if((d1==1 or d5==1)  and not(d1==1 and d5==1))
  {
    if(d1==1)
    {
      analogWrite(en_a,300+450*d1);
      analogWrite(en_b,300);
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
      delay(50);
    }
    if(d5==1)
    {
      analogWrite(en_a,300);
      analogWrite(en_b,300+450*d5);
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
      delay(50);
    }

  }
  else if(d1+d2+d3+d4+d5==0)
  {
    analogWrite(en_a,k_1);
    analogWrite(en_b,k_2);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    delay(10);
  }
  return l_1,l_2;
}

/*
*Function Name: left()
*Input: -
*Output: -
*Logic: used for turning the bot left
*Example Call: left();
*/

void left(){
  d3=digitalRead(ir_pin_3);
  if(d3==0){
    straight();
    delay(20);
  }
    analogWrite(en_a,505);
    analogWrite(en_b,500);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    delay(250);
    analogWrite(en_a,505);
    analogWrite(en_b,500);
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    delay(150);
  d3=digitalRead(ir_pin_3);

  while(d3==0){
    d3=digitalRead(ir_pin_3);
    analogWrite(en_a,505);
    analogWrite(en_b,500);
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    delay(10);

  }
  
}

/*
*FunctionNmae: right()
*Input: -
*Output: -
*Logic: used for turning bot right
*Example Call: right();
*/

void right(){
  d3=digitalRead(ir_pin_3);
  if(d3==0){
    straight();
    delay(20);
  }
    analogWrite(en_a,505);
    analogWrite(en_b,500);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    delay(50);
    analogWrite(en_a,505);
    analogWrite(en_b,500);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    delay(200);
  d3=digitalRead(ir_pin_3);

  while(d3==0){
    d3=digitalRead(ir_pin_3);
    analogWrite(en_a,505);
    analogWrite(en_b,500);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    delay(10);

  }
}

/*
*FunctionNmae: stop1()
*Input: -
*Output: -
*Logic: used for giving buzzer beep for 5 sec and stop at the end node.
*Example Call: stop1(); 
*/



void stop1(){
  
  
      digitalWrite(in1, LOW);           
      digitalWrite(in2, LOW);
      digitalWrite(in3, LOW);           
      digitalWrite(in4, LOW); 
      delay(5000);
      
}


/*
*FunctionNmae: loop()
*Input: -
*Output: -
*Logic: all the main stuff run here 
        1. connecting to host
        2. after connection , whenever a node is reached a data will be sent from host to client for turning right or left or straight
        3. aswell as whenever a required a region where the buzzer needs to beep we will send data from client to host for stopping bot and to beep buzzer for 1 sec 
        4. calling all the before functions
        5. if no condition then run straight

*/


void loop(){
  digitalWrite(buzzer,HIGH);
  // for connecting to host or else the bot doesnt move
  if (!client.connect(host, port)) {
    Serial.println("Connection to host failed");
    digitalWrite(in1, LOW);           
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);           
    digitalWrite(in4, LOW); 
    delay(200);
    return;
  }
  
  // after connection established
    while(1){
        con=0;
        d1 = digitalRead(ir_pin_1);
        d2 = digitalRead(ir_pin_2);
        d3 = digitalRead(ir_pin_3);
        d4 = digitalRead(ir_pin_4);
        d5 = digitalRead(ir_pin_5);
      // when node reached sending data to host and receving data for turning from host,
      //    accordingly calling fuction
       
      if(d2+d3+d4==3 ){       
        analogWrite(en_a,l_1);
        analogWrite(en_b,l_2);
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
        delay(200);

        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
        digitalWrite(in3, LOW);
        digitalWrite(in4, LOW);
        delay(10);
        con=1;
        client.print(con);
      msg = client.readStringUntil('\n');         //Read the message through the socket until new line char(\n)
              
      func_call = msg.toInt();
      Serial.println(func_call);
        while(func_call!=1 and func_call!=2 and func_call!=3){
    digitalWrite(in1, LOW);           
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);           
    digitalWrite(in4, LOW);
    con=1;
    client.print(con);
    msg = client.readStringUntil('\n');         //Read the message through the socket until new line char(\n)
    func_call = msg.toInt(); 
        }
        if (func_call==1){
          straight();
        }
        if (func_call==2){
          left();
        }
        if (func_call==3){
          right();
          
        }
    // for clearing any unwanted data
     while(client.available()){
      char dummy = client.read();
      
     }
    j=0;
  }
  client.print(2);
    
    if(j==0){
    // whenever clients sends msg other than at node this loop occurs and for stopping and buzzer beeeping
    if (client.available()){
      if(e<4){
      digitalWrite(in1,LOW);
      digitalWrite(in2,LOW);
      digitalWrite(in3,LOW);
      digitalWrite(in4,LOW);
     
      digitalWrite(buzzer,LOW);
      delay(1000);
      digitalWrite(buzzer,HIGH);      
      e=e+1;
      j=j+1;}
      else if(e==4){                  
      digitalWrite(in1,LOW);
      digitalWrite(in2,LOW);
      digitalWrite(in3,LOW);
      digitalWrite(in4,LOW);
      
      digitalWrite(buzzer,LOW);
      delay(5000);
      digitalWrite(buzzer,HIGH);
      digitalWrite(in1,LOW);
      digitalWrite(in2,LOW);
      digitalWrite(in3,LOW);
      digitalWrite(in4,LOW);
      delay(10000);    
      e=e+1;   }      
     }}
     digitalWrite(buzzer,HIGH);
  // or else to move straight    
  l_1,l_2=straight();
     
      
    }
      
    
    
    
}
