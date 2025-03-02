import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

def load_and_preprocess_data(filepath):
    df = pd.read_csv(filepath, sep=";")
    
    # Các cột cần mã hóa
    label_cols = ["school", "sex", "address", "famsize", "Pstatus", "Mjob", "Fjob", "reason", "guardian",
                  "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic"]
    
    for col in label_cols:
        df[col] = LabelEncoder().fit_transform(df[col])
    
    # Chuẩn hóa điểm số về thang điểm 10
    score_cols = ["G1", "G2", "G3"]
    df[score_cols] = df[score_cols] / 2  # Vì max 20, ta chia 2 để đưa về thang 10

    return df

if __name__ == "__main__":
    file_path = "./student/student-mat.csv"  
    df = load_and_preprocess_data(file_path)
    df.to_csv("processed_student_data.csv", index=False)
    print("Dữ liệu đã được tiền xử lý và lưu lại.")
