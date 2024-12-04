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
    # data1 = data1.dropna()
    # data2 = data2.dropna()

    # 연도 범위 확인
    print("데이터에 포함된 연도:", data1["년도"].unique())

    # 연도 컬럼을 정수로 변환
    data1["년도"] = data1["년도"].astype(int)

    # 2012 ~ 2023년 전체 연도 생성
    full_years = pd.DataFrame({"년도": range(2012, 2024)})

    # 연도를 기준으로 데이터 병합 (결측치 포함)
    data1 = pd.merge(full_years, data1, on="년도", how="left")

    # 각 열에 대해 개별 차트 생성
    for column in data1.columns:
        if column != "년도":
            # 열 데이터를 숫자로 변환하며 오류 발생 시 NaN으로 처리
            data1[column] = pd.to_numeric(data1[column], errors="coerce")

            plt.figure(figsize=(12, 6))
            plt.plot(
                data1["년도"],
                data1[column],
                label=column,
                marker="o",
                linestyle="-",
                color="red",
            )
            plt.title(f"{column} - 데이터 시각화")
            plt.xlabel("년도")
            plt.ylabel("값")

            # y축 범위 설정: 데이터가 비어있지 않을 때만 실행
            if not data1[column].isna().all():
                y_min = data1[column].min() - 0.01
                y_max = data1[column].max() + 0.01
                plt.ylim(y_min, y_max)

            plt.legend(loc="upper left")
            plt.grid(True, linestyle="--", alpha=0.7)
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
    createDatabase()
    visualization()
