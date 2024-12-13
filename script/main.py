import os
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from matplotlib import rc

# 한글 폰트 설정
rc("font", family="AppleGothic")  # macOS
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 기호 깨짐 방지


def process_and_store_csv(file_path, table_name, db_path):
    try:
        # CSV 파일을 로드하고 인덱스 리셋
        data = pd.read_csv(file_path, index_col=None)

        # 데이터셋에서 첫 두 행 제거 및 인덱스 리셋
        data = data.iloc[2:].reset_index(drop=True)

        # 특정 열 제거 (예: '지자체')
        if "지자체" in data.columns:
            data = data.drop("지자체", axis=1)

        # 모든 값이 결측치인 열 제거
        data_cleaned = data.dropna(axis=1, how="all")

        # 숫자만 있는 열을 int로 변환
        for column in data_cleaned.select_dtypes(include=["float64", "int64"]).columns:
            if (data_cleaned[column] % 1 == 0).all():
                data_cleaned.loc[:, column] = data_cleaned[column].astype("int")

        # SQLite 데이터베이스에 연결
        conn = sqlite3.connect(db_path)

        # 데이터 저장
        data_cleaned.to_sql(table_name, conn, if_exists="replace", index=False)

        conn.close()
        print(f"'{file_path}' 파일의 데이터를 '{table_name}' 테이블에 저장 완료.")
    except Exception as e:
        print(f"파일 처리 중 오류 발생: {file_path}. 오류: {e}")


def create_database_from_files(data_dir, db_path):
    # 데이터 디렉토리 내의 모든 CSV 파일 탐색
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".csv"):
            file_path = os.path.join(data_dir, file_name)
            table_name = file_name.split(" - ")[-1].replace(".csv", "")
            process_and_store_csv(file_path, table_name, db_path)


if __name__ == "__main__":
    # 데이터 디렉토리 경로 및 데이터베이스 경로
    data_dir = "../data"
    db_path = "../data/sdgs_data.db"

    # 모든 CSV 파일을 데이터베이스에 저장
    create_database_from_files(data_dir, db_path)
