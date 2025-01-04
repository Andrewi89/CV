import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ----------------------
# Data and icon mappings
# ----------------------
APPLIANCE_DATA = [
    {"Appliance": "Oven", "PowerRating_kW": 2.50, "UsageFrequency": "Daily", "UsageMinutes": 30},
    {"Appliance": "Kettle", "PowerRating_kW": 3.00, "UsageFrequency": "Multiple times daily", "UsageMinutes": 5},
    {"Appliance": "Fridge", "PowerRating_kW": 0.2, "UsageFrequency": "Continuous", "UsageMinutes": 1440},
    {"Appliance": "Electric shower", "PowerRating_kW": 9, "UsageFrequency": "Daily", "UsageMinutes": 10},
    {"Appliance": "Tumble Dryer", "PowerRating_kW": 2.5, "UsageFrequency": "Daily", "UsageMinutes": 30},
    {"Appliance": "Electric heater", "PowerRating_kW": 2.5, "UsageFrequency": "Daily", "UsageMinutes": 60},
    {"Appliance": "Washing machine", "PowerRating_kW": 2.1, "UsageFrequency": "Daily", "UsageMinutes": 60},
    {"Appliance": "Oil-filled radiator", "PowerRating_kW": 2, "UsageFrequency": "Daily", "UsageMinutes": 60},
    {"Appliance": "Hairdryer", "PowerRating_kW": 2, "UsageFrequency": "Daily", "UsageMinutes": 5},
    {"Appliance": "Hob", "PowerRating_kW": 2, "UsageFrequency": "Daily", "UsageMinutes": 15},
    {"Appliance": "Grill", "PowerRating_kW": 1.5, "UsageFrequency": "Daily", "UsageMinutes": 15},
    {"Appliance": "Iron", "PowerRating_kW": 1.5, "UsageFrequency": "Daily", "UsageMinutes": 30},
    {"Appliance": "Toaster", "PowerRating_kW": 1, "UsageFrequency": "Daily", "UsageMinutes": 5},
    {"Appliance": "Microwave", "PowerRating_kW": 1, "UsageFrequency": "Daily", "UsageMinutes": 10},
    {"Appliance": "Microwave (low power)", "PowerRating_kW": 0.8, "UsageFrequency": "Daily", "UsageMinutes": 10},
    {"Appliance": "Electric mower", "PowerRating_kW": 1, "UsageFrequency": "Daily", "UsageMinutes": 30},
    {"Appliance": "Vacuum cleaner", "PowerRating_kW": 0.9, "UsageFrequency": "Daily", "UsageMinutes": 30},
    {"Appliance": "Dehumidifier", "PowerRating_kW": 0.5, "UsageFrequency": "Daily", "UsageMinutes": 30},
    {"Appliance": "Towel rail", "PowerRating_kW": 0.45, "UsageFrequency": "Daily", "UsageMinutes": 30},
    {"Appliance": "LCD TV", "PowerRating_kW": 0.12, "UsageFrequency": "Daily", "UsageMinutes": 60},
    {"Appliance": "Fridge-freezer", "PowerRating_kW": 0.3, "UsageFrequency": "Continuous", "UsageMinutes": 1440},
    {"Appliance": "Desktop computer", "PowerRating_kW": 0.14, "UsageFrequency": "Daily", "UsageMinutes": 360},
    {"Appliance": "Games console", "PowerRating_kW": 0.12, "UsageFrequency": "Daily", "UsageMinutes": 240},
    {"Appliance": "Laptop", "PowerRating_kW": 0.05, "UsageFrequency": "Daily", "UsageMinutes": 240},
    {"Appliance": "TV box", "PowerRating_kW": 0.04, "UsageFrequency": "Daily", "UsageMinutes": 240},
    {"Appliance": "Extractor fan", "PowerRating_kW": 0.02, "UsageFrequency": "Daily", "UsageMinutes": 30},
    {"Appliance": "Broadband router", "PowerRating_kW": 0.01, "UsageFrequency": "Continuous", "UsageMinutes": 1440},
]

# You could map any text-based icon/emoji to your appliance names:
APPLIANCE_ICONS = {
    "Oven": "🔥",
    "Kettle": "☕",
    "Fridge": "❄️",
    "Electric shower": "🚿",
    "Tumble Dryer": "🌪️",
    "Electric heater": "♨️",
    "Washing machine": "🌀",
    "Oil-filled radiator": "🔥",
    "Hairdryer": "💇",
    "Hob": "🍳",
    "Grill": "🍖",
    "Iron": "🧺",
    "Toaster": "🍞",
    "Microwave": "🔌",
    "Microwave (low power)": "🔌",
    "Electric mower": "🌱",
    "Vacuum cleaner": "🧹",
    "Dehumidifier": "💧",
    "Towel rail": "🚿",
    "LCD TV": "📺",
    "Fridge-freezer": "❄️",
    "Desktop computer": "💻",
    "Games console": "🎮",
    "Laptop": "💻",
    "TV box": "📺",
    "Extractor fan": "💨",
    "Broadband router": "🌐"
}


