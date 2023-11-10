import streamlit as st
import util_funcs
from utils import linear_regression

df = util_funcs.load_data()

st.markdown('# Linear Regression Results')

fig1, fig2, results = linear_regression.regression(df)

st.markdown('This module conducts a regression analysis on a given dataset, employing the scikit-learn library for '
            'linear regression.')

if fig1 is not None:
    st.markdown('**Correlation of the dataset features:**')
    st.pyplot(fig1)

st.markdown('**Achieved linear regression results:**')
st.markdown(results)

if fig2 is not None:
    st.markdown('**Feature weights:**')
    st.pyplot(fig2)
