import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tkinter import *
import tkinter.ttk as ttk
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
dt_now = datetime.datetime.now()
if(dt_now.month<10):
    dt_now="{0}0{1}{2}".format(dt_now.year,dt_now.month,dt_now.day)
else:
    dt_now="{0}{1}{2}".format(dt_now.year,dt_now.month,dt_now.day)
def get_pa_df():
    serviceKey='API Servicekey'
    startCreateDt=str(int(dt_now)-100)
    endCreateDt=dt_now
    url1='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey={0}&pageNo=1&numOfRows=10&startCreateDt={1}&endCreateDt={2}'.format(serviceKey,startCreateDt,endCreateDt)
    res = requests.get(url1)

    #요청한 xml을 불러오는거 
    soup = bs(res.text, 'lxml')
    items = soup.find_all('item')

    lst = []
    for y in items:
        l = {}
        for x in y:
            l[x.name] = x.text
        lst.append(l)
    
    # list를 dataframe으로 만들기
    df = pd.DataFrame(lst)
    #df.columns = df.columns.map(response)
    #df=df[['기준일','총확진자수','격리해제수','검사진행수','사망자수','치료중인환자수']]
    df=df[['statedt','decidecnt','clearcnt','accexamcnt','deathcnt','carecnt']]

    df['decidecnt']=df['decidecnt'].astype(int)
    df['dailydecidecnt']=(df.decidecnt-df.decidecnt.shift(-1)).fillna(0)
    df['dailydecidecnt']=df['dailydecidecnt'].astype(int)

    df['deathcnt']=df['deathcnt'].astype(int)
    df['dailydeathcnt']=(df.deathcnt-df.deathcnt.shift(-1)).fillna(0)
    df['dailydeathcnt']=df['dailydeathcnt'].astype(int)

    df['clearcnt']=df['clearcnt'].astype(int)
    df['dailyclearcnt']=(df.clearcnt-df.clearcnt.shift(-1)).fillna(0)
    df['dailyclearcnt']=df['dailyclearcnt'].astype(int)

    df['accexamcnt']=df['accexamcnt'].astype(int)
    df['dailyaccexamcnt']=(df.accexamcnt-df.accexamcnt.shift(-1)).fillna(0)
    df['dailyaccexamcnt']=df['dailyaccexamcnt'].astype(int)

    response ={
    'statedt':'기준일',
    'decidecnt':'확진자수',
    'clearcnt':'완치자수',
    'accexamcnt':'검사자수',
    'deathcnt':'사망자수',
    'carecnt':'치료중인환자수',
    'dailydecidecnt':'일일확진자수',
    'dailydeathcnt':'일일사망자수',
    'dailyclearcnt':'일일완치자수',
    'dailyaccexamcnt':'일일검사자수'
    }

    df.columns = df.columns.map(response)
    df=df[::-1]
    df
    return df
def get_vac_df():
    url1='https://nip.kdca.go.kr/irgd/cov19stats.do?list=all'
    res = requests.get(url1)

    #요청한 xml을 불러오는거 
    soup = bs(res.text, 'lxml')
    items = soup.find_all('item')

    lst = []
    for y in items:
        l={}
        l[y.find('tpcd').text+" 1차"]=y.find('firstcnt').text
        l[y.find('tpcd').text+" 2차"]=y.find('secondcnt').text
        lst.append(l)
        
    # list를 dataframe으로 만들기
    df = pd.DataFrame(lst)
    df.iloc[0][2]=df.iloc[1][2]
    df.iloc[0][3]=df.iloc[1][3]
    df.iloc[0][4]=df.iloc[2][4]
    df.iloc[0][5]=df.iloc[2][5]
    df=df.drop(index=[1,2],axis=0)

    #df 값 int로 변환
    df['당일실적(A) 1차']=df['당일실적(A) 1차'].astype(int)
    df['당일실적(A) 2차']=df['당일실적(A) 2차'].astype(int)
    df['전일누적(B) 1차']=df['전일누적(B) 1차'].astype(int)
    df['전일누적(B) 2차']=df['전일누적(B) 2차'].astype(int)
    df['전체건수(C): (A)+(B) 1차']=df['전체건수(C): (A)+(B) 1차'].astype(int)
    df['전체건수(C): (A)+(B) 2차']=df['전체건수(C): (A)+(B) 2차'].astype(int)
    
    return df
covid_df=get_pa_df()
vac_df=get_vac_df()
root=Tk()
root.title("Covid19 LIVE")
root.geometry("700x750+400+10")
#root.resizable(False,False)
#root.configure(bg="#FAFAFA")
Label(root,text="",pady=1).pack()
Label(root,text="Covid19 LIVE",font=("경기천년제목 Bold",15)).pack(side="top")

Label(root,text="",pady=1).pack()
now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d')
Label(root,text="{0} 기준".format(today),font=("경기천년제목 Bold",10),anchor="w").pack()

Label(root,text="Copyright 2021.Cochonsy All Rights Reserved.").pack(side="bottom")
Label(root,text="",pady=1).pack()

frame_today=Frame(root,background="#FFFFFF",highlightthickness=2,highlightbackground="#CCCCCC")
frame_today.pack()
Label(frame_today,text="확진자",width=15,bg="#FFFFFF").grid(row=0,column=0)
Label(frame_today,text="사망자",width=15,bg="#FFFFFF").grid(row=0,column=1)
Label(frame_today,text="완치자",width=15,bg="#FFFFFF").grid(row=0,column=2)
Label(frame_today,text="검사자",width=15,bg="#FFFFFF").grid(row=0,column=3)
Label(frame_today,text="1차백신접종자",width=15,bg="#FFFFFF").grid(row=0,column=4)
Label(frame_today,text="2차백신접종자",width=15,bg="#FFFFFF").grid(row=0,column=5)

