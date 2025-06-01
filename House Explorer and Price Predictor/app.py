import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# from scipy.stats import zscore

# Loading and preprocessing the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("House Explorer and Price Predictor/house_dataset.csv")

    # Drop particular columns as it contains duplicate data
    df.drop(columns=['POSTED_BY','UNDER_CONSTRUCTION','RERA'], inplace=True)

    # Drop missing and malformed data
    df.dropna(subset=['TARGET(PRICE_IN_LACS)', 'SQUARE_FT', 'ADDRESS', 'BHK_NO.'], inplace=True)

    # Remove exact duplicate rows
    df.drop_duplicates(inplace=True)
    
    # Filter out rows with extremely high prices (price < 600 lacs)
    df = df[df['TARGET(PRICE_IN_LACS)'] < 600]
    
     # Filter out rows with extremely high bhks (bhk < 10)
    df = df[df['BHK_NO.'] < 10]
    
    # Filter out rows with extremely high land_area (area < 6000 sq_ft)
    df = df[df['SQUARE_FT'] < 6000]
    
    # Extract city from address
    df['CITY'] = df['ADDRESS'].apply(lambda x: x.strip().split(',')[-1].strip())

    # Price per sqft (for anomaly detection)
    # df['PRICE_PER_SQFT'] = df['TARGET(PRICE_IN_LACS)'] / df['SQUARE_FT']

    return df

df = load_data()

# Title
st.title("House Property Explorer & Price Predictor")

# Sidebar
mode = st.sidebar.radio("Choose Mode", ["Property Explorer", "Price Predictor"])

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

    # # Anomaly Detection: remove houses with outlier price/sqft
    # z_scores = zscore(filtered_df['PRICE_PER_SQFT'])
    # filtered_df = filtered_df[(np.abs(z_scores) < 2.5)]

    st.write(f"Found {len(filtered_df)} matching houses:")
    st.dataframe(filtered_df[['ADDRESS', 'BHK_NO.', 'SQUARE_FT', 'TARGET(PRICE_IN_LACS)', 'CITY']].head(10))



# Function 2: Predict the price
else:
    st.header("Price Predictor")

    input_city = st.selectbox("City", sorted(df['CITY'].unique()))
    input_bhk = st.selectbox("BHK (Bedrooms)", sorted(df['BHK_NO.'].unique()))
    input_area = st.number_input("Area (sqft)", min_value=300, max_value=5000, value=1000)

    new_df = df[df['CITY'] == input_city].copy()

    # Outlier removal based on SQUARE_FT and PRICE 
    # Remove top 10% from sqft and price
    sqft_threshold = new_df['SQUARE_FT'].quantile(0.90)
    price_threshold = new_df['TARGET(PRICE_IN_LACS)'].quantile(0.99)

    filtered_df = new_df[
        (new_df['SQUARE_FT'] <= sqft_threshold) &
        (new_df['TARGET(PRICE_IN_LACS)'] <= price_threshold)
    ]

    # Using Linear Regression 
    # Features and target
    X = filtered_df[['BHK_NO.', 'SQUARE_FT']]
    y = filtered_df['TARGET(PRICE_IN_LACS)']

    # Create a Linear regressor
    lm = LinearRegression()

    # Training the model  
    lm.fit(X, y)

    coeffs = lm.coef_
    a1, a2 = coeffs[0], coeffs[1]
    b1 = lm.intercept_

    # Model prediction on user_input data
    predicted_price = a1*input_bhk + a2*input_area + b1

    st.success(f"Predicted Price: ₹ {int(predicted_price):,} Lacs")


