from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

# --- 配置 ---
app = Flask(__name__)
CORS(app) # 允许所有来源的跨域请求，方便开发

# 数据库连接信息 (请替换成你自己的)
DB_CONFIG = {
    'dbname': 'grade_system',
    'user': 'postgres',
    'password': 'czw0417Cc', # 替换成你的密码
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    """建立数据库连接"""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# --- API 路由 ---
@app.route('/api/grades/<student_id>', methods=['GET'])
def get_grades_by_student_id(student_id):
    grades = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT student_name, course_name, score FROM scores WHERE student_id = %s",
            (student_id,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return jsonify({'error': '未找到该学号的学生信息'}), 404

        for row in rows:
            grades.append({
                'student_name': row[0],
                'course_name': row[1],
                'score': row[2]
            })

        return jsonify(grades)

    except Exception as e:
        print(e)
        return jsonify({'error': '服务器内部错误'}), 500

# --- 启动服务 ---
if __name__ == '__main__':
    # host='0.0.0.0' 让局域网内其他设备也能访问
    app.run(host='0.0.0.0', port=5000, debug=True)
