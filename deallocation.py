    # Importing the libraries
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from IPython.display import display

# Ignore pandas chained assignment warning
pd.options.mode.chained_assignment = None  # default='warn'

def time_deallocation(memory_block_size, alpha=0.1, beta=1):
    """
    Sets up the time latency when deallocating a memory block size.
    """

    return (memory_block_size * alpha)/1000 + beta

# Statistical and graphing function
def statistics(time_latency=[], df=None):
    """
    This is a function that provides statistical graphs about the necessary information encompassing deallocation.
    The graphs provided are:
        1. Memory Block Size Distribution
        2. Job Status Distribution
        3. Time Latency Distribution
        4. Memory Block Size Distribution
    """
    fig, ax = plt.subplots(2,2,figsize=(15, 10))
    ax[0, 0].bar(x=df.index, height=df['Memory Block Size'])
    ax[0, 0].set_xticks(range(30))
    ax[0, 0].set_xlabel('Table Block Index')
    ax[0, 0].set_ylabel('Memory Block Size')
    ax[0, 0].set_title('Memory Block Size Distribution')

    ax[0, 1].bar(x=df['Job Status'].value_counts().index, height=df['Job Status'].value_counts())
    ax[0, 1].set_xticks(df['Job Status'].value_counts().index.to_list())
    ax[0, 1].set_yticks(range(0, 25, 5))
    ax[0, 1].set_xlabel('Job Status')
    ax[0, 1].set_ylabel('Count')
    ax[0, 1].set_title('Job Status Distribution')

    ax[1, 0].plot(time_latency)
    ax[1, 0].set_xlabel('Deallocated Block Number')
    ax[1, 0].set_ylabel('Time Latency')
    ax[1, 0].set_title('Time Latency Distribution')

    ax[1, 1].bar([0, 1], [df[df['Job Status'] == 0]['Memory Block Size'].sum(), df[df['Job Status'] == 1]['Memory Block Size'].sum()])
    ax[1, 1].set_xticks(df['Job Status'].value_counts().index.to_list())
    ax[1, 1].set_xlabel('Job Status')
    ax[1, 1].set_ylabel('Cumulative Memory Block Size')
    ax[1, 1].set_title('Memory Block Size Distribution')

    plt.tight_layout()

    st.write(f"Total time latency = {np.sum(time_latency)}")
    st.write(f"Average time latency = {np.mean(time_latency)}")
    st.pyplot(fig)

def generate_fixed_partition_dataframe(num_job, MAX_MEMORY = 15000):
    """
    This is a function that generates a memory block containing equally distributed memory address and block size, and randomized job status.
    """

    random_memory_locations = np.linspace(1, MAX_MEMORY, num_job, dtype='int')
    random_job_status = np.random.randint(0, 2, num_job)
    memory_block_size = []

    for i in range(len(random_memory_locations) - 1):
        memory_block_size.append(random_memory_locations[i+1] - random_memory_locations[i])
    memory_block_size.append(np.random.randint(1, 1000, 1)[0])
    return pd.DataFrame({"Memory Address": random_memory_locations,
                         "Memory Block Size": memory_block_size,
                         "Job Status": random_job_status})

def deallocate_fixed_partition(df):
    """
    This is a function that alters the dataframe parameter (df) by performing the fixed-partition deallocation algorithm as discussed above.
    """
    deallocated_memory_count = 0
    time_latency = []
    for i in range(len(df)):
        if df["Job Status"].loc[i] == 1:
            # Simulating Fixed partition deallocation
            st.write(f"Deallocating Memory for Memory Address: {df['Memory Address'].loc[i]}...")
            time_ = time_deallocation(df["Memory Block Size"].loc[i])
            time_latency.append(time_)
            time.sleep(time_)
            df["Job Status"].loc[i] = 0
            deallocated_memory_count += 1
    st.write(f"Total memory deallocated: {deallocated_memory_count}")
    return time_latency

