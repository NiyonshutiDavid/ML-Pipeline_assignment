import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

# Load and prepare data
df = pd.read_csv('data/heart.csv')
X = df[['Age', 'Cholesterol', 'RestingBP']]
y = df['HeartDisease']

# Train and save model
model = LogisticRegression()
model.fit(X, y)
joblib.dump(model, 'model/heart_model.pkl')