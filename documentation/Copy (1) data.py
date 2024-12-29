import pandas as pd
import statsmodels.api as sm

# Load the data from the CSV file
df = pd.read_csv('data.csv')

# Display the first few rows to make sure the data is loaded correctly
print(df.head())
print(f"Total rows in dataset: {len(df)}")
# Independent variables (X) - speed, capacity, range, in-game life
X = df[['Speed', 'Capacity', 'Range', 'In_game_life']]
#X = df[['Capacity', 'ge_travel_time', 'In_game_life']]

# Add a constant to the independent variables (for the intercept in the regression equation)
X = sm.add_constant(X)

# Dependent variable (Y) - Buying Cost
y = df['Cost']

# Fit the regression model
model = sm.OLS(y, X).fit()

# Print the summary of the regression results
print(model.summary())

# Let's predict the Buying Cost for new data (example)
new_data = pd.DataFrame({
    'const': [1],  # The intercept term
    'Speed': [1020],  # Example new data
    'Capacity': [721],
    'Range': [2500],
  #  'ge_travel_time': [26],
    'In_game_life': [20]
})

# Predict the Buying Cost for the new data
predicted_cost = model.predict(new_data)
print("Predicted Cost:", predicted_cost[0])

