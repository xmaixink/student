import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("processed_student_data.csv")

# Hiển thị thống kê mô tả
print(df.describe())

# Vẽ biểu đồ phân bố điểm G3
sns.histplot(df["G3"], bins=10, kde=True)
plt.xlabel("G3 (Thang điểm 10)")
plt.ylabel("Tần suất")
plt.title("Phân bố điểm số G3")
plt.show()
