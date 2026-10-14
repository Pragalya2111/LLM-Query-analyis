import streamlit as st
import pandas as pd
import numpy as np


class Dashboard:
    def __init__(self):
        self.title = "My Streamlit Dashboard"
 
    def run(self):
        st.set_page_config(layout="wide")
        st.sidebar.markdown("- [Home](#)")
        st.sidebar.markdown("- Config")
        styl = f"""
        <style>
            .stTextInput {{
            position: fixed;
            top: 1rem;
            }}
        </style>
        """
        st.markdown(styl, unsafe_allow_html=True)
        st.text_input("", "", placeholder="search here...")
 
        col1, col2, col3 = st.columns(3)
 
        with col1:
            st.markdown(
                """
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 15px;'>
                    <h3>The Best</h3>
                    <p>Ans</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            # st.subheader("The Best")
            # st.write("Ans")
 
        with col2:
            st.markdown(
                """
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 15px;'>
                    <h3>2nd match</h3>
                    <p>Ans</p>
                </div>
                """,
                unsafe_allow_html=True
            )
 
        with col3:
            st.markdown(
                """
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 15px;'>
                    <h3>3rd match</h3>
                    <p>Ans</p>
                </div>
                """,
                unsafe_allow_html=True
            )
 
        col4, col5 = st.columns(2)
 
        with col4:
            chart_data1 = np.random.randn(20, 3)
            st.line_chart(chart_data1)
 
        with col5:
            chart_data2 = np.random.randn(20, 3)
            st.area_chart(chart_data2)
 
        st.subheader("Table")
        data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'London', 'Paris']
        }
        df = pd.DataFrame(data)
        st.table(df)
 
if __name__ == "__main__":
   
    dashboard = Dashboard()
    dashboard.run()