# ----------------------
# Helper function
# ----------------------
def calculate_costs(df: pd.DataFrame, peak: float, offpeak: float = None) -> pd.DataFrame:
    """
    Given a base dataframe of appliances, calculates total energy usage 
    and cost for day & optional night tariff.
    """
    df['Energy (kWh)'] = df['PowerRating_kW'] * (df['UsageMinutes'] / 60)
    
    # Calculate day cost
    df['Day Time Cost (£)'] = df['Energy (kWh)'] * peak
    
    # Offpeak calculation if user has it
    if offpeak is not None:
        df['Night Time Cost (£)'] = df['Energy (kWh)'] * offpeak
    else:
        df['Night Time Cost (£)'] = np.nan  # or 0, whichever you prefer
    
    # Map icons
    df['Icon'] = df['Appliance'].apply(lambda x: APPLIANCE_ICONS.get(x, "❓"))
    
    return df


# ----------------------
# Streamlit layout
# ----------------------
st.title("True Energy Cost Calculator")
st.write("Find out what that tariff is actually costing you")

peak_electricity = st.number_input(
    "Insert a electricity cost (day)",
    value=0.00,
    help="Enter your daytime electricity cost in £/kWh..."
)

offpeak_on = st.toggle("I have a separate night-time price")

if offpeak_on:
    offpeak_electricity = st.number_input(
        "Insert an electricity cost (night)",
        value=0.00,
        help="Enter your night-time electricity cost in £/kWh..."
    )
    st.write(f"**Day-time electricity cost**: £{peak_electricity:,.2f}")
    st.write(f"**Night-time electricity cost**: £{offpeak_electricity:,.2f}")
else:
    offpeak_electricity = None
    st.write(f"**Day-time electricity cost**: £{peak_electricity:,.2f}")

# ----------------------
# Create / display table
# ----------------------
if peak_electricity >= 0.001:
    df = pd.DataFrame(APPLIANCE_DATA)
    df = calculate_costs(df, peak_electricity, offpeak_electricity)
    
    # Conditionally rename columns, depending on offpeak usage
    if offpeak_on:
        # Rename "Day Time Cost (£)" -> "Day Cost"
        #        "Night Time Cost (£)" -> "Night Cost"
        df.rename(
            columns={
                'Day Time Cost (£)': 'Day Cost',
                'Night Time Cost (£)': 'Night Cost'
            }, 
            inplace=True
        )
    else:
        # No offpeak, so rename day column to just "Cost"
        # and remove the night cost column
        df.rename(columns={'Day Time Cost (£)': 'Cost'}, inplace=True)
        df.drop(columns='Night Time Cost (£)', inplace=True)

    # st.subheader("Full details")
    # st.dataframe(df)

    # ----------------------
    # Appliance Cost Summary
    # ----------------------
    st.subheader("Appliance Cost Summary")
    
    # Let the user select which appliances to show in the summary
    all_appliance_names = df["Appliance"].unique().tolist()
    selected_appliances = st.multiselect(
        "Select appliances to display in the summary:",
        options=all_appliance_names,
        default=["Oven", "Hob", "Toaster", "Kettle", "Fridge-freezer","Washing machine", "Hairdryer"]  # or any set of default appliances
    )

    # Filter DataFrame for just the selected appliances
    summary_df = df[df['Appliance'].isin(selected_appliances)].copy()
    # Create a new "Usage (hours)" column for the summary
    summary_df["Usage (hours)"] = summary_df["UsageMinutes"] / 60
    # Figure out which columns to display
    base_cols = ["Icon", "Appliance", "Usage (hours)"]
    # If offpeak_on is True, we have 'Day Cost' and 'Night Cost' columns
    if offpeak_on:
        cost_cols = ["Day Cost", "Night Cost"]
    else:
        # If offpeak is off, we have only 'Cost' column
        cost_cols = ["Cost"]
    display_cols = base_cols + cost_cols
    summary_df = summary_df[display_cols]

    # Display table
    format_dict = {col: "£{:.2f}" for col in cost_cols if col in summary_df.columns}
    format_dict["Usage (hours)"] = "{:.2f}"

    st.table(summary_df.style.format(format_dict))

# ----------------------
# Footer
# ----------------------
current_year = datetime.now().year
footer_col1, footer_col2, footer_col3 = st.columns([1, 6, 1])
with footer_col2:
    st.markdown(
        f"""
        <hr style="height:1px;border:none;color:#333;background-color:#333;" />
        <p style="text-align: center; color: grey;">
            &copy; {current_year} Andrew Ireland. All Rights Reserved.
        </p>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <small style="color: grey;">
    ***Disclaimer:***  
    While I have aimed to make this calculator as accurate as possible, please note that the results are estimates. 
    These estimates should be used to inform decisions but not as the sole basis for making significant financial 
    commitments. 
    </small>
    """,
    unsafe_allow_html=True,
)