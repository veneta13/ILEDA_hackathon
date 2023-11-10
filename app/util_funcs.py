import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    df = pd.read_csv(
        'data/processed.csv'
    )
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def text_to_display(text):
    if text == 'Graded assignments':
        return 'assessments'
    if text == 'Non-graded activities':
        return 'non_assessments'
    if text == 'Both types (single plot)':
        return 'total'
    if text == 'Both types (separate plots)':
        return 'both'

