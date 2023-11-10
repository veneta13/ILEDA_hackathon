import streamlit as st
import util_funcs
from utils import network_analysis

df = util_funcs.load_data()

st.markdown('# Network Analysis')

figure, data = network_analysis.get_network(df)

st.markdown('This module generates a visualization of the number of interactions per course and the types '
            'of interactions. Each course is represented by a node, and the interactions are represented by links '
            'between the nodes.')

st.plotly_chart(figure, use_container_width=True)

st.markdown('## Data Display')

st.markdown('**Filter the data:**')
courses = st.multiselect(
    'Select course(s)',
    data['Course'].drop_duplicates().tolist(),
    data['Course'].drop_duplicates().tolist()[0])

interactions = st.multiselect(
    'Select course(s)',
    data['Interaction with'].drop_duplicates().tolist(),
    data['Interaction with'].drop_duplicates().tolist()[0])

st.dataframe(
    data[data['Course'].isin(courses) & data['Interaction with'].isin(interactions)],
    use_container_width=True
)
