import streamlit as st
import pandas as pd

@st.cache_data
def load_data(file_path: str, dtype: dict, date_cols: list) -> pd.DataFrame:

    df = pd.read_csv(file_path, dtype=dtype)

    for col_data in date_cols:
        df[col_data] = pd.to_datetime(df[col_data])
    
    return df
