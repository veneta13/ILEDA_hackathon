import streamlit as st
import util_funcs
from utils import time_series

df = util_funcs.load_data()

st.markdown('# Time Series Analysis')

st.markdown('This module contains functions for analyzing and visualizing time series data related to user '
            'interactions in a learning environment.')

course = st.selectbox(
    "Select a course",
    df['Course'].drop_duplicates().tolist(),
    placeholder="Enter course name here...",
)

display_type = st.selectbox(
    "Select an assignment type",
    ['Graded assignments', 'Non-graded activities', 'Both types (single plot)', 'Both types (separate plots)'],
    placeholder="Enter assignment type here...",
)

st.pyplot(time_series.analyze_time_series(
    df,
    course,
    util_funcs.text_to_display(display_type)
))

st.pyplot(time_series.display_course_or_institution_actions(
    df,
    course,
    util_funcs.text_to_display(display_type)
))
