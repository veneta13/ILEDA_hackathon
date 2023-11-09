import streamlit as st
import util_funcs
from utils import actor_engagement

if 'viz_type' not in st.session_state:
    st.session_state.viz_type = 'Course'

df = util_funcs.load_data()

st.markdown('# Student engagement')

st.radio(
    'Select the category you want to visualize',
    ['Course', 'Institution', 'Actor'],
    key='viz_type'
)

selected = None

if st.session_state.viz_type in ['Course', 'Institution']:
    selected = st.selectbox(
        "Filter by " + st.session_state.viz_type.lower(),
        (df['Course'].drop_duplicates().tolist() if st.session_state.viz_type == 'Course'
         else df['Institution'].drop_duplicates().tolist()),
        placeholder="Select " + st.session_state.viz_type.lower() + '...',
    )
else:
    selected = st.slider(
        'Select actor index...',
        0,
        df['actor.id'].max(),
        466
    )

treemap, bars, ranking = actor_engagement.display(df, selected)

if treemap is not None:
    st.plotly_chart(treemap)

if bars is not None:
    st.pyplot(bars)

if ranking is not None:
    st.plotly_chart(ranking)
