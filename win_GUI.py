#-----------------------------------------------------------------------------
#Library

import tkinter as tk
import tkinter.ttk
import tkinter.font
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.style as mplstyle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import csv
import datetime
import socket
import os,sys
import pickle
import time

#-----------------------------------------------------------------------------
#Variable

t=0
x_start=0
x_end=300
stime=0
stemp=0
shumi=0
smemp=0
sxval=0
syval=0
szval=0
svibe=0
scount=0
last=0
c=""

timelist=[]
templist=[]
humilist=[]
memplist=[]
xvallist=[]
yvallist=[]
zvallist=[]
vibelist=[]
countlist=[]
timlist=[]

HOST="127.0.0.1"
PORT=8070

client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))
datenow=datetime.datetime.now()
path="./ProJect"

#-----------------------------------------------------------------------------
#Flag

connectflag=0
realconnect=0
tempwarn=0
humiwarn=0
vibewarn=0
mtempwarn=0
tcpflag=0
done=0
timeflag=0
lastflag=0

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

#-----------------------------------------------------------------------------
#GUI

fig=plt.figure(figsize=(16,8))

root=tk.Tk()
root.title("Client Dash Board GUI")
root.geometry("1600x900+100+50")
root.resizable(False,False)

valuefont=tk.font.Font(family="맑은 고딕", size=50)
namefont=tk.font.Font(family="맑은 고딕", size=30)

tabframe=tk.Frame(root)
tabframe.pack(side="top",fill="both",expand=True)

notebook=tk.ttk.Notebook(tabframe)
notebook.pack(side="left",fill="both",expand=True)

##----------------------------------------------------------------------------
#DashBoard Tab

tab1=tk.Frame(tabframe)
notebook.add(tab1,text="DASH BOARD")

###---------------------------------------------------------------------------
#Temperature & Humidity Frame

titleframe=tk.Frame(tab1,bg="light green")
titleframe.pack(side="top",fill="both",expand=True)

titlelabel=tk.Label(titleframe,text="테스트 장비",bg="light green",fg="white",font=namefont)
titlelabel.pack()

tnhframe=tk.Frame(tab1,bg="white")
tnhframe.pack(side="top",fill="both",expand=True)

####---------------------------------------------------------------------------
#Temperature Board

tempframe=tk.Frame(tnhframe,bg="#4e4e4e",relief="solid",bd=1)
tempframe.pack(side="left",fill="both",expand=True)

templabel=tk.Label(tempframe,text="대기 온도",bg="#4e4e4e",fg="white",font=namefont)
templabel.pack()

def tempval():
    global stemp,tempwarn
    temp=stemp
    tempscale.set(temp)
    tvaluelabel.config(text=str(stemp)+" °C")
    if temp<-10:
        tvaluelabel.config(fg="blue")
        tempscale.config(bg="blue")
    elif temp<5 and temp>=-10:
        tvaluelabel.config(fg="light blue")
        tempscale.config(bg="light blue")
    elif temp<20 and temp>=5:
        tvaluelabel.config(fg="light green")
        tempscale.config(bg="light green")
    elif temp<30 and temp>=20:
        tvaluelabel.config(fg="orange")
        tempscale.config(bg="orange")
    else:
        tvaluelabel.config(fg="red")
        tempscale.config(bg="red")
        consolelabel.config(text=" Console : Temperature Warning!")
        tempwarn=1
    pass

tempvar=tk.StringVar()
tempscale=tk.Scale(tempframe,variable=tempvar,command=tempval,
                   orient="horizontal",showvalue=False,width=50,
                   tickinterval=10,from_=-40,to=40,length=600,
                   relief="solid",sliderrelief="solid",bd=1,bg="light blue",
                   troughcolor="white",activebackground="white",highlightbackground="white")
tempscale.pack()

tvaluelabel=tk.Label(tempframe,text="0 °C",font=valuefont,fg="light blue",bg="#4e4e4e")
tvaluelabel.pack()

