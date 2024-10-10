import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from chart_utils import *
from indicator_utils import *
from query import view_all_data
from style_config import apply_custom_css

def show():
    st.title("Real-Time Data Visualization")

# Fetch data from the database
results = view_all_data()

# Convert the results to a DataFrame
df = pd.DataFrame(results, columns=["stock_symbol", "date", "open_price", "high_price", "low_price", "close_price", "volume"])

# Ensure the date column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Set a common height and width for all charts
chart_height = 600
chart_width = 1000

# Define range selector buttons including the new options
rangeselector_buttons = [
    dict(count=5, label="5D", step="day", stepmode="backward"),
    dict(count=1, label="1M", step="month", stepmode="backward"),
    dict(count=3, label="3M", step="month", stepmode="backward"),
    dict(label="YTD", step="year", stepmode="todate"),
    dict(count=1, label="1Y", step="year", stepmode="backward"),
    dict(count=3, label="3Y", step="year", stepmode="backward"),
    dict(count=5, label="5Y", step="year", stepmode="backward"),
    dict(step="all")
]

# Define grid settings for xaxis and yaxis
axis_config = dict(
    gridcolor='rgb(200, 200, 200)',  # Set grid line color
    gridwidth=1,  # Set grid line width
    tickformat='%Y-%m-%d',  # Format tick marks for xaxis
    tickformat_y='.2f'  # Format tick marks for yaxis
)

# Function to create different types of charts with optional indicators
def create_chart(data, chart_type, indicator=None, window=20):
    if chart_type == "Candlestick Chart":
        fig = create_candlestick_chart(data, company)
    elif chart_type == "Line Chart":
        fig = create_line_chart(data)
    elif chart_type == "Bar Chart":
        fig = create_bar_chart(data)
    elif chart_type == "Area Chart":
        fig = create_area_chart(data)

    # Add indicator if selected
    if indicator == "SMA":
        sma = calculate_sma(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=sma, mode='lines', name=f'SMA ({window})'))
    elif indicator == "EMA":
        ema = calculate_ema(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=ema, mode='lines', name=f'EMA ({window})'))
    elif indicator == "Bollinger Bands":
        sma, upper_band, lower_band = calculate_bollinger_bands(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=upper_band, mode='lines', name=f'Upper Band ({window})'))
        fig.add_trace(go.Scatter(x=data['date'], y=lower_band, mode='lines', name=f'Lower Band ({window})'))
    elif indicator == "Keltner Channels":
        ema_typical_price, upper_channel, lower_channel = calculate_keltner_channels(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=upper_channel, mode='lines', name=f'Upper Keltner Channel ({window})'))
        fig.add_trace(go.Scatter(x=data['date'], y=lower_channel, mode='lines', name=f'Lower Keltner Channel ({window})'))
    elif indicator == "Envelopes":
        upper_envelope, lower_envelope = calculate_envelopes(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=upper_envelope, mode='lines', name=f'Upper Envelope ({window})'))
        fig.add_trace(go.Scatter(x=data['date'], y=lower_envelope, mode='lines', name=f'Lower Envelope ({window})'))
    elif indicator == "Price Channels":
        high_channel, low_channel = calculate_price_channels(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=high_channel, mode='lines', name=f'High Channel ({window})'))
        fig.add_trace(go.Scatter(x=data['date'], y=low_channel, mode='lines', name=f'Low Channel ({window})'))
    elif indicator == "Average True Range (ATR)":
        atr = calculate_atr(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=atr, mode='lines', name=f'ATR ({window})'))
    
    # Update layout for all chart types
    fig.update_layout(
        title={
            'text': f'<b>{company}</b>',
            'x': 0.5,
            'font': {
                'size': 30
            }
        },
        xaxis=dict(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=rangeselector_buttons,
                bgcolor='lightblue',
                activecolor='darkblue',
                yanchor='top',
                y=-0.4
            ),
            showgrid=True,
            gridcolor=axis_config['gridcolor'],
            gridwidth=axis_config['gridwidth'],
            tickformat=axis_config['tickformat'],
            autorange=True  # Enable dynamic range for x-axis
        ),
        yaxis=dict(
            gridcolor=axis_config['gridcolor'],
            gridwidth=axis_config['gridwidth'],
            tickformat=axis_config['tickformat_y'],
            showgrid=True,
            autorange=True  # Enable dynamic range for y-axis
        ),
        height=chart_height,
        width=chart_width
    )

    return fig

# Apply custom CSS
apply_custom_css()
apply_custom_css()
# Define columns for chart type, date range, and indicator selection

company = st.sidebar.selectbox("Select company", df['stock_symbol'].unique())
col1, col2, col3 = st.columns(3)

with col1:
    chart_type = st.selectbox("Chart Type", ["Bar Chart", "Candlestick Chart", "Line Chart", "Area Chart"], key="chart_type_select")

with col2:
    date_range = st.date_input("Date Range", [df['date'].min(), df['date'].max()], key="date_range_input")

with col3:
    indicator = st.selectbox("Indicator", [None, "SMA", "EMA", "Bollinger Bands", "Keltner Channels", "Envelopes", "Average True Range (ATR)", "Price Channels"], key="indicator_select")

# Convert date_range to datetime64
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# Filter the dataframe based on selection
filtered_df = df[(df['stock_symbol'] == company) & (df['date'] >= start_date) & (df['date'] <= end_date)]
chart = create_chart(filtered_df, chart_type, indicator)

# Display the chart using Plotly
st.plotly_chart(chart, use_container_width=True)

if st.button("Start Session", key="start_session_button"):
    # Add your condition or action here
    st.write("Session started!")
