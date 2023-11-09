import streamlit as st
import util_funcs
from utils import clustering

df = util_funcs.load_data()

st.markdown('# Cluster Analysis ')

course = st.selectbox(
    "Select a course",
    df['Course'].drop_duplicates().tolist(),
    placeholder="Enter course name here...",
)

fig1, fig2 = clustering.cluster(course, 3)

if fig1 is not None:
    st.plotly_chart(fig1)

if fig2 is not None:
    st.pyplot(fig2)

