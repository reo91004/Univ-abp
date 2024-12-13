import os
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Admin SDK 초기화
cred = credentials.Certificate("abp-sdgs-firebase-adminsdk-fbdul-bf15550536.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def upload_csv_to_firestore(file_path, collection_name):
    try:
        # CSV 파일을 로드하고 인덱스 리셋
        data = pd.read_csv(file_path, index_col=None)

        # 데이터셋에서 첫 두 행을 제거합니다
        data = data.iloc[2:].reset_index(drop=True)

        # '지자체' 열 제거
        data = data.drop("지자체", axis=1, errors="ignore")

        # 모든 값이 결측치인 열을 제거합니다
        data_cleaned = data.dropna(axis=1, how="all")

        # 숫자만 있는 열을 int로 변환
        for column in data_cleaned.select_dtypes(include=["float64", "int64"]).columns:
            if (data_cleaned[column] % 1 == 0).all():
                data_cleaned.loc[:, column] = data_cleaned[column].astype("int")

        # Firestore에 데이터를 업로드합니다
        collection_ref = db.collection(collection_name)
        for idx, row in enumerate(data_cleaned.iterrows(), start=1):
            doc_id = f"{idx:02}"  # 01부터 시작하는 고정 길이 ID 생성
            doc_data = row[1].to_dict()
            collection_ref.document(doc_id).set(doc_data)
            print(f"[{collection_name}] Document {doc_id} successfully written!")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


def upload_all_csv_files_to_firestore(data_dir):
    # 데이터 디렉토리 내의 모든 CSV 파일 탐색
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".csv"):
            file_path = os.path.join(data_dir, file_name)
            # 파일 이름에서 테이블 이름 생성
            collection_name = file_name.split(" - ")[-1].replace(".csv", "")
            upload_csv_to_firestore(file_path, collection_name)


if __name__ == "__main__":
    # 데이터 디렉토리 경로
    data_dir = "../data"

    # 모든 CSV 파일을 Firestore에 업로드
    upload_all_csv_files_to_firestore(data_dir)
