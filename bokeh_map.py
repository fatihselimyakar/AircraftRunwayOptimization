from tkinter import *
from tkinter import messagebox as tkMessageBox
from bokeh.io import output_file, show
from bokeh.models import GeoJSONDataSource
from bokeh.plotting import figure
from bokeh.sampledata.sample_geojson import geojson
import numpy as np
from bokeh.models import HoverTool,LabelSet,ColumnDataSource
from bokeh.tile_providers import get_provider,Vendors
from random import seed,random,randint
from datetime import datetime
import time
import algorithms

def buttonRun(entry1,entry2):
    algorithmName=entry1.get()
    algorithmDataSamp=int(entry2.get())
    if(algorithmName == '' or algorithmDataSamp == ''):
        tkMessageBox.showerror("Hata","Boş bir hücre var!")
    else:
        runMap(algorithmName,algorithmDataSamp)
        tkMessageBox.showinfo("Bilgi","Çalışma Tamamlandı.")

def tkinterRun():
    try:
        master = Tk() 
        Label(master, text='Algoritma İsmi:').grid(row=0) 
        Label(master, text='Hangi Veri Örneği?:').grid(row=1)
        e1 = Entry(master) 
        e2 = Entry(master) 
        e1.grid(row=0, column=1) 
        e2.grid(row=1, column=1) 
        master.title('Hava Trafik Kontrol Algoritma Programı') 
        button = Button(master,text='ÇALIŞTIR',fg='green',bg='yellow',command=lambda: buttonRun(e1,e2))
        button.grid(row=5,column=1)
        mainloop() 
    except:
        tkMessageBox.showerror("Hata","Bir hata oluştu!")



def wgs84_to_web_mercator(df, longtitude="long", latitude="lat"):
    k = 6378137
    df["x"] = df[longtitude] * (k * np.pi/180.0)
    df["y"] = np.log(np.tan((90 + df[latitude]) * np.pi/360.0)) * k
    return df

#point
def wgs84_web_mercator_point(longtitude,latitude):
    k = 6378137
    x= longtitude * (k * np.pi/180.0)
    y= np.log(np.tan((90 + latitude) * np.pi/360.0)) * k
    return x,y

def randBetweenFloats(lowerBound,upperBound):
    return lowerBound+((upperBound-lowerBound)*random())

def runMap(algorithmName,algorithmDataSamp):
    #Coordinate variables
    min_latitude,min_longtitude=40.01384,27.94966
    max_latitude,max_longtitude=42.01384,29.94966

    xy_min=wgs84_web_mercator_point(min_longtitude,min_latitude)
    xy_max=wgs84_web_mercator_point(max_longtitude,max_latitude)

    x_range,y_range=([xy_min[0],xy_max[0]], [xy_min[1],xy_max[1]])

    retVal=[]
    if(algorithmName=="GA"):
        retVal=algorithms.runGA(algorithmDataSamp)
    elif(algorithmName=="MRaatcsr"):
        retVal=algorithms.runMetaRaps(algorithmDataSamp,0)
    elif(algorithmName=="MRfpi"):
        retVal=algorithms.runMetaRaps(algorithmDataSamp,1)
    elif(algorithmName=="MRert"):
        retVal=algorithms.runMetaRaps(algorithmDataSamp,2)
    elif(algorithmName=="SAaatcsr"):
        retVal=algorithms.runSA(algorithmDataSamp,0)
    elif(algorithmName=="SAfpi"):
        retVal=algorithms.runSA(algorithmDataSamp,1)
    elif(algorithmName=="SAert"):
        retVal=algorithms.runSA(algorithmDataSamp,2)
    elif(algorithmName=="AATCSR"):
        retVal=algorithms.runAATCSR(algorithmDataSamp)
    elif(algorithmName=="FPI"):
        retVal=algorithms.runFPI(algorithmDataSamp)
    elif(algorithmName=="ERT"):
        retVal=algorithms.runERT(algorithmDataSamp)
    else:
        exit()

    x_array=[]
    y_array=[]
    aircraft=[]
    objFunc=[]
    startTime=[]
    indexes=[]
    for i in range(len(retVal[1])):
        x_array.append(randBetweenFloats(x_range[0],x_range[1]))
        y_array.append(randBetweenFloats(y_range[0],y_range[1]))
        aircraft.append('Uçak'+str(retVal[1][i]))
        startTime.append(retVal[2][i])
        objFunc.append(retVal[0])
        indexes.append(i)


    source = ColumnDataSource(
        data=dict(lat=x_array,
                lon=y_array,
                callsign=aircraft,
                order=indexes,
                startTime=startTime,
                objective=objFunc)
    )


    p=figure(x_range=x_range,y_range=y_range,x_axis_type='mercator',y_axis_type='mercator',sizing_mode='scale_width',plot_height=300)
    tile_prov=get_provider(Vendors.STAMEN_TERRAIN)
    p.add_tile(tile_prov,level='image')
    #p.image_url( x='lat', y='lon',source=source,anchor='center',angle_units='deg',angle='rot_angle',h_units='screen',w_units='screen',w=40,h=40)
    p.circle('lat','lon',source=source,fill_color='blue',hover_color='yellow',size=10,fill_alpha=0.8,line_width=0)

    my_hover=HoverTool()
    my_hover.tooltips=[('Sıralama','@order'),('Başlama Zamanı','@startTime'),('Objektif Fonksiyon Değeri','@objective'),('Enlem','@lat'),('Boylam','@lon')]
    labels = LabelSet(x='lat', y='lon', text='callsign', level='glyph',x_offset=5, y_offset=5, source=source, render_mode='canvas',background_fill_color='white',text_font_size="10pt")
    p.add_tools(my_hover)
    p.add_layout(labels)

    show(p)

if __name__ == "__main__":
    seed(datetime.now())
    tkinterRun()
