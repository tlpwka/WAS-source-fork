import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load the data from the CSV file
df = pd.read_csv('data.csv')

# Step 1: Compute Derived Variables Based on the Formula
# Travel Time
df['Travel_time'] = (df['Range'] / ((df['Speed'] / 3600 * 16 * 256) / (74 * 2) * 24 / 10 * 2) + 12)
df['ge_travel_time'] = np.floor(df['Travel_time'] * 0.4)

# Time Factor
df['Time_factor'] = np.maximum(
    31,
    np.where(
        df['ge_travel_time'] <= 0,
        255,
        np.where(
            (0 < df['ge_travel_time']) & (df['ge_travel_time'] <= 24),
            255 - (df['ge_travel_time'] - 0),
            255 - 2 * (df['ge_travel_time'] - 0) + 24
        )
    )
)

# Income Per Travel
df['Income_per_travel'] = (df['Capacity'] * df['Range'] * 3185 * df['Time_factor']) / (2 ** 21)

# Annual Travels
df['Annual_travels'] = 365 / df['Travel_time']

# Annual Profit
df['Annual_profit'] = df['Income_per_travel'] * df['Annual_travels']

# Calculated Cost
df['Calculated_Cost'] = df['In_game_life'] * df['Annual_profit'] * 0.25

# Step 2: Validate Correlation Between Provided Cost and Calculated Cost
correlation = df[['Cost', 'Calculated_Cost']].corr()
print("Correlation between actual and calculated costs:")
print(correlation)

# Step 3: Prepare Features for Regression
X = df[['In_game_life', 'Annual_profit']]
X = sm.add_constant(X)  # Add intercept term
y = df['Cost']

# Step 4: Fit Regression Model
model = sm.OLS(y, X).fit()

# Step 5: Display Summary
print(model.summary())

# Step 6: Predict Cost for New Data
new_data = pd.DataFrame({
    'Speed': [1020],
    'Capacity': [721],
    'Range': [2500],
    'In_game_life': [20]
})

# Compute Derived Variables for New Data
new_data['Travel_time'] = (new_data['Range'] / ((new_data['Speed'] / 3600 * 16 * 256) / (74 * 2) * 24 / 10 * 2) + 12)
new_data['ge_travel_time'] = np.floor(new_data['Travel_time'] * 0.4)
new_data['Time_factor'] = np.maximum(
    31,
    np.where(
        new_data['ge_travel_time'] <= 0,
        255,
        np.where(
            (0 < new_data['ge_travel_time']) & (new_data['ge_travel_time'] <= 24),
            255 - (new_data['ge_travel_time'] - 0),
            255 - 2 * (new_data['ge_travel_time'] - 0) + 24
        )
    )
)
new_data['Income_per_travel'] = (new_data['Capacity'] * new_data['Range'] * 3185 * new_data['Time_factor']) / (2 ** 21)
new_data['Annual_travels'] = 365 / new_data['Travel_time']
new_data['Annual_profit'] = new_data['Income_per_travel'] * new_data['Annual_travels']

# Prepare Data for Prediction
new_data['const'] = 1
predicted_cost = model.predict(new_data[['const', 'In_game_life', 'Annual_profit']])
print("Predicted Cost:", predicted_cost[0])

