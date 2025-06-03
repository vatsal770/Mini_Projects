import streamlit as st
import pandas as pd
import requests

BASE_URL = 'http://127.0.0.1:8000'

End_Point = 'data'
# Get the Data from the /data endpoint
output = requests.get(BASE_URL+"/"+End_Point)
data = output.json()
df= pd.DataFrame(data)


# Title
st.title("House Property Explorer & Price Predictor")

# Sidebar
mode = st.sidebar.selectbox("Choose Mode", ["Property Explorer", "Price Predictor"])

# Function 1: Explore the houses from the dataset
if mode == "Property Explorer":
    st.header("Find Houses in your City")

    city = st.selectbox("City", sorted(df['CITY'].unique()))
    bhk = st.selectbox("BHK (Bedrooms)", sorted(df['BHK_NO.'].unique()))
    area = st.slider("Area (sqft)", int(df['SQUARE_FT'].min()), int(df['SQUARE_FT'].max()), (500, int(df['SQUARE_FT'].max())))
    price_range = st.slider("Price Range (₹)", int(df['TARGET(PRICE_IN_LACS)'].min()), int(df['TARGET(PRICE_IN_LACS)'].max()), (0, 50))

    filtered_df = df[
        (df['CITY'] == city) &
        (df['BHK_NO.'] == bhk) &
        (df['SQUARE_FT'] >= area[0]) & (df['SQUARE_FT'] <= area[1]) &
        (df['TARGET(PRICE_IN_LACS)'] >= price_range[0]) & (df['TARGET(PRICE_IN_LACS)'] <= price_range[1])
    ]

    st.write(f"Found {len(filtered_df)} matching houses:")
    st.dataframe(filtered_df[['ADDRESS', 'BHK_NO.', 'SQUARE_FT', 'TARGET(PRICE_IN_LACS)', 'CITY']].head(10))



# Function 2: Predict the price
else:
    st.header("Price Predictor")

    input_city = st.selectbox("City", ['Agra', 'Bangalore', 'Bhopal'])
    
    # input_bhk = st.slider("BHK (Bedrooms)", 1.0, 10.0, 1.0, 1.0)
    input_area = st.number_input("Area (sqft)", min_value=300, max_value=5000, value=1000)

    input_data = {
        "city": input_city,
        # "bhk": input_bhk,
        "area": input_area
    }
    # Get the predicted price from /predict endpoint
    End_Point = 'predict'
    output = requests.post(BASE_URL+'/'+End_Point, json=input_data)
    st.write(output)
    predicted_price = int(output.json()["predicted_price"])

    st.success(f"Predicted Price: ₹ {int(predicted_price):,} Lacs")


