import pandas as pd
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# loading endpoint
@app.get("/data")
def load_data():
    df = pd.read_csv("C:/Users/vatsal trivedi/Documents/VS Code/Mini_Projects/Datasets/house_dataset.csv")
    # Drop missing and malformed data
    df.dropna(subset=['TARGET(PRICE_IN_LACS)', 'SQUARE_FT', 'ADDRESS', 'BHK_NO.'], inplace=True)

    # Drop particular columns as it contains duplicate data
    df.drop(columns=['POSTED_BY','UNDER_CONSTRUCTION','RERA'], inplace=True)

    # Remove exact duplicate rows
    df.drop_duplicates(inplace=True)

    # Filter out rows with extremely high prices (price < 400 lacs)
    df = df[df['TARGET(PRICE_IN_LACS)'] < 300]

    # Filter out rows with extremely high bhks (bhk < 6)
    df = df[df['BHK_NO.'] < 6]

    # Filter out rows with extremely high prices (price < 400 lacs)
    df = df[df['SQUARE_FT'] < 3000]

    # Extract city from address
    df['CITY'] = df['ADDRESS'].apply(lambda x: x.strip().split(',')[-1].strip())

    # Price per sqft (for anomaly detection)
    df['PRICE_PER_SQFT'] = df['TARGET(PRICE_IN_LACS)'] / df['SQUARE_FT']
    print('f"C:/Users/vatsal trivedi/Documents/VS Code/Mini_Projects/Models/.pkl')
    return df.to_dict()
    

class Input(BaseModel):
    city: str
    area: float

# prediction endpoint
@app.post("/predict")
async def predict(data: Input):
    path = f"C:/Users/vatsal trivedi/Documents/VS Code/Mini_Projects/Models/{data.city}.pkl"
    with open(path, 'rb') as f:
        model = pickle.load(f)
    a1 = float(model.coef_[0])
    b1 = model.intercept_

    predicted_price = a1*data.area + b1
    print(predicted_price)
    return {"predicted_price": predicted_price}


