from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd

app = Flask(__name__)
CORS(app)  # 모든 경로에 대해 CORS 허용


@app.route("/data")
def get_data():
    # SQLite 데이터베이스 연결
    conn = sqlite3.connect("../data/sdgs_data.db")
    data = pd.read_sql_query("SELECT * FROM T9_IndustryInnovationInfrastruc", conn)
    conn.close()

    # 데이터를 JSON으로 변환하여 반환
    return jsonify(data.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
