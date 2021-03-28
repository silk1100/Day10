import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from alpha_vantage.timeseries import TimeSeries
import os
import dotenv


st.title("12 Days MileStone")

st.subheader("Data")
st.text("Loading data from Alpha Vantage ...")
dotenv.load_dotenv()
@st.cache
def load_data(symbol="MSFT"):
    ts = TimeSeries(key=os.getenv("ALPHAKEY"), output_format="pandas", indexing_type='date')
    data = ts.get_daily_adjusted(symbol=symbol, outputsize=40)[0]
    return data

df = load_data()
st.text("PLotting data")


basic_plt = px.line(x=df.index,
                    y=df['4. close'],
                    labels={'x':"Date",'y':"Price"},
                    title="Closing Prices for ")

st.plotly_chart(figure_or_data=basic_plt)