def generate_dynamic_partition_dataframe(num_jobs, case1=False, case2=False, case3=False, MAX_MEMORY = 15000):
    """
    This is a function that generates a memory block containing randomized distributed memory address, block size, job status.
    """

    random_memory_locations = sorted(np.random.randint(1, MAX_MEMORY, num_jobs))
    random_job_status = np.random.randint(0, 2, num_jobs)
    memory_block_size = []

    for i in range(len(random_memory_locations) - 1):
        memory_block_size.append(random_memory_locations[i+1] - random_memory_locations[i])
    memory_block_size.append(np.random.randint(1, 1000, 1)[0])

    if case1:
        random_job_status[-1] = 0

    if case2:
        random_job_status = [0 if num % 2 == 0 else 1 for num in range(num_jobs)]
        random_job_status[-1] = 0
        random_job_status[0] = 0

    if case3:
        random_job_status[2] = 1
        random_job_status[1] = 1
        random_job_status[0] = 1


    return pd.DataFrame({"Memory Address": random_memory_locations,
                         "Memory Block Size": memory_block_size,
                         "Job Status": random_job_status})

def deallocate_dynamic_case_1(df, one_iter=False):
    """
    This function takes a memory block dataframe as an input and simulates a dynamic
    memory deallocation based on case 1 parameters.
    """
    initial_len = len(df["Memory Address"])
    deallocated_memory_count = 0
    iterations = 1
    time_latency = []

    while df["Job Status"].nunique() != 1:
        st.write(f"Iteration Number: {iterations}")
        rows_to_drop = []
        for i in range(len(df) - 1):
            if df["Job Status"].loc[i] == 1 and df["Job Status"].loc[i + 1] == 0:
                # Simulating case 1 dyanmic partition deallocation
                st.write(f"  \tWaiting for Memory in Memory address {df['Memory Address'].loc[i]} to be realeased (free)...")
                time_ = time_deallocation(df["Memory Block Size"].loc[i])
                time.sleep(time_)
                st.write(f"  \tDeallocating Memory for Memory Address: {df['Memory Address'].loc[i]}...")
                st.write(f"  \tJoining Memory Address {df['Memory Address'].loc[i]} and {df['Memory Address'].loc[i + 1]}  \n")

                # Freeing job status
                df["Job Status"].loc[i] = 0

                # Joining memory address block sizes
                df["Memory Block Size"].loc[i] += df["Memory Block Size"].loc[i+1]

                # Putting the next memory address to rows to drop
                rows_to_drop.append(i + 1)

                # Memory deallocation time latency
                time.sleep(time_)
                time_latency.append(2 * time_)

        df.drop(rows_to_drop, inplace=True)
        df.reset_index(inplace=True, drop=True)
        if one_iter:
          break
        iterations +=1
    st.write(f"Total memory deallocated: {initial_len - len(df['Memory Address'])}.")
    return time_latency

def deallocate_dynamic_case_2(df, remove_null=False):
    """
    This function takes a memory block dataframe as an input and simulates a dynamic
    memory deallocation based on case 2 parameters.
    """

    iterations = 1
    initial_len = len(df["Memory Address"])
    time_latency = []

    rows_to_drop = []
    for i in range(1, len(df) - 2):
        if df["Job Status"].loc[i] == 1 and df["Job Status"].loc[i + 1] == 0 and df["Job Status"].loc[i - 1] == 0:
            # Simulating case 2 dyanmic partition deallocation
            st.write(f"Waiting for Memory in Memory address {df['Memory Address'].loc[i]} to be realeased (free)...")
            time_ = time_deallocation(df["Memory Block Size"].loc[i])
            time.sleep(time_)
            st.write(f"Deallocating Memory for Memory Address: {df['Memory Address'].loc[i]}...")
            st.write(f"Joining Memory Address {df['Memory Address'].loc[i-1]}, {df['Memory Address'].loc[i]} and {df['Memory Address'].loc[i+1]}  \n")

            # Freeing job status
            df["Job Status"].loc[i] = 0

            # Joining memory address block sizes
            df["Memory Block Size"].loc[i-1] += df["Memory Block Size"].loc[i]
            df["Memory Block Size"].loc[i-1] += df["Memory Block Size"].loc[i+1]

            # Putting the next memory address to rows to drop
            rows_to_drop.append(i + 1)

            # Replace current memory location to a null entry
            df.loc[i, "Memory Address"] = "*"
            df.loc[i, "Memory Block Size"] = 0
            df.loc[i, "Job Status"] = None
            df.loc[i+1, "Job Status"] = 1

            time.sleep(time_)
            time_latency.append(2 * time_)
    df.drop(rows_to_drop, inplace=True)
    df.reset_index(inplace=True, drop=True)
    iterations +=1

    if remove_null:
    # Removing Null Entries
        st.write(f"Removing Null Entries...")
        null_entries = df[df['Job Status'].isna()].index
        time.sleep(len(null_entries))
        df.drop(null_entries, inplace=True)
        st.write(f"Total number of null entries removed: {len(null_entries)}")
        df.reset_index(inplace=True, drop=True)
        df['Job Status'] = df['Job Status'].apply(lambda x: int(x))
    st.write(f"Total memory deallocated: {initial_len - len(df['Memory Address'])}.")
    return time_latency

