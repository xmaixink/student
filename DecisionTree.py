import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import joblib

df = pd.read_csv("processed_student_data.csv")

X = df.drop(columns=["G3"])
y = df["G3"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "student_score_model.pkl")

print("Mô hình Decision Tree đã được huấn luyện và lưu thành công!")
