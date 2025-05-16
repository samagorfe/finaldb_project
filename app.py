from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_connection():
    return sqlite3.connect('database.db')

# Landing page route
@app.route('/landing')
def landing():
    return render_template('landing.html')

# Main console page with SQL editor + dashboard button
@app.route('/', methods=['GET', 'POST'])
def index():
    results, headers, error = [], [], None
    sql = ""

    conn = get_connection()
    cursor = conn.cursor()

    # Dashboard metrics
    cursor.execute("SELECT COUNT(*) FROM USERPROFILE")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ROLEPOSTING")
    total_jobs = cursor.fetchone()[0]

    cursor.execute("SELECT ROUND(AVG(Grade), 2) FROM INTERVIEW")
    avg_grade = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM SALARYPAYMENT")
    total_payments = cursor.fetchone()[0]

    cursor.execute("SELECT AppType FROM View3 ORDER BY ItemsSold DESC LIMIT 1")
    top_app = cursor.fetchone()
    top_app_type = top_app[0] if top_app else "N/A"

    if request.method == 'POST':
        sql = request.form['sql']
        try:
            cursor.execute(sql)
            headers = [desc[0] for desc in cursor.description] if cursor.description else []
            results = cursor.fetchall()
        except Exception as e:
            error = str(e)

    conn.close()

    return render_template(
        'index.html',
        results=results,
        headers=headers,
        sql=sql,
        error=error,
        total_users=total_users,
        total_jobs=total_jobs,
        avg_grade=avg_grade,
        total_payments=total_payments,
        top_app_type=top_app_type
    )

@app.route('/tables')
def show_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return render_template('tables.html', tables=tables)

@app.route('/views')
def show_views():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
    views = [row[0] for row in cursor.fetchall()]
    conn.close()
    return render_template('views.html', views=views)

@app.route('/queries')
def show_queries():
    queries = [
        {"description": "Average Monthly Salary", "sql": "SELECT * FROM View1"},
        {"description": "Rounds Passed Per Job", "sql": "SELECT * FROM View2"},
        {"description": "App Types Sold Count", "sql": "SELECT * FROM View3"},
        {"description": "App Total Component Cost", "sql": "SELECT * FROM View4"},
    ]
    return render_template('queries.html', queries=queries)

@app.route('/dashboard')
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM USERPROFILE")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ROLEPOSTING")
    total_jobs = cursor.fetchone()[0]

    cursor.execute("SELECT ROUND(AVG(Grade), 2) FROM INTERVIEW")
    avg_grade = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM SALARYPAYMENT")
    total_payments = cursor.fetchone()[0]

    cursor.execute("SELECT AppType FROM View3 ORDER BY ItemsSold DESC LIMIT 1")
    top_app = cursor.fetchone()
    top_app_type = top_app[0] if top_app else "N/A"

    conn.close()

    return render_template(
        'dashboard.html',
        total_users=total_users,
        total_jobs=total_jobs,
        avg_grade=avg_grade,
        total_payments=total_payments,
        top_app_type=top_app_type
    )

@app.route('/run_query', methods=['POST'])
def run_query():
    sql = request.form['sql']
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        headers = [desc[0] for desc in cursor.description] if cursor.description else []
        results = cursor.fetchall()
    except Exception as e:
        conn.close()
        return render_template('query_result.html', error=str(e), results=[], headers=[], sql=sql)
    conn.close()
    return render_template('query_result.html', results=results, headers=headers, sql=sql)

if __name__ == '__main__':
    app.run(debug=True)
