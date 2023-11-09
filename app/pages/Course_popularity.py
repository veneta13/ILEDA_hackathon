import streamlit as st
import util_funcs
from utils import course_popularity

df = util_funcs.load_data()

st.markdown('# Course Popularity')

fig1, fig2, fig3 = course_popularity.course_popularity(df)

st.pyplot(fig1)
st.pyplot(fig2)
st.pyplot(fig3)
