import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px


#st.title("Hello world")
#st.markdown("## my first streamlit application")
st.markdown("# Analyzing the data with help of the streamlit library in python ")


DATA_URL=(
"C:\streamlit-nyc/Motor_Vehicle_Collisions_-_Crashes.csv"
)
st.title("Motor_Vehicle_Collisions in Newyork city ")
st.markdown("<h1 style='text-align: center;'>🚗💥🏎️</h1>", unsafe_allow_html=True)
st.markdown("### This application is streamlit dashboard that it can be used to analyse the Motor_Vehicle_Collisions")
@st.cache(persist=True)
def load_data(nrows):
    data=pd.read_csv(DATA_URL,nrows=nrows,parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE','ZIP_CODE'],inplace=True)
    lowercase=lambda x:str(x).lower()
    data.rename(lowercase,axis='columns',inplace=True)
    data.rename(columns={'crash_date_crash_time':'date/time'},inplace=True)
    return data
#data=pd.read_csv(DATA_URL)
data=load_data(100000)
copy_of_data=data
st.header("Where the most people are injuried in Newyork")
injured_people=st.slider("No of persons injuried  in vechile collision",0,19)
st.map(data.query("injured_persons>=@injured_people")[['latitude','longitude']].dropna(how="any"))

st.header("how many collison are occured during a given time in a day")
hour=st.slider("hour to look at ",0,24)
data=data[data['date/time'].dt.hour==hour]

st.markdown("vechile collision between %i:00 and %i:00" %(hour,(hour+1)%24))
midpoint=(np.average(data['latitude']),np.average(data['longitude']))
st.write(pdk.Deck(
map_style="mapbox://styles/mapbox/light-v9",
initial_view_state={
"latitude":midpoint[0],
"longitude":midpoint[1],
"zoom":11,
"pitch":50,

},
layers=[
pdk.Layer(
"HexagonLayer",
data=data[['date/time','latitude','longitude']],
get_position=['longitude','latitude'],
radius=100,
extruded=True,
pickable=True,
elevation_scale=4,
auto_highlight=True,
coverage=1,
elevation_range=[0,1000],
),
],
))


st.subheader("In between %i:00 to %i:00 No.of collisions are occured for every minute are Plotted in a graph" %(hour,(hour+1)%24))
filtered=data[(data['date/time'].dt.hour>=hour)& (data['date/time'].dt.hour<(hour+1))]
hist=np.histogram(filtered['date/time'].dt.minute,bins=60,range=(0,60))[0]
chart_data=pd.DataFrame({'minute':range(60),'crashes':hist})
fig=px.bar(chart_data,x='minute',y='crashes',hover_data=['minute','crashes'],height=400)
st.write(fig)

st.header("Top 5 dangerous streets affected by people")
select=st.selectbox("affected type of prople",['pedestrains','cyclists','motorists'])
if select=='pedestrians':
    st.write(copy_of_data.query("injured_pedestrians>=1")[["on_street_name","injured_pedestrians"]].sort_values(by=["injured_pedestrians"],ascending=False).dropna(how="any")[:5])
elif select=="cyclists":
    st.write(copy_of_data.query("injured_cyclists>=1")[["on_street_name","injured_cyclists"]].sort_values(by=["injured_cyclists"],ascending=False).dropna(how="any")[:5])
else:
    st.write(copy_of_data.query("injured_motorists>=1")[["on_street_name","injured_motorists"]].sort_values(by=["injured_motorists"],ascending=False).dropna(how="any")[:5])


if st.checkbox("show Rawdata",False):
    st.subheader("Raw data")
    st.write(data)
