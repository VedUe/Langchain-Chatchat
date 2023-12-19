import pymysql

conn = pymysql.connect(host='172.17.0.3', user='dockers_admin', password='gicdockers_admin', db='gemology', charset='utf8')
cursor = conn.cursor()

# sql = f'select idx from idx2head where head=%(head)s'
# cursor.execute(sql, {'head' :"刚玉 红宝石、蓝宝石的基本性质及产状 光性"})
# results = cursor.fetchall()
# idxs = [results[i][0] for i in range(len(results))]
# print(idxs)

sql = f'select content from idx2content where idx=%(idx)s'
cursor.execute(sql, {'idx': 2}) 
print(cursor.fetchone()[0])