from flask import Flask, render_template, request, redirect, url_for
import boto3
import pymysql
import json
import os

app = Flask(__name__, template_folder='/var/www/html/templates')

def get_db_connection():
    # パラメータストアから値を取得
    ssm_client = boto3.client('ssm')
    secret_id = ssm_client.get_parameter(Name='/rds/secret')['Parameter']['Value']
    host = ssm_client.get_parameter(Name='/rds/host')['Parameter']['Value']
    
    # Secrets ManagerからDB接続情報を取得
    secrets_client = boto3.client('secretsmanager')
    secret_value = secrets_client.get_secret_value(SecretId=secret_id)
    secret = json.loads(secret_value['SecretString'])
    
    connection = pymysql.connect(
        host=host,
        user=secret['username'],
        password=secret['password'],
        database='memo_db',
        charset='utf8mb4'
    )
    return connection

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, content FROM memos ORDER BY id DESC')
    memos = cursor.fetchall()
    conn.close()
    return render_template('index.html', memos=memos)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO memos (title, content) VALUES (%s, %s)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/edit/<int:memo_id>', methods=['GET', 'POST'])
def edit(memo_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute('UPDATE memos SET title = %s, content = %s WHERE id = %s', (title, content, memo_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute('SELECT id, title, content FROM memos WHERE id = %s', (memo_id,))
    memo = cursor.fetchone()
    conn.close()
    return render_template('edit.html', memo=memo)

@app.route('/delete/<int:memo_id>')
def delete(memo_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM memos WHERE id = %s', (memo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)