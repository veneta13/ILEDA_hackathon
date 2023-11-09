import streamlit as st
import util_funcs
from utils import linear_regression

df = util_funcs.load_data()

st.markdown('# Linear Regression Results')

fig1, fig2, results = linear_regression.regression(df)

st.markdown('### Correlation matrix')

if fig1 is not None:
    st.pyplot(fig1)


st.markdown(results)

if fig2 is not None:
    st.pyplot(fig2)
