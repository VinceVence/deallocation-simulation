# Importing the libraries
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from IPython.display import display
from deallocation import time_deallocation, statistics, generate_fixed_partition_dataframe, deallocate_fixed_partition, generate_dynamic_partition_dataframe, deallocate_dynamic_case_1, deallocate_dynamic_case_2, deallocate_dynamic_case_3

# Ignore pandas chained assignment warning
pd.options.mode.chained_assignment = None  # default='warn'

# Setting Defaults
PAGE_CONFIG = {"page_title": "Deallocation Simulation",
               "page_icon": r'Pictures/web_icon.png',
               "layout": "wide",
               "initial_sidebar_state": "auto"}
NUM_JOBS = 30

st.set_page_config(**PAGE_CONFIG)

def callback():
    try:
        st.session_state.generate_fixed = True
        st.session_state.generate_dynamic = True
    except:
        st.warning("No current session initialized")


def main():
    st.title("Deallocation Simulation")
    menu = ['Fixed Partition', 'Dynamic Partition']
    with st.sidebar:
        st.title("Simulation Parameters")
        choice = st.selectbox("Deallocation Type", menu, on_change=callback)
        num_jobs = st.slider("Memory Size", 5, 100, NUM_JOBS, 5, on_change=callback)
        MAX_MEMORY = st.slider("Maximum memory address", 10000, 20000, 15000, 1000, on_change=callback)
        st.title("Time Latency")
        alpha = st.slider("alpha", 0.0, 0.5, 0.1, on_change=callback)
        beta = st.slider("beta", 1.0, 2.0, 1.5, on_change=callback)


    if choice == 'Fixed Partition':
        try:
            generate_fixed = st.button('Generate Fixed-Partition Memory Block', on_click=callback)
            if generate_fixed or st.session_state.generate_fixed:
                df = generate_fixed_partition_dataframe(num_jobs, MAX_MEMORY)
                st.dataframe(df, None, None)
                if st.button('Simulate'):
                    time_latency = deallocate_fixed_partition(df)
                    st.dataframe(df)
                    statistics(time_latency, df)
        except:
            st.warning("No current session initialized")

    if choice == 'Dynamic Partition':
        try:
            generate_dynamic = st.button('Generate Dynamic-Partition Memory Block', on_click=callback)
            if generate_dynamic or st.session_state.generate_dynamic:
                case = st.radio('Select case:', ['Case 1', 'Case 2', 'Case 3'])
                st.markdown('<p><b>Note: Refer to the documentation for further details about the dynamic cases.</b></p>', unsafe_allow_html=True)
                if case == 'Case 1':
                    df = generate_dynamic_partition_dataframe(num_jobs,case1=True,MAX_MEMORY=MAX_MEMORY)
                elif case == 'Case 2':
                    df = generate_dynamic_partition_dataframe(num_jobs,case2=True,MAX_MEMORY=MAX_MEMORY)
                else:
                    df = generate_dynamic_partition_dataframe(num_jobs,case3=True,MAX_MEMORY=MAX_MEMORY)
                st.dataframe(df)
                if st.button('Simulate'):
                    if case == 'Case 1':
                        time_latency = deallocate_dynamic_case_1(df)
                        st.dataframe(df)
                        statistics(time_latency, df)
                    elif case == 'Case 2':
                        time_latency = deallocate_dynamic_case_2(df, remove_null=True)
                        st.dataframe(df)
                        statistics(time_latency, df)
                    else:
                        time_latency = deallocate_dynamic_case_3(df, freeing_latency=2)
                        st.dataframe(df)
                        statistics(time_latency, df)
        except Exception as e:
            st.warning("No current session initialized")
            st.warning(e)



if __name__ == "__main__":
    main()
