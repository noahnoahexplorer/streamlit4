import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Streamlit settings
st.set_page_config(page_title="Lottery Betting Analysis", layout="wide")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])


# Function to process and display the data
def display_heatmaps(data):
    st.write("### Number Betting Heatmap")
    # Assuming the number_cost_dict is parsed correctly
    # Assuming the betting_data DataFrame has been already parsed and contains the number betting data

    # Create a heatmap for betting data
    heatmap_data = pd.DataFrame(data)
    number_covered = list(range(1, 101))  # Numbers from 1 to 100
    # Initialize a zero matrix for heatmap
    heatmap_matrix = pd.DataFrame(0, index=number_covered, columns=["Betting Coverage"])

    # Fill the heatmap matrix based on betting data
    for betting_dict in data['number_cost_dict']:
        for number, amount in betting_dict.items():
            heatmap_matrix.loc[int(number)] += amount

    # Visualize the number betting heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(heatmap_matrix, cmap='YlGnBu', annot=False, cbar=True, ax=ax)
    st.pyplot(fig)

    # 30-minute Interval Heatmap Based on 'created_at'
    st.write("### 30-Minute Interval Heatmap Based on Created At")
    data['created_at'] = pd.to_datetime(data['created_at'])
    data['30min_interval'] = data['created_at'].dt.floor('30T')

    # Aggregate data for the heatmap
    interval_data = data.groupby('30min_interval').size().reset_index(name='num_bets')
    interval_data['day'] = interval_data['30min_interval'].dt.day_name()
    interval_data['time_slot'] = interval_data['30min_interval'].dt.strftime('%H:%M')

    # Create pivot table for heatmap
    heatmap_data_time = interval_data.pivot('day', 'time_slot', 'num_bets').fillna(0)

    # Plotting the heatmap
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(heatmap_data_time, cmap='YlGnBu', annot=True, fmt=".1f", ax=ax)
    plt.title('Number of Bets by 30-Minute Intervals')
    plt.xlabel('Time Slot (30 min intervals)')
    plt.ylabel('Day of the Week')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    st.pyplot(fig)


# Check if file is uploaded
if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        betting_data = pd.read_csv(uploaded_file)

        # Convert 'number_cost_dict' column to dictionary
        betting_data['number_cost_dict'] = betting_data['number_cost_dict'].apply(eval)  # Ensure it's a dictionary

        # Display the heatmaps
        display_heatmaps(betting_data)

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")

