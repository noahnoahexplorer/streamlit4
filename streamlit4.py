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
    try:
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
    except Exception as e:
        st.error(f"Error in number betting heatmap: {e}")

    try:
        # 30-minute Interval Heatmap Based on 'created_at'
        st.write("### 30-Minute Interval Heatmap Based on Created At")
        
        # Convert 'created_at' to datetime with the correct format
        data['created_at'] = pd.to_datetime(data['created_at'], format='%d/%m/%Y %H:%M', errors='coerce')
        
        # Remove rows with invalid 'created_at' (NaT values)
        data.dropna(subset=['created_at'], inplace=True)
        
        # Create a new column for 30-minute intervals
        data['30min_interval'] = data['created_at'].dt.floor('30T')
        
        # Aggregate data for the heatmap
        interval_data = data.groupby(['30min_interval']).size().reset_index(name='num_bets')
        interval_data['day'] = interval_data['30min_interval'].dt.day_name()
        interval_data['time_slot'] = interval_data['30min_interval'].dt.strftime('%H:%M')
        
        # Create pivot table for heatmap
        heatmap_data_time = interval_data.pivot(index='day', columns='time_slot', values='num_bets').fillna(0)
        
        # Plotting the heatmap with larger font size and rounded values
        fig, ax = plt.subplots(figsize=(14, 8))  # Adjust the figure size for more space
        sns.heatmap(heatmap_data_time, cmap='YlGnBu', annot=True, fmt=".1f", ax=ax, 
                    annot_kws={"size": 10},  # Increase font size for annotation
                    cbar_kws={'label': 'Number of Bets'})  # Colorbar label
        plt.title('Number of Bets by 30-Minute Intervals')
        plt.xlabel('Time Slot (30 min intervals)')
        plt.ylabel('Day of the Week')
        plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate and adjust font size for x-axis labels
        plt.yticks(rotation=0, fontsize=10)  # Adjust font size for y-axis labels
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error in 30-minute interval heatmap: {e}")

# Check if file is uploaded
if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        betting_data = pd.read_csv(uploaded_file)

        # Print the first few rows for debugging
        st.write("First few rows of the uploaded data:")
        st.write(betting_data.head())

        # Check if the required columns are present
        if 'number_cost_dict' not in betting_data.columns or 'created_at' not in betting_data.columns:
            st.error("Uploaded CSV file must contain 'number_cost_dict' and 'created_at' columns.")
        else:
            # Convert 'number_cost_dict' column to dictionary
            betting_data['number_cost_dict'] = betting_data['number_cost_dict'].apply(eval)  # Ensure it's a dictionary

            # Display the heatmaps
            display_heatmaps(betting_data)

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