####---------------------------------------------------------------------------
#Humidity Board

humidityframe=tk.Frame(tnhframe,bg="#4e4e4e",relief="solid",bd=1)
humidityframe.pack(side="left",fill="both",expand=True)

humilabel=tk.Label(humidityframe,text="습도",bg="#4e4e4e",fg="white",font=namefont)
humilabel.pack()

def humival():
    global shumi,humiwarn
    humi=shumi
    humiscale.set(humi)
    hvaluelabel.config(text=str(shumi)+" %")
    if humi<68:
        hvaluelabel.config(fg="light green")
        humiscale.config(bg="light green")
    elif humi<75 and humi>=65:
        hvaluelabel.config(fg="yellow")
        humiscale.config(bg="yellow")
    elif humi<80 and humi>=75:
        hvaluelabel.config(fg="orange")
        humiscale.config(bg="orange")
    else:
        hvaluelabel.config(fg="red")
        humiscale.config(bg="red")
        consolelabel.config(text=" Console : Humidity Warning!")
        humiwarn=1
    pass

humivar=tk.StringVar()
humiscale=tk.Scale(humidityframe,variable=humivar,command=humival,
                   orient="horizontal",showvalue=False,width=50,
                   tickinterval=10,from_=0,to=100,length=600,
                   relief="solid",sliderrelief="solid",bd=1,bg="light green",
                   troughcolor="white")
humiscale.pack()

hvaluelabel=tk.Label(humidityframe,text="0 %",font=valuefont,fg="light green",bg="#4e4e4e")
hvaluelabel.pack()

###---------------------------------------------------------------------------
#Vibration & Motor Temperature Frame

vnmtframe=tk.Frame(tab1,bg="white")
vnmtframe.pack(side="top",fill="both",expand=True)

####---------------------------------------------------------------------------
#Vibration Board

vibrationframe=tk.Frame(vnmtframe,bg="#4e4e4e",relief="solid",bd=1)
vibrationframe.pack(side="right",fill="both",expand=True)

vibelabel=tk.Label(vibrationframe,text="진동",bg="#4e4e4e",fg="white",font=namefont)
vibelabel.pack()

def vibeval():
    global svibe,vibewarn
    vibe=svibe
    vibescale.set(vibe)
    vvaluelabel.config(text=str(svibe)+" mm/s^2")
    if vibe<300:
        vvaluelabel.config(fg="light green")
        vibescale.config(bg="light green")
    elif vibe<600 and vibe>=300:
        vvaluelabel.config(fg="yellow")
        vibescale.config(bg="yellow")
    elif vibe<800 and vibe>=600:
        vvaluelabel.config(fg="orange")
        vibescale.config(bg="orange")
    else:
        vvaluelabel.config(fg="red")
        vibescale.config(bg="red")
        consolelabel.config(text=" Console : Vibration Warning!")
        vibewarn=1
    pass

vibevar=tk.StringVar()
vibescale=tk.Scale(vibrationframe,variable=vibevar,command=vibeval,
                   orient="horizontal",showvalue=False,width=50,
                   tickinterval=100,from_=0,to=1000,length=600,
                   relief="solid",sliderrelief="solid",bd=1,bg="light green",
                   troughcolor="white")
vibescale.pack()

vvaluelabel=tk.Label(vibrationframe,text="0 mm/s^2",font=valuefont,fg="light green",bg="#4e4e4e")
vvaluelabel.pack()

####---------------------------------------------------------------------------
#Motor Temperature Board

motortempframe=tk.Frame(vnmtframe,bg="#4e4e4e",relief="solid",bd=1)
motortempframe.pack(side="right",fill="both",expand=True)

memplabel=tk.Label(motortempframe,text="모터 온도",bg="#4e4e4e",fg="white",font=namefont)
memplabel.pack()

