import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from matplotlib import rc

# 한글 폰트 설정
rc("font", family="AppleGothic")  # macOS
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 기호 깨짐 방지


def createDatabase():
    # 업로드된 CSV 파일을 불러옵니다
    file1_path = (
        "../data/2024-2 SDGs 수집파일 - T9_IndustryInnovationInfrastruc.csv"
    )
    # file2_path = "data/2024-2 SDGs 수집파일 - T8_EconomicGrowthIndicators_202.csv"

    # CSV 파일을 로드하고 인덱스 리셋
    data1 = pd.read_csv(file1_path, index_col=None)
    # data2 = pd.read_csv(file2_path, index_col=None)

    # 데이터셋에서 첫 두 행을 제거합니다
    data1 = data1.iloc[2:].reset_index(drop=True)
    # data2 = data2.iloc[2:].reset_index(drop=True)

    data1 = data1.drop("지자체", axis=1)
    # data2 = data2.drop("지자체", axis=1)

    # 모든 값이 결측치인 열을 제거합니다
    data1_cleaned = data1.dropna(axis=1, how="all")
    # data2_cleaned = data2.dropna(axis=1, how="all")

    # 숫자만 있는 열을 int로 변환
    for column in data1_cleaned.select_dtypes(include=["float64", "int64"]).columns:
        if (data1_cleaned[column] % 1 == 0).all():
            data1_cleaned.loc[:, column] = data1_cleaned[column].astype("int")

    # for column in data2_cleaned.select_dtypes(include=["float64", "int64"]).columns:
    #     if (data2_cleaned[column] % 1 == 0).all():
    #         data2_cleaned.loc[:, column] = data2_cleaned[column].astype("int")

    # SQLite 데이터베이스에 연결합니다
    conn = sqlite3.connect("../data/sdgs_data.db")

    # 정리된 데이터를 SQLite 데이터베이스에 저장합니다
    data1_cleaned.to_sql(
        "T9_IndustryInnovationInfrastruc", conn, if_exists="replace", index=False
    )
    # data2_cleaned.to_sql(
    #     "T8_EconomicGrowthIndicators", conn, if_exists="replace", index=False
    # )

    conn.close()


def visualization():
    # SQLite 데이터베이스를 로드합니다
    db_path = "../data/sdgs_data.db"
    conn = sqlite3.connect(db_path)

    # 데이터베이스의 테이블을 데이터프레임으로 불러옵니다
    data1 = pd.read_sql_query("SELECT * FROM T9_IndustryInnovationInfrastruc", conn)
    # data2 = pd.read_sql_query("SELECT * FROM T8_EconomicGrowthIndicators", conn)

    conn.close()

    # 결측값 제거
    data1 = data1.dropna()
    data2 = data2.dropna()

    # T9_IndustryInnovationInfrastruc 데이터 시각화
    plt.figure(figsize=(10, 6))
    for column in data1.columns:
        if column != "년도":
            plt.plot(
                data1["년도"], data1[column], label=column, marker="o", linestyle="-"
            )

    plt.title("T9: 산업 혁신 인프라 - 데이터 전체 표시")
    plt.xlabel("년도")
    plt.ylabel("값")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()

    # # T8_EconomicGrowthIndicators 데이터 시각화
    # plt.figure(figsize=(10, 6))
    # for column in data2.columns:
    #     if column != "년도":
    #         plt.plot(
    #             data2["년도"], data2[column], label=column, marker="o", linestyle="-"
    #         )

    # plt.title("T8: 경제 성장 지표 - 데이터 전체 표시")
    # plt.xlabel("년도")
    # plt.ylabel("값")
    # plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    # plt.tight_layout()
    # plt.show()


if __name__ == "__main__":
    # createDatabase()
    visualization()
