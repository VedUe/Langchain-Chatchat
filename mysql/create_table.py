import json
import pymysql
import re

# 连接到MySQL数据库
conn = pymysql.connect(host='172.17.0.3', user='dockers_admin', password='gicdockers_admin', db='gemology', charset='utf8')
cursor = conn.cursor()

# 创建表格（如果不存在）
create_table_sql1 = '''
CREATE TABLE IF NOT EXISTS idx2head (
    idx INT primary key,
    head TEXT(4096));
'''
create_table_sql2 = '''
CREATE TABLE IF NOT EXISTS idx2content (
    idx INT primary key,
    content text(4096));
'''
cursor.execute(create_table_sql1)
cursor.execute(create_table_sql2)

frh = open('mysql/source/idx2head.json', 'r')
frc = open('mysql/source/idx2content.json', 'r')
# 将JSON数据插入到表格中
jsonl = json.load(frh)
for j in jsonl:
    idx = j['idx']
    head = re.sub('"', '\\"', j['head'])
    head = re.sub("'", "\\'", head)
    insert_sql = f'''
INSERT INTO idx2head (idx, head) VALUES ({idx}, "{head}");
    '''
    print(insert_sql)
    cursor.execute(insert_sql)
    
jsonl = json.load(frc)
for j in jsonl:
    idx = j['idx']
    content = re.sub('"', '\\"', j['content'])
    content = re.sub("'", "\\'", content)
    insert_sql = f"""
INSERT INTO idx2content (idx, content) VALUES ({idx}, '{content}');
    """
    print(insert_sql)
    cursor.execute(insert_sql)

# 提交事务
conn.commit()

# 关闭数据库连接
cursor.close()
conn.close()
