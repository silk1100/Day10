import streamlit as st
from streamlit import caching
import pandas as pd
import numpy as np
import plotly.express as px
from alpha_vantage.timeseries import TimeSeries
import os
import dotenv


st.title("12 Days MileStone")

dotenv.load_dotenv()
symbol = st.text_input("Enter symbol:")
st.text(symbol)
if not os.path.exists('./symbol.txt') and len(symbol) > 0:
    with open('./symbol.txt', 'w') as f:
        f.write(symbol)
elif len(symbol) > 0:
    with open('./symbol.txt','r') as f:
        old_sym = f.readline()
    if old_sym != symbol:
        caching.clear_cache()
        with open('./symbol.txt', 'w') as f:
            f.write(symbol)

if len(symbol) > 0:
    @st.cache
    def load_data(symbol="MSFT"):
        ts = TimeSeries(key=os.getenv("ALPHAKEY"), output_format="pandas", indexing_type='date')
        data = ts.get_daily_adjusted(symbol=symbol, outputsize="full")[0]
        return data

    df = load_data(symbol)
    year = st.number_input("Select year", value=2020, min_value=df.index.year.min(), max_value=df.index.year.max())
    month = st.number_input("Select Month", value=1, min_value=df.index.month.min(), max_value=df.index.month.max())

    sub_df = df.loc[(df.index.year==year)&(df.index.month==month),:]

    # st.dataframe(sub_df)
    if len(sub_df) >0:
        basic_plt = px.line(x=sub_df.index,
                            y=sub_df['4. close'],
                            labels={'x':f"Days of {month}/{year}",'y':"Price"},
                            title=f"Closing Prices for {symbol}")

        st.plotly_chart(figure_or_data=basic_plt)
    else:
        st.text(f"NO data for {symbol} in {month}/{year}")