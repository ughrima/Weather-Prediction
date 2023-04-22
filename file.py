import requests
import os
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import numpy as np
  
api_key="4fe7422487ca80a369fea7b428598217"
url="http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

# api_link=requests.get(completelink)
# api_dataa=api_link.json()

def getweather(city):
    result=requests.get(url.format(city,api_key))
    if result :
        api_dataa=result.json()
        country=api_dataa['sys']['country']
        temp_city=((api_dataa['main']["temp"])-273.15)
        weather_desc=api_dataa['weather'][0]['description']
        hmdt=api_dataa['main']['humidity']
        wind_speed=api_dataa['wind']['speed']
        icon=api_dataa['weather'][0]['icon']
        lon=api_dataa['coord']['lon']
        lat=api_dataa['coord']['lat']
        date_time=datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
        res=[country,round(temp_city,1),weather_desc,hmdt,wind_speed,
             icon,lon,lat,date_time]
        return res,api_dataa
    else: 
        print("Error in search!")

#app code
st.title('Weather Application')
# st.image("https://www.clipartmax.com/middle/m2i8Z5G6i8b1d3K9_11-white-weather-icon-png/", width=100)
col1,col2 =st.columns(2)
with col1:
    place_name=st.text_input("Please enter your city ")
    if place_name:
        res,api_dataa=getweather(place_name)
        st.map(pd.DataFrame({'lat' : [res[7]] , 'lon' : [res[6]]},columns = ['lat','lon']))
with col2:  
    if place_name:
        res,api_dataa=getweather(place_name)
        st.success("Date & Time : "+str(res[8]))
        st.success("Current : "+ str(round(res[1],2)))
        st.info("Description : "+str(res[2]))
        st.info("Humidity : "+str(round(res[3],2)))
        st.info("Wind Speed : "+str(res[4]))
        web_str = "![Alt Text]"+"(http://openweathermap.org/img/wn/"+str(res[5])+"@2x.png)"
        st.markdown(web_str)
        #st.markdown(str(res[5]))
        


# historical data
def history(lat,lon,start):
    res=requests.get(url.format(lat,lon,start,api_key))
    api_dataa=res.json()
    # weather_desc=api_dataa['weather'][0]['description']
    # return weather_desc
    temp=[]
    for i in api_dataa['weather']:
        t=i['description']
        temp.append(t)
    return api_dataa,temp 


if place_name:
    show_hist=st.expander(label="Last 5 Days History")
    with show_hist:
        start_date_string=st.date_input("Current Date")
        date_df=[]
        description=[]
        icon=[]
        for i in range(5):
          date_Str=start_date_string- timedelta(i)
          start_date=datetime.strptime(str(date_Str),"%Y-%m-%d")
          timestamp_1=datetime.timestamp(start_date)
        # his,temp=(res[5],res[4],int(timestamp_1))
          date_df.append(date_Str)

          res,api_dataa=getweather(place_name)
        # for i in range(int(date_Str),int(timestamp_1)):
          description.append(str(res[2]))
        #   k="![Alt Text]"+"(http://openweathermap.org/img/wn/"+str(res[5])+"@2x.png)"
        #   icon.append(k)

        df=pd.DataFrame()
        df['Date']=date_df
        df['Description']=description
        # df['Symbol']=icon
        st.table(df)