def mempval():
    global smemp,mtempwarn
    memp=smemp
    mempscale.set(memp)
    mvaluelabel.config(text=str(smemp)+" °C")
    if memp<0:
        mvaluelabel.config(fg="blue")
        mempscale.config(bg="blue")
    elif memp<25 and memp>=0:
        mvaluelabel.config(fg="light blue")
        mempscale.config(bg="light blue")
    elif memp<80 and memp>=25:
        mvaluelabel.config(fg="light green")
        mempscale.config(bg="light green")
    elif memp<100 and memp>=80:
        mvaluelabel.config(fg="orange")
        mempscale.config(bg="orange")
    else:
        mvaluelabel.config(fg="red")
        mempscale.config(bg="red")
        consolelabel.config(text=" Console : Motor Temperature Warning!")
        mtempwarn=1
    pass

mempvar=tk.StringVar()
mempscale=tk.Scale(motortempframe,variable=mempvar,command=mempval,
                   orient="horizontal",showvalue=False,width=50,
                   tickinterval=10,from_=-20,to=120,length=600,
                   relief="solid",sliderrelief="solid",bd=1,bg="light blue",
                   troughcolor="white")
mempscale.pack()

mvaluelabel=tk.Label(motortempframe,text="0 °C",font=valuefont,fg="light blue",bg="#4e4e4e")
mvaluelabel.pack()

###---------------------------------------------------------------------------
#Count Frame

countframe=tk.Frame(tab1,bg="black")
countframe.pack(side="bottom",fill="both",expand=True)

####--------------------------------------------------------------------------
#Last Count Frame

lastcountframe=tk.Frame(countframe,bg="white")
lastcountframe.pack(side="left",fill="both",expand=True)

lastlabel=tk.Label(lastcountframe,text=" 이전 총 횟수 : 0",font=namefont,bg="white")
lastlabel.pack(anchor="center",fill="both",expand=True)

####--------------------------------------------------------------------------
#Now Count Frame

nowcountframe=tk.Frame(countframe,bg="white")
nowcountframe.pack(side="left",fill="both",expand=True)

nowlabel=tk.Label(nowcountframe,text=" 현재 횟수 : 0",font=namefont,bg="white")
nowlabel.pack(anchor="center",fill="both",expand=True)

####--------------------------------------------------------------------------
#Total Count Frame

totalcountframe=tk.Frame(countframe,bg="white")
totalcountframe.pack(side="right",fill="both",expand=True)

totallabel=tk.Label(totalcountframe,text=" 전체 횟수 : 0",font=namefont,bg="white")
totallabel.pack(anchor="center",fill="both",expand=True)

##----------------------------------------------------------------------------
#Graph Tab

tab2=tk.Frame(tabframe)
notebook.add(tab2,text="GRAPH")

graphframe=tkinter.Frame(tab2,relief="solid",bd=2)
graphframe.pack(fill="both",expand=True)

canvas=FigureCanvasTkAgg(fig, master=graphframe)
canvas.get_tk_widget().pack(fill="both", expand=True)

mpl.rcParams['path.simplify']=True
mpl.rcParams['path.simplify_threshold']=1.0
mpl.rcParams['agg.path.chunksize']=10000
mplstyle.use('fast')

tempax=plt.subplot(411)
plt.subplots_adjust(hspace=0.45,top=0.96)
tline,=tempax.plot([],lw=2,color="green",label="Temperature")
tempax.set_xlabel("Time (s)")
tempax.set_ylabel("Temperature (°C)")
tempax.set_title("Temperature Graph")
tempax.set_xlim(x_start,x_end)
tempax.set_ylim(-42,42)
tempax.legend(loc="upper left")

humiax=plt.subplot(412)
plt.subplots_adjust(hspace=0.45)
hline,=humiax.plot([],lw=2,color="blue",label="Humidity")
humiax.set_xlabel("Time (s)")
humiax.set_ylabel("Humidity (%)")
humiax.set_title("Humidity Graph")
humiax.set_xlim(x_start,x_end)
humiax.set_ylim(-2,102)
humiax.legend(loc="upper left")

