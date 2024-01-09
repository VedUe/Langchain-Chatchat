import json
import pymysql
import re
import sys
sys.path.append('/code/Langchain-Chatchat')
from configs import MYSQL_HOST

# 连接到MySQL数据库
conn = pymysql.connect(host=MYSQL_HOST, user='dockers_admin', password='gicdockers_admin', db='gemology', charset='utf8')
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

frh = open('mysql/output/idx2head.json', 'r')
frc = open('mysql/source/idx2content.json', 'r')

# 将JSON数据插入到表格中
for line in frh:
    j = json.loads(line)
    idx = j['idx']
    head = re.sub('"', '\\"', j['head'])
    head = re.sub("'", "\\'", head)
    update_sql = f'''
        UPDATE idx2head SET idx={idx}, head="{head}" WHERE idx={idx};
    '''
    print(update_sql)
    cursor.execute(update_sql)
    
jsonl = json.load(frc)
for j in jsonl:
    idx = j['idx']
    content = re.sub('"', '\\"', j['content'])
    content = re.sub("'", "\\'", content)
    update_sql = f'''
        UPDATE idx2content SET idx={idx}, content="{content}" WHERE idx={idx};
    '''
    print(update_sql)
    cursor.execute(update_sql)

# 提交事务
conn.commit()

# 关闭数据库连接
cursor.close()
conn.close()

fr = open('mysql/output/idx2head.json', 'r')
fw = open('knowledge_base/gems/content/heads.md', 'w')
l = []
for line in fr:
    j = json.loads(line)
    l.append(j['head'])
fw.writelines("【split】".join(l))