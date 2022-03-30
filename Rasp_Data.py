from serial import Serial
import time
import datetime
import os
import csv
import socket
import matplotlib.pyplot as plt
import pickle
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

email_from="****@naver.com"
email_to="*****@company.co.kr"
email_id="****"
email_pass="**********"
datenow=datetime.datetime.now()

subject=str(datenow.year)+"/"+str(datenow.month)+"/"+str(datenow.day)+"_데이터 수집 결과파일"

msg=MIMEMultipart()
msg["from"]=email_from
msg["To"]=email_to
msg["Subject"]=subject
sendfile=[]

body="테스트용 대시보드 수집 데이터"
msg.attach(MIMEText(body,"plain"))

def mailsend(name1,name2):
    global sendfile
    sendfile.append(name1)
    sendfile.append(name2)
    for f in sendfile:
        attachment=open(f,"rb")
        part=MIMEBase("application","octet-stream")
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition","attachment; filename="+os.path.basename(f))
        msg.attach(part)
    
    text=msg.as_string()
    server=smtplib.SMTP("smtp.naver.com",587)
    server.starttls()
    server.login(email_id,email_pass)
    
    server.sendmail(email_from,email_to,text)
    server.quit()

HOST="127.0.0.1"
PORT=8070

stemp=0
shumi=0
smemp=0
sxval=0
syval=0
szval=0
vibe=0
sphoto=0
scount=0
end=0
first=0
x_start=0
x_end=300
t=0
lastcount=""

inflag=0
connectflag=0
realconnect=0
tempwarn=0
humiwarn=0
vibewarn=0
mtempwarn=0
filesave=0
tcpflag=0
conflag=0
onflag=0

searchtime=[]
foldlist=[]
lastflist=[]
timelist=[]
vibelist=[]
templist=[]
humilist=[]
memplist=[]
xvallist=[]
yvallist=[]
zvallist=[]
countlist=[]
senddata=[]

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind((HOST,PORT))


path="/home/pi/Downloads/ProJect/DATA/"
dirs=os.listdir(path)
mega=Serial(port="/dev/ttyACM0",baudrate=9600,)

while True:
    if datenow.month<10:
        monthdat="0"+str(datenow.month)
    else:
        monthdat=str(datenow.month)
    if datenow.day<10:
        daydat="0"+str(datenow.day)
    else:
        daydat=str(datenow.day)
    if not os.path.isdir(path+str(datenow.year)+"_"+str(monthdat)+"_"+str(daydat)):
        os.mkdir(path+str(datenow.year)+"_"+str(monthdat)+"_"+str(daydat))
    else:
        break

def Decode(A):
    A=A.decode()
    hindex=A.find("B")
    mtindex=A.find("C")
    pindex=A.find("D")
    xindex=A.find("E")
    yindex=A.find("F")
    zindex=A.find("G")
    endindex=A.find("H")
    temp=float(A[:hindex])
    humi=float(A[hindex+1:mtindex])
    memp=float(A[mtindex+1:pindex])
    photo=float(A[pindex+1:xindex])
    xval=float(A[xindex+1:yindex])
    yval=float(A[yindex+1:zindex])
    zval=float(A[zindex+1:endindex])
    return temp,humi,memp,photo,xval,yval,zval
    pass
    

def Ardread():
    global stemp,shumi,smemp,sphoto,sxval,syval,szval
    if mega.readable():
        try:
            res=mega.readline()
            code=Decode(res)
        except ValueError:
            code=stemp,shumi,smemp,sphoto,sxval,syval,szval
        return code
    else:
        print("Read Error (Ardread)")

def filemake():
    global searchtime,templist,humilist,memplist,xvallist,yvallist,zvallist,vibeist,countlist
    fig=plt.figure(figsize=(24,14))
    if datenow.month<10:
        monthdat="0"+str(datenow.month)
    else:
        monthdat=str(datenow.month)
    if datenow.day<10:
        daydat="0"+str(datenow.day)
    else:
        daydat=str(datenow.day)
    with open(path+str(datenow.year)+"_"+monthdat+"_"+daydat+"/Data.csv","w",newline="") as w:
        write=csv.writer(w)
        write.writerow(["Time","Temp","Humi","Motor Temp","XVal","YVal","ZVal","Vibe","Count"])
        for i in range(len(templist)):
            write.writerow([searchtime[i],templist[i],humilist[i],memplist[i],xvallist[i],yvallist[i],zvallist[i],vibelist[i],countlist[i]])
    
    plt.subplot(411)
    plt.subplots_adjust(hspace=0.45,top=0.96)
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Graph")
    plt.xlim(0,timelist[-1])
    plt.ylim(-42,42)
    plt.plot(timelist,templist,color="green",label="Temperature")
    plt.legend(loc="upper left")
    
    plt.subplot(412)
    plt.subplots_adjust(hspace=0.45)
    plt.xlabel("Time (s)")
    plt.ylabel("Humidity (%)")
    plt.title("Humidity Graph")
    plt.xlim(0,timelist[-1])
    plt.ylim(-2,102)
    plt.plot(timelist,humilist,color="blue",label="Humidity")
    plt.legend(loc="upper left")
    
    plt.subplot(413)
    plt.subplots_adjust(hspace=0.45)
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (mm/s^2)")
    plt.title("Vibration Graph")
    plt.xlim(0,timelist[-1])
    plt.ylim(0,1100)
    plt.plot(timelist,zvallist,color="cyan",label="Z Value")
    plt.plot(timelist,yvallist,color="yellow",label="Y Value")
    plt.plot(timelist,xvallist,color="magenta",label="X Value")
    plt.plot(timelist,vibelist,color="black",label="Total Value")
    plt.legend(loc="upper left")
    
    plt.subplot(414)
    plt.subplots_adjust(hspace=0.45,bottom=0.05)
    plt.xlabel("Time (s)")
    plt.ylabel("Motor Temperature (°C)")
    plt.title("Motor Temperature Graph")
    plt.xlim(0,timelist[-1])
    plt.ylim(-22,122)
    plt.plot(timelist,memplist,color="red",label="Motor Temperature")
    plt.legend(loc="upper left")
    
    fig.tight_layout()
    fig.savefig(path+str(datenow.year)+"_"+monthdat+"_"+daydat+"/Data.png")
    pass

