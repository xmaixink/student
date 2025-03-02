import joblib
import numpy as np

# Load mô hình đã huấn luyện
model = joblib.load("student_score_model.pkl")

# Danh sách đầy đủ các đặc trưng đã dùng để huấn luyện mô hình
FEATURES = [
    "school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu",
    "Mjob", "Fjob", "reason", "guardian", "traveltime", "studytime", "failures",
    "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet",
    "romantic", "famrel", "freetime", "goout", "Dalc", "Walc", "health",
    "absences", "G1", "G2"
]

def predict_student_score(data):
    try:
        # Điền giá trị mặc định = 0 cho những đặc trưng còn thiếu
        input_data = [data.get(feature, 0) for feature in FEATURES]
        input_data = np.array([input_data]).astype(float)

        # Dự đoán điểm số G3
        predicted_G3 = model.predict(input_data)[0]

        # Giới hạn giá trị dự đoán trong khoảng [0, 10]
        predicted_G3 = max(0, min(10, predicted_G3))

        # Xác định mức độ rủi ro và gợi ý cải thiện
        if predicted_G3 < 5:
            risk_level = "Cao"
            suggestion = "Bạn cần học lớp phụ đạo"
        elif predicted_G3 < 10:
            risk_level = "Thấp"
            suggestion = "Tiếp tục duy trì"
        else:
            risk_level = "Không có"
            suggestion = "Xuất sắc, hãy giữ vững phong độ"

        # Trả về kết quả dự đoán
        return {
            "predicted_G3": round(predicted_G3, 2),
            "risk_level": risk_level,
            "suggestion": suggestion
        }
    except Exception as e:
        return {"error": str(e)}

# Kiểm tra chạy thử nếu file này được chạy trực tiếp
if __name__ == "__main__":
    test_input = {
        "school": 1,
        "sex": 0,
        "age": 17,
        "studytime": 3,
        "absences": 5,
        "failures": 1,
        "G1": 7,
        "G2": 8
    }

    result = predict_student_score(test_input)
    print(result)
