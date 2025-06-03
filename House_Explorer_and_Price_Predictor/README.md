# House Explorer & Price Predictor

An interactive **Streamlit app** which lets users explore house listings by city, area, BHK, and price range — and also predict the price of a new property based on BHK, area, and city using a regression technique.

---

## Features

- **Dual Interface**:
  - **Property Explorer**: Filter houses by city, BHK, area, and price.
  - **Price Predictor**: Predict price based on BHK, area, and location.
- **Data Cleaning**:
  - Removes invalid/missing entries and filters extreme values.
- **ML Model**:
  - Trains a Linear Regression model dynamically based on city-specific listings.

---

## Tech Used

- Python
- Streamlit
- Pandas & NumPy
- Scikit-learn (for Regression)
- Jupyter Notebook (for Data Analysis)

---

## Dataset Preprocessing

- Drops irrelevant or duplicate columns: `POSTED_BY`, `UNDER_CONSTRUCTION`, `RERA`
- Extracts city names from full addresses
- Removes missing values and duplicates
- Filters invalid data (e.g., price > 600 Lacs, BHK > 10, area > 6000 sqft)

---

## Setup Instructions

1. **Clone the Repo**

```bash
git clone https://github.com/vatsal770/Mini_Projects.git
cd House Explorer and Price Predictor
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the App**
```bash
streamlit run app.py
```

---

## Sample of the App:

![Sample App Screenshot](Sample_App.png)

---

## Dataset Visualizer (Notebook)
I have included a Jupyter Notebook to help understand the data visually.

---

---

