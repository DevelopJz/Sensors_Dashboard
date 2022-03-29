# Python3 Project_4
## Sensors_Dashboard

### 사용 언어
**Python 3.7.6**  
**Arduino 1.8.13**  

### 사용 환경
**Ubuntu 18.04 LTS**  
**Windows 10**  

### 라이브러리
 - Python (Raspberry pi)  
   - pyserial  
   - time  
   - datetime  
   - os  
   - csv  
   - socket  
   - matplotlib  
   - pickle  
   - smtplib  
   - email  

 - Python (Windows)  
   - tkinter  
   - matplotlib  
   - time  
   - csv  
   - datetime  
   - socket  
   - os,sys  
   - pickle  
   - time  
 
 - Arduino  
   - DHT.h  
   - SPI.h  
   - Adafruit_MAX31855.h  

### 라이브러리 설치
**Python**  

```python

python -m pip install 라이브러리명

```

**Arduino**  

필요한 라이브러리 인터넷 검색 후 zip 파일 다운로드  

C:\Users\사용자명\Documents\Arduino\libraries 에 zip 파일 저장  

zip 파일 불러오기  
![image](https://user-images.githubusercontent.com/96412126/159386813-feac94ca-6859-458a-b36c-97582c2fd0cd.png)

C:\Users\사용자명\Documents\Arduino\libraries 에서 다운로드한 zip 파일 선택  

### 동작 개요

arduino : 각 센서 값 읽어 Raspberry pi 에 전송

Raspberry pi : 전송받은 센서 값 측정 시간에 맞춰서 기록, 

PC : 

![image](https://user-images.githubusercontent.com/96412126/160563672-f853f8d4-1cea-48b0-be82-877f80174f85.png)


### 코드 설명  

**Sensor.ino**  

온/습도 센서 : 테스트 장비 환경의 온도/습도 측정  
가속도 센서 : 테스트 장비의 동작 시 진동 측정  
포토 센서 : 테스트 장비의 동작 횟수 측정  
열전대 센서 : 테스트 장비의 모터 온도 측정  
Serial 통신으로 Raspberry pi 에 각 센서값 전송  

**Rasp_Data.py**  

테스트 장비 동작하는 동안 전송받은 데이터 csv, 그래프 파일 저장  
email : 테스트 장비 동작 정지 및 테스트 종료 후 csv, 그래프 파일 email로 사무실의 pc에 전송, 하루 치 측정 데이터 확인 가능  
TCP/IP : 클라이언트가 접속했을 때 각 센서 값, 측정 시간 클라이언트로 전송  

**win_GUI.py**  

TCP/IP : Raspberry pi 에 접속하여 각 센서 값, 측정 시간 전송받고 GUI에 표시  
접속한 순간부터 GUI 데이터 기록  

GUI
 - DashBoard : 
 - Graph : 
