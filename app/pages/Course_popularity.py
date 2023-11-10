import streamlit as st
import util_funcs
from utils import course_popularity

df = util_funcs.load_data()

st.markdown('# Course Popularity')

st.markdown('This module aims to analyze the popularity of courses within the dataset, providing insights into user '
            'interactions and engagement patterns.')

fig1, fig2, fig3 = course_popularity.course_popularity(df)

st.markdown('**Distribution of user interactions across courses:**')
st.pyplot(fig1)

st.markdown('**Distribution of user interactions by course:**')
st.pyplot(fig2)

st.markdown('**Median interaction count per person vs the number of students enrolled in each course:**')
st.markdown(':star: Flipped classroom course')
st.markdown(':white_circle: Project-based course')
st.pyplot(fig3)