Label(frame_today,text=format(covid_df.at[0,'확진자수'],","),width=15,pady=5,fg="#EB6F8F",bg="#FFFFFF").grid(row=1,column=0)
Label(frame_today,text=format(covid_df.at[0,'사망자수'],","),width=15,pady=5,fg="#5C5C5A",bg="#FFFFFF").grid(row=1,column=1)
Label(frame_today,text=format(covid_df.at[0,'완치자수'],","),width=15,pady=5,fg="#5B8E04",bg="#FFFFFF").grid(row=1,column=2)
Label(frame_today,text=format(covid_df.at[0,'검사자수'],","),width=15,pady=5,fg="#727AEA",bg="#FFFFFF").grid(row=1,column=3)
Label(frame_today,text=str(round(vac_df.at[0,'전체건수(C): (A)+(B) 1차']/51821669*100,2))+"%",width=15,pady=5,fg="#5C5C5A",bg="#FFFFFF").grid(row=1,column=4)
Label(frame_today,text=str(round(vac_df.at[0,'전체건수(C): (A)+(B) 2차']/51821669*100,2))+"%",width=15,pady=5,fg="#5C5C5A",bg="#FFFFFF").grid(row=1,column=5)

Label(frame_today,text=format(covid_df.at[0,'일일확진자수'],",")+" ↑",width=15,pady=5,fg="#EB6F8F",bg="#FDEEF1").grid(row=2,column=0)
Label(frame_today,text=format(covid_df.at[0,'일일사망자수'],",")+" ↑",width=15,pady=5,fg="#5C5C5A",bg="#F7F7F7").grid(row=2,column=1)
Label(frame_today,text=format(covid_df.at[0,'일일완치자수'],",")+" ↑",width=15,pady=5,fg="#5B8E04",bg="#E1F4E1").grid(row=2,column=2)
Label(frame_today,text=format(covid_df.at[0,'일일검사자수'],",")+" ↑",width=15,pady=5,fg="#727AEA",bg="#F2F5FF").grid(row=2,column=3)
Label(frame_today,text=format(vac_df.at[0,'당일실적(A) 1차'],",")+" ↑",width=15,pady=5,fg="#5C5C5A",bg="#F7F7F7").grid(row=2,column=4)
Label(frame_today,text=format(vac_df.at[0,'당일실적(A) 2차'],",")+" ↑",width=15,pady=5,fg="#5C5C5A",bg="#F7F7F7").grid(row=2,column=5)


Label(root,text="",pady=2).pack()

lbl=Label(root,text="COVID 추세",pady=2,font=("맑은고딕",10)).pack()
frame_dailydecidecnt=Frame(root,background="#FFFFFF",highlightthickness=2,highlightbackground="#CCCCCC")
frame_dailydecidecnt.pack()
values=['확진자','사망자','완치자','검사자']
combobox_graph=ttk.Combobox(frame_dailydecidecnt,height=5,values=values)
combobox_graph.grid(row=0,column=0)
combobox_graph.set("그래프 선택")
frame_daily=Frame(root,background="#FFFFFF",highlightthickness=2,highlightbackground="#CCCCCC")
frame_daily.pack()

mpl.rcParams['font.family'] ='Malgun Gothic'
mpl.rcParams['axes.unicode_minus'] =False

#도표생성
figure_daily=plt.Figure(figsize=(8,6),dpi=50)

ax_daily=figure_daily.add_subplot(111)
line_daily=FigureCanvasTkAgg(figure_daily,root)
line_daily.get_tk_widget().pack()

covid_df1=covid_df[['기준일','일일확진자수']].groupby('기준일').sum()
covid_df1.plot(kind='line',legend=True,ax=ax_daily,color='r',marker='o',fontsize=10)

ax_daily.set_title('일일확진자수 추이')
plt.show()

def btn_graph_cmd():
    get=combobox_graph.get()
    if(get=="확진자"):
        ax_daily.clear()
        covid_df1=covid_df[['기준일','일일확진자수']].groupby('기준일').sum()
        covid_df1.plot(kind='line',legend=True,ax=ax_daily,color='r',marker='o',fontsize=10)
        ax_daily.set_title('일일확진자수 추이')
        plt.show()
        
    elif(get=="사망자"):
        ax_daily.clear()
        covid_df1=covid_df[['기준일','일일사망자수']].groupby('기준일').sum()
        covid_df1.plot(kind='line',legend=True,ax=ax_daily,color='r',marker='o',fontsize=10)
        ax_daily.set_title('일일사망자수 추이')
        plt.show()

    elif(get=="완치자"):
        ax_daily.clear()
        covid_df1=covid_df[['기준일','일일완치자수']].groupby('기준일').sum()
        covid_df1.plot(kind='line',legend=True,ax=ax_daily,color='r',marker='o',fontsize=10)
        ax_daily.set_title('일일완치자수 추이')
        plt.show()

    elif(get=="검사자"):
        ax_daily.clear()
        covid_df1=covid_df[['기준일','일일검사자수']].groupby('기준일').sum()
        covid_df1.plot(kind='line',legend=True,ax=ax_daily,color='r',marker='o',fontsize=10)
        ax_daily.set_title('일일검사자수 추이')
        plt.show()
btn_graph=Button(frame_dailydecidecnt,text="선택",height=1,width=10,command=btn_graph_cmd)
btn_graph.grid(row=0,column=1)
root.mainloop()