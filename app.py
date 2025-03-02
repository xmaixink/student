from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
from pymongo import MongoClient
from predict_score import predict_student_score

# Kết nối MongoDB
client = MongoClient("mongodb+srv://vuhoangson3000:123456789Son@cluster0.we2k3.mongodb.net/")
db = client["student_db"]
collection = db["predictions"]

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Gọi model dự đoán điểm G3
        prediction = predict_student_score(data)

        # Đảm bảo prediction luôn là số
        if isinstance(prediction, dict):
            prediction = prediction.get("predicted_G3", 0)

        predicted_G3 = float(prediction)  # Ép kiểu số để so sánh chính xác

        # Xác định mức độ rủi ro
        risk_level = "Cao" if predicted_G3 < 5 else "Thấp"

        # Gợi ý cải thiện
        suggestion = "Bạn cần học lớp phụ đạo" if risk_level == "Cao" else "Tiếp tục duy trì phong độ"

        # Debug kiểm tra giá trị
        print(f"Dự đoán G3: {predicted_G3}, Kiểu dữ liệu: {type(predicted_G3)}")
        print(f"Mức độ rủi ro: {risk_level}")

        # Lưu vào MongoDB
        record = {
            "age": data.get("age"),
            "studytime": data.get("studytime"),
            "absences": data.get("absences"),
            "failures": data.get("failures"),
            "G1": data.get("G1"),
            "G2": data.get("G2"),
            "predicted_G3": predicted_G3,
            "risk_level": risk_level,
            "suggestion": suggestion
        }
        collection.insert_one(record)

        return jsonify(record)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/history", methods=["GET"])
def get_history():
    try:
        history = list(collection.find({}, {"_id": 0}))
        return jsonify(history)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/delete_history", methods=["POST"])
def delete_history():
    try:
        collection.delete_many({})
        return jsonify({"message": "Lịch sử dự đoán đã được xóa thành công!"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/history_page", methods=["GET"])
def history_page():
    try:
        history = list(collection.find({}, {"_id": 0}))

        # Cập nhật gợi ý cải thiện
        for record in history:
            record["suggestion"] = (
                "Bạn cần học lớp phụ đạo" if record.get("risk_level") == "Cao" else "Tiếp tục duy trì phong độ"
            )

        return render_template("history.html", history=history)
    except Exception as e:
        return f"Lỗi: {str(e)}"

@app.route("/predict_page", methods=["GET"])
def predict_page():
    return render_template("predict.html")

@app.route("/predict_web", methods=["POST"])
def predict_web():
    try:
        data = request.get_json()
        prediction = predict_student_score(data)

        # Nếu prediction là dictionary, lấy giá trị số
        if isinstance(prediction, dict):
            prediction = prediction.get("predicted_G3", 0)

        predicted_G3 = float(prediction)

        # Xác định mức độ rủi ro và gợi ý cải thiện
        risk_level = "Cao" if predicted_G3 < 5 else "Thấp"
        suggestion = "Bạn cần học lớp phụ đạo" if risk_level == "Cao" else "Tiếp tục duy trì phong độ"

        # Lưu vào MongoDB
        data["predicted_G3"] = predicted_G3
        data["risk_level"] = risk_level
        data["suggestion"] = suggestion
        collection.insert_one(data)

        return jsonify({
            "predicted_G3": predicted_G3,
            "risk_level": risk_level,
            "suggestion": suggestion
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=1910)
