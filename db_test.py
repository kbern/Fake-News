import psycopg2
import pandas
try:
    connection = psycopg2.connect("host = localhost dbname = fakenews user = postgres password =12PRu7dh56")
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print (connection.get_dsn_parameters(),"\n")
    # Print PostgreSQL version
    cursor.execute(CREATE articles_per_domain_and_type (
    SELECT D.domain_url, T.type_name, COUNT(*)
    FROM Domain D, Webpage W, Article A, Typ T
    WHERE D.domain_id = W.domain_id
    AND A.article_id = W.article_id 
    AND A.type_id = T.type_id
    GROUP BY T.type_name, D.domain_url;
    )
    cursor.execute(ALTER TABLE articles_per_domain_and_type
ADD CONSTRAINT domain_type PRIMARY KEY (DOMAIN_url, type_name)
)
    connection.commit()
    
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")