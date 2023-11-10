import streamlit as st
import util_funcs
from utils import verbs

df = util_funcs.load_data()

st.markdown('# Verbs')

st.markdown('This module contains visualizations for analyzing interactions within the learning platform dataset, '
            'focusing on verbs, courses, and their relationships.')

lollipop_fig = verbs.get_verb_lollipop(df)
radar_fig_course = verbs.get_verb_radar_course(df)
radar_fig_verb = verbs.get_verb_radar_verb(df)

st.pyplot(lollipop_fig)

with st.expander('Show the verb(s) associated with each course'):
    st.plotly_chart(radar_fig_course, use_container_width=True)

with st.expander('Show the course(s) associated with each verb'):
    st.plotly_chart(radar_fig_verb, use_container_width=True)
