import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Load dữ liệu đã tiền xử lý
df = pd.read_csv("processed_student_data.csv")

# Chọn đầu vào (X) và đầu ra (y)
X = df.drop(columns=["G3"])
y = df["G3"]

# Chia tập dữ liệu thành train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình
model = LinearRegression()
model.fit(X_train, y_train)

# Lưu mô hình
joblib.dump(model, "student_score_model.pkl")

print("Mô hình đã được huấn luyện và lưu thành công!")