def deallocate_dynamic_case_3(df, freeing_latency=2):
    """
    This function takes a memory block DataFrame as an input and simulates a dynamic memory deallocation based on case 3 parameters.
    """
    initial_df = df.copy()
    time_latency = []

    for i in range(1, len(df) - 2):
        if df["Job Status"].loc[i] == 1 and df["Job Status"].loc[i + 1] == 1 and df["Job Status"].loc[i - 1] == 1:
            # Simulating case 2 dyanmic partition deallocation
            st.write(f"Deallocating Memory for Memory Address: {df['Memory Address'].loc[i]}...")
            st.write(f"Found two adjacent busy job status for Memory Address {df['Memory Address'].loc[i]}:")
            st.write(f"  \t{df['Memory Address'].loc[i-1]}")
            st.write(f"  \t{df['Memory Address'].loc[i+1]}")

            time_ = time_deallocation(df['Memory Block Size'].loc[i])
            time.sleep(time_)
            time_latency.append(time_)

            # Converting Current Memory as null entry
            df.loc[i, "Memory Address"] = "*"
            df.loc[i, "Memory Block Size"] = 0
            df.loc[i, "Job Status"] = None

    memory_deallocated = 0
    display(df)
    free_null = st.text_input("Free Null Memories [y/N]: ", 'y', 1, help="Type 'y' for yes and 'N' for n")
    if free_null == 'y':

        # Free Null Entries
        st.write(f"Freeing Null Entries...")
        time.sleep(freeing_latency)
        for i in range(1, len(df) - 2):
            if df['Job Status'].isna().values[i]:

                st.write(f"Now catering memory address: {initial_df['Memory Address'].loc[i]}")
                st.write(f"Waiting for adjacent memory address to be deallocated...")

                # Deallocating previous adjacent memory address
                df.loc[i-1, "Job Status"] = 0
                time.sleep(freeing_latency)
                st.write(f"  \tAjacent memory address {df['Memory Address'].loc[i-1]} is now free!")

                # Deallocating next adjacent memory address
                df.loc[i+1, "Job Status"] = 0
                time.sleep(freeing_latency)
                st.write(f"  \tAdjacent memory address {df['Memory Address'].loc[i+1]} is now free!  \n")

                # Re-entry of the previously nulled memory address
                st.write(f"Reallocating memory address {initial_df['Memory Address'].loc[i]} to *  \n")
                time.sleep(freeing_latency)

                # Deallocating the current memory address
                df.loc[i, "Memory Address"] = initial_df["Memory Address"].loc[i]
                df.loc[i, "Memory Block Size"] = initial_df["Memory Block Size"].loc[i]
                df.loc[i, "Job Status"] = 0
                time.sleep(freeing_latency)
                st.write(f"    \tAdjacent memory address {df['Memory Address'].loc[i]} is now free!  \n")

                memory_deallocated+=3

        df['Job Status'] = df['Job Status'].apply(lambda x: int(x))
    st.write(f"Total memory deallocated: {memory_deallocated}")
    return time_latency