vibeax=plt.subplot(413)
plt.subplots_adjust(hspace=0.45)
vxline,=vibeax.plot([],lw=2,color="magenta",label="X value")
vyline,=vibeax.plot([],lw=2,color="yellow",label="Y value")
vzline,=vibeax.plot([],lw=2,color="cyan",label="Z value")
vline,=vibeax.plot([],lw=2,color="black",label="Total value")
vibeax.set_xlabel("Time (s)")
vibeax.set_ylabel("Acceleration (mm/s^2)")
vibeax.set_title("Vibration Graph")
vibeax.set_xlim(x_start,x_end)
vibeax.set_ylim(0,1100)
vibeax.legend(loc="upper left")

mtempax=plt.subplot(414)
plt.subplots_adjust(hspace=0.45,bottom=0.05)
mtline,=mtempax.plot([],lw=2,color="red",label="Motor Temperature")
mtempax.set_xlabel("Time (s)")
mtempax.set_ylabel("Motor Temperature (°C)")
mtempax.set_title("Motor Temperature Graph")
mtempax.set_xlim(x_start,x_end)
mtempax.set_ylim(-22,122)
mtempax.legend(loc="upper left")

fig.canvas.draw()

tempaxbg=fig.canvas.copy_from_bbox(tempax.bbox)
humiaxbg=fig.canvas.copy_from_bbox(humiax.bbox)
vibeaxbg=fig.canvas.copy_from_bbox(vibeax.bbox)
mtempaxbg=fig.canvas.copy_from_bbox(mtempax.bbox)

###---------------------------------------------------------------------------
#Graph Input

def realgraph():
    global t,stime,timeflag,x_start,x_end,timelist,templist,humilist,memplist,xvallist,yvallist,zvallist,vibelist,countlist,timlist,t
    if t>x_end:
        x_start=x_start+1
        x_end=x_end+1
        tempax.set_xlim(x_start,x_end)
        humiax.set_xlim(x_start,x_end)
        vibeax.set_xlim(x_start,x_end)
        mtempax.set_xlim(x_start,x_end)
    
    fig.canvas.draw()
    
    tline.set_data(timlist,templist)
    hline.set_data(timlist,humilist)
    vxline.set_data(timlist,xvallist)
    vyline.set_data(timlist,yvallist)
    vzline.set_data(timlist,zvallist)
    vline.set_data(timlist,vibelist)
    mtline.set_data(timlist,memplist)
    
    fig.canvas.flush_events()
    pass

#-----------------------------------------------------------------------------
#TCP/IP & Serial

def Decode(A):
    global done,stime,stemp,shumi,smemp,sxval,syval,szval,svibe,scount
    A=A.decode()
    A=A.replace("\n","")
    if A=="":
        done=1
        pass
    else:
        try:
            tindex=A.find("B")
            hindex=A.find("C")
            mtindex=A.find("D")
            xindex=A.find("E")
            yindex=A.find("F")
            zindex=A.find("G")
            vindex=A.find("H")
            pindex=A.find("I")
            endindex=A.find("J")
            t=float(A[:tindex])
            temp=float(A[tindex+1:hindex])
            humi=float(A[hindex+1:mtindex])
            memp=float(A[mtindex+1:xindex])
            xval=float(A[xindex+1:yindex])
            yval=float(A[yindex+1:zindex])
            zval=float(A[zindex+1:vindex])
            vibe=float(A[vindex+1:pindex])
            count=float(A[pindex+1:endindex])
        except ValueError:
            print("value error")
            return stime,stemp,shumi,smemp,sxval,syval,szval,svibe,scount
        return t,temp,humi,memp,xval,yval,zval,vibe,count

def recvdata(size,client):
    tempdata=b""
    while True:
        data=client.recv(size)
        if not data:
            break
        tempdata+=data
    cmd=pickle.loads(tempdata)
    return cmd

