import psycopg2
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

import re
import os

conn = psycopg2.connect("host = localhost dbname = fakenews_1m user = postgres password =12PRu7dh56")
cur = conn.cursor()

#query 2
cur.execute("""SELECT t.type_name, COUNT(DISTINCT d.domain_id)
            FROM Typ t, Domain d, Webpage w, Article a
            WHERE w.domain_id=d.domain_id
            AND w.article_id=a.article_id
            AND t.type_id=a.type_id
            GROUP BY t.type_name """)
#take the words similarity of the content of the articles


conn.commit()
# cur.execute(query)
rows = cur.fetchall()
df = pd.DataFrame(rows, columns=['type_name', 'count'])
df[['type_name', 'count']].plot.bar(x='type_name', y='count', rot=45, figsize=(5, 5))
plt.title('Distribution of types')
plt.xlabel('Type_name')
plt.ylabel('Counts')
plt.show()
#conn.close()


#query 1
cur.execute("""SELECT t.type_name, ROUND(COUNT(*)*100/SUM(COUNT(*)) over(), 2) as share 
FROM Typ t, Article a 
WHERE t.type_id=a.type_id 
GROUP BY t.type_id 
ORDER BY share DESC""")

conn.commit()


rows = cur.fetchall()
new_rows = []
for i in range(len(rows)):
    temp = []
    new_rows.append(temp)
    new_rows[i].append(rows[i][0])
    new_rows[i].append(float(rows[i][1]))
df = pd.DataFrame(new_rows, columns=['type_name','share'])

df[['type_name', 'share']].plot.bar(x='type_name', y='share', rot=45, figsize=(5, 5))
plt.title('Types by percentage')
plt.xlabel('type_name')
plt.ylabel('percentage')
# plt.show()

# plt.figure(figsize=(14,6))
# # plot chart
# ax1 = plt.subplot(111, aspect='equal')
# df.plot(kind='pie', y = 'share', ax=ax1, 
#  startangle=90, shadow=False, fontsize=14)
# labels = df['type_name']
# plt.legend(labels,loc='upper left', fontsize='small')


plt.show()
#conn.close()

#query 3
cur.execute("""SELECT d.domain_url, ROUND(COUNT(*)*100/SUM(COUNT(*)) OVER(), 2) as share 
FROM Domain d, Article a, Webpage w 
WHERE w.domain_id=d.domain_id 
AND w.article_id=a.article_id 
GROUP BY d.domain_url ORDER BY share DESC""")

conn.commit()
rows = cur.fetchall()
new_rows = []
for i in range(15):
    temp = []
    new_rows.append(temp)
    new_rows[i].append(rows[i][0])
    new_rows[i].append(float(rows[i][1]))
df = pd.DataFrame(new_rows, columns=['domain_url','share'])
df[['domain_url', 'share']].plot.bar(x='domain_url', y='share', rot=45, figsize=(5, 5))
plt.title('15 most common urls by percentage')
plt.xlabel('domain_url')
plt.ylabel('Percentage')
plt.show()
#conn.close()

#query 4
cur.execute("""SELECT d.domain_url, ROUND(COUNT(*)*100/SUM(COUNT(*)) OVER(), 2) as share
FROM Domain d, Article a, Webpage w, Typ t 
WHERE w.domain_id=d.domain_id 
AND w.article_id=a.article_id 
AND t.type_id = a.type_id 
AND t.type_name = 'fake' 
GROUP BY d.domain_url 
ORDER BY share DESC""")

conn.commit()
rows = cur.fetchall()
new_rows = []
for i in range(10):
    temp = []
    new_rows.append(temp)
    new_rows[i].append(rows[i][0])
    new_rows[i].append(float(rows[i][1]))
df = pd.DataFrame(new_rows, columns=['domain_url','share'])
df[['domain_url', 'share']].plot.bar(x='domain_url', y='share', rot=45, figsize=(5, 5))
plt.title('Percentage of fake articles per domain')
plt.xlabel('Domain_url')
plt.ylabel('Percentage of fake articles')
plt.show()
conn.close()