def fileread():
    global foldlist,lastflist, lastcount
    for file in dirs:
        foldlist.append(file)
        lastflist.append(file)
        
    for i in range(len(foldlist)):
        foldlist[i].replace("_","")
        foldlist[i]=int(foldlist[i])
    
    findindex=foldlist.index(max(foldlist))
    
    with open(path+lastflist[findindex]+"/Data.csv","r") as r:
        readcount=r.readlines()
        readcount=readcount[-1].replace("\n","").split(",")
        lastcount=readcount[-1]

def sendlist(cmd,client):
    data=pickle.dumps(cmd)
    client.sendall(data)

def waitclient():
    global conflag,client_socket,addr,onflag
    server_socket.settimeout(0.01)
    server_socket.listen(3)
    client_socket,addr=server_socket.accept()
    print("Connect")
    conflag=1
    pass

def tcpip():
    global addr,filesave,timelist,templist,humilist,memplist,xvallist,yvallist,zvallist,vibelist,countlist,senddata,tcpflag,conflag
    try:
        if tcpflag==0:
            c=str(countlist[0])
            client_socket.sendall(c.encode())
            tcpflag=1
        else:
            sendata=str(timelist[-1])+"B"+str(templist[-1])+"C"+str(humilist[-1])+"D"+str(memplist[-1])+"E"+str(xvallist[-1])+"F"+str(yvallist[-1])+"G"+str(zvallist[-1])+"H"+str(vibelist[-1])+"I"+str(countlist[-1])+"J"
            client_socket.sendall(sendata.encode())
    except ConnectionResetError:
        print("Connect Reset")
        conflag=0
        tcpflag=0
        client_socket.close()
        pass

def main():
    global inflag,searchtime,t,timelist,stemp,shumi,smemp,sxval,syval,szval,sphoto,scount,templist,humilist,memplist,xvallist,yvallist,zvallist,countlist,end,vibe,lastcount,senddata
    dateno=datetime.datetime.now()
    stemp,shumi,smemp,sphoto,sxval,syval,szval=Ardread()
    vibe=(sxval+syval+szval)//3
    searchtime.append(str(dateno.hour)+":"+str(dateno.minute)+":"+str(dateno.second))
    timelist.append(round(t,2))
    templist.append(round(stemp,2))
    humilist.append(round(shumi,2))
    memplist.append(round(smemp,2))
    xvallist.append(round(sxval,2))
    yvallist.append(round(syval,2))
    zvallist.append(round(szval,2))
    vibelist.append(round(vibe,2))
    if inflag==0:
        if sphoto==0:
            inflag=1
            scount=scount+1
        else:
            inflag=0
    elif inflag==1:
        if sphoto==0:
            inflag=1
        else:
            inflag=0
    countlist.append(int(lastcount)+scount)
    time.sleep(0.001)
    t=t+0.27
    

if __name__=="__main__":
    first=time.time()
    fileread()
    while True:
        if end-first<32700:
            if conflag==0:
                try:
                    waitclient()
                    main()
                    end=time.time()
                except OSError:
                    main()
                    print("waiting")
                    end=time.time()
                    continue
                except socket.timeout:
                    main()
                    print("waiting_timeout")
                    end=time.time()
                    continue
                except Exception as e:
                    main()
                    print("waiting_",e)
                    end=time.time()
                    continue
            else:
                print("Work")
                main()
                tcpip()
                end=time.time()
        else:
            filemake()
            mailsend(path+str(datenow.year)+"_"+monthdat+"_"+daydat+"/Data.csv",path+str(datenow.year)+"_"+monthdat+"_"+daydat+"/Data.png")
            print("Done")
            client_socket.shutdown(socket.SHUT_RDWR)
            server_socket.shutdown(socket.SHUT_RDWR)