import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Temperature Tracker", layout="wide")

# Initialize session state for storing data if it doesn't exist
if "data" not in st.session_state:
    st.session_state.data = []

# Sidebar input form
st.sidebar.header("Add a Temperature Record")
name = st.sidebar.text_input("Child's Name")
temp = st.sidebar.number_input("Temperature (°F)", min_value=90.0, max_value=110.0, step=0.1)
medicine = st.sidebar.text_input("Medicine Given (optional)")
dosage = st.sidebar.text_input("Dosage (optional)")
date = st.sidebar.date_input("Date", datetime.now().date())
time = st.sidebar.time_input("Time", datetime.now().time())
timestamp = datetime.combine(date, time)

if st.sidebar.button("Add Record"):
    if name and temp:
        st.session_state.data.append({
            "Child": name,
            "Temperature": temp,
            "Medicine": medicine if medicine else None,
            "Dosage": dosage if dosage else None,
            "Timestamp": timestamp
        })
        st.sidebar.success("Record added successfully!")
    else:
        st.sidebar.error("Please enter both the child's name and temperature.")

# Convert session data to DataFrame
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    df = df.sort_values("Timestamp")
    
    # Plot data
    st.title("Children's Temperature Over Time")
    fig, ax = plt.subplots(figsize=(10, 5))
    for child in df["Child"].unique():
        child_data = df[df["Child"] == child]
        ax.plot(child_data["Timestamp"], child_data["Temperature"], marker="o", linestyle="-", label=child)
    
    ax.set_xlabel("Date and Time")
    ax.set_ylabel("Temperature (°F)")
    ax.legend()
    st.pyplot(fig)
    
    # Display data table
    st.subheader("Temperature Records")
    st.dataframe(df, use_container_width=True)
else:
    st.info("No data entered yet. Use the sidebar to add records.")
