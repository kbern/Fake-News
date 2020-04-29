PORT=5432
DATABASE=fakenews_100k
ROOTPATH=/tmp/new_tables/

mkdir -p tables
python3 create_csv_db.py
psql -U postgres -p${PORT} -d ${DATABASE} -a -f create_schema.sql

psql -U postgres -p${PORT} -d ${DATABASE} -c "COPY Keyword FROM '${ROOTPATH}keyword.csv' delimiter ',' csv;"
psql -U postgres -p${PORT} -d ${DATABASE} -c "COPY Author FROM '${ROOTPATH}author.csv' delimiter ',' csv;"
psql -U postgres -p${PORT} -d ${DATABASE} -c "COPY Domain FROM '${ROOTPATH}domain.csv' delimiter ',' csv;"
psql -U postgres -p${PORT} -d ${DATABASE} -c "COPY Typ FROM '${ROOTPATH}type.csv' delimiter ',' csv;"
psql -U postgres -p${PORT} -d ${DATABASE} -c "COPY Article FROM '${ROOTPATH}article.csv' delimiter ',' csv;"
psql -U postgres -p${PORT} -d ${DATABASE} -c "COPY Webpage FROM '${ROOTPATH}webpage.csv' delimiter ',' csv;"
psql -U postgres -p${PORT} -d ${DATABASE} -c "COPY Tags FROM '${ROOTPATH}tags.csv' delimiter ',' csv;"
psql -U postgres -p${PORT} -d ${DATABASE} -c "COPY Written_by FROM '${ROOTPATH}written_by.csv' delimiter ',' csv;"