def tcpip(size):
    global stime,stemp,shumi,smemp,sxval,syval,szval,svibe,scount,tcpflag,done,timelist,templist,humilist,memplist,xvallist,yvallist,zvallist,vibelist,countlist,last,lastflag,t,timlist,c
    if done==0:
        if tcpflag==0:
            c=client_socket.recv(1024)
            tcpflag=1
        else:
            data=client_socket.recv(1024)
            if not data:
                done=1
            stime,stemp,shumi,smemp,sxval,syval,szval,svibe,scount=Decode(data)
            timlist.append(t)
            timelist.append(stime)
            templist.append(stemp)
            humilist.append(shumi)
            memplist.append(smemp)
            xvallist.append(sxval)
            yvallist.append(syval)
            zvallist.append(szval)
            vibelist.append(svibe)
            countlist.append(scount)
            t=t+0.27
            tempval()
            humival()
            vibeval()
            mempval()
            lastlabel.config(text=" 이전 총 횟수 : "+str(c.decode()))
            nowlabel.config(text=" 현재 횟수 : "+str(int(scount-int(c.decode()))))
            totallabel.config(text=" 전체 횟수 : "+str(int(scount)))
            realgraph()
            time.sleep(0.001)
    pass

##----------------------------------------------------------------------------
#Console Frame

buttonframe=tk.Frame(root,bg="black")
buttonframe.pack(side="bottom",fill="x",expand=False)

def filemake():
    global timelist,templist,humilist,memplist,xvallist,yvallist,zvallist,vibelist,countlist
    timeend=datetime.datetime.now()
    if datenow.month<10:
        monthdat="0"+str(datenow.month)
    else:
        monthdat=str(datenow.month)
    if datenow.day<10:
        daydat="0"+str(datenow.day)
    else:
        daydat=str(datenow.day)
    with open(path+str(datenow.year)+"_"+monthdat+"_"+daydat+"/"+str(datenow.hour)+"_"+str(datenow.minute)+"_"+str(datenow.second)+"to"+str(timeend.hour)+"_"+str(timeend.minute)+"_"+str(timeend.second)+"_"+"Data.csv","w",newline="") as w:
        write=csv.writer(w)
        write.writerow(["Time","Temp","Humi","Motor Temp","XVal","YVal","ZVal","Vibe","Count"])
        for i in range(len(templist)):
            write.writerow([timelist[i],templist[i],humilist[i],memplist[i],xvallist[i],yvallist[i],zvallist[i],vibelist[i],countlist[i]])
    
    fig.tight_layout()
    fig.savefig(path+str(datenow.year)+"_"+monthdat+"_"+daydat+"/"+str(datenow.hour)+"_"+str(datenow.minute)+"_"+str(datenow.second)+"to"+str(timeend.hour)+"_"+str(timeend.minute)+"_"+str(timeend.second)+"_"+"Data.png")
    pass

def exitnsave():
    global done
    done=1
    consolelabel.config(text=" Console : Saving...")
    time.sleep(1)
    filemake()
    consolelabel.config(text=" Console : Exiting...")
    time.sleep(1)
    try:
        client_socket.shutdown(socket.SHUT_RDWR)
        root.destroy()
    except tkinter.TclError:
        pass
    pass

ensbutton=tk.Button(buttonframe,text="Exit & Save",command=exitnsave)
ensbutton.pack(side="right",fill="y",expand=False,anchor="e")

consolelabel=tk.Label(buttonframe,text=" Console : GUI On",fg="white",bg="black",height=2)
consolelabel.pack(side="left",fill="y",expand=True,anchor="w")

#-----------------------------------------------------------------------------

if __name__=="__main__":
    size=65535*100
    while True:
        if done==0:
            tcpip(size)
            pass
        else:
            consolelabel.config(text=" Console : Server Done, Click Exit & Save")
        root.update()
    
    client_socket.shutdown(socket.SHUT_RDWR)