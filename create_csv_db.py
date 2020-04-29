import os
import csv
import json

DIR2WRITE = './tables'
WRITEHEADER = False

def clean_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        data = []
        for row in reader:
            obj = {}
            for header, value in zip(headers, row):
                obj[header] = value
            data.append(obj)

        for obj in data:
            obj['authors'] = [author.strip().lower() for author in obj['authors'].split(',')]
            obj['tags'] = [tag.strip().lower() for tag in obj['tags'].split(',')]
            obj['keywords'] = [tag.strip().lower() for tag in obj['keywords'].split(',')]
            obj['meta_keywords'] = [mk.strip().lower() for mk in json.loads(obj['meta_keywords'].replace("'", '"'))]
    
    return data

def create_simple_tables(data):
    # in this method, we create tables which do not deepend on other tables
    # i.e. have no referential constraints
    def create_domain_table():
        domains = set()
        [domains.add(obj['domain']) for obj in data if obj['domain']]
        return { d: idx for idx, d in enumerate(list(domains))}

    def create_type_table():
        types = set()
        [types.add(obj['type']) for obj in data if obj['type']]
        return { t: idx for idx, t in enumerate(list(types))}

    def create_author_table():
        authors = set()
        [authors.add(author) for obj in data for author in obj['authors'] if author]
        return { a: idx for idx, a in enumerate(list(authors))}

    def create_keyword_table():
        keywords = set()
        [keywords.add(kw) for obj in data for kw in obj['keywords'] if kw]
        [keywords.add(mkw) for obj in data for mkw in obj['meta_keywords']if mkw]
        [keywords.add(t) for obj in data for t in obj['tags'] if t]
        return { kw: idx for idx, kw in enumerate(list(keywords))}
    
    def write(table, filename, header):
        with open(os.path.join(DIR2WRITE, filename), 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            if WRITEHEADER: writer.writerow(header)
            for item, idx in table.items():
                writer.writerow([idx, item])
    
    domains = create_domain_table()
    types = create_type_table()
    authors = create_author_table()
    keywords = create_keyword_table()

    write(domains, 'domain.csv', ['domain_id', 'domain_url'])
    write(types, 'type.csv', ['type_id', 'type_name'])
    write(authors, 'author.csv', ['author_id', 'author_name'])
    write(keywords, 'keyword.csv', ['keyword_id', 'keyword'])

    return domains, types, authors, keywords

def create_article_table(data, types):
    with open(os.path.join(DIR2WRITE, 'article.csv'), 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        if WRITEHEADER: writer.writerow(['article_id', 'title', 'content', 'summary', 'meta_description', 'type_id', 
            'updated_at', 'scraped_at', 'inserted_at'])
        for obj in data:
            writer.writerow([obj['id'], obj['title'], obj['content'], obj['summary'], obj['meta_description'], 
                types.get(obj['type'], ''), obj['updated_at'], obj['scraped_at'], obj['inserted_at']])

def create_webpage_table(data, domains):
    with open(os.path.join(DIR2WRITE, 'webpage.csv'), 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        if WRITEHEADER: writer.writerow(['url', 'article_id', 'domain_id'])
        for obj in data:
            writer.writerow([obj['url'], obj['id'], domains[obj['domain']]])

def create_tags_table(data, keywords):
    with open(os.path.join(DIR2WRITE, 'tags.csv'), 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        if WRITEHEADER: writer.writerow(['article_id', 'keyword_id'])
        for obj in data:
            for kw in obj['keywords']:
                if kw: writer.writerow([obj['id'], keywords[kw]])
            for mkw in obj['meta_keywords']:
                if mkw: writer.writerow([obj['id'], keywords[mkw]])
            for t in obj['tags']:
                if t: writer.writerow([obj['id'], keywords[t]])

def create_writtenby_table(data, authors):
    with open(os.path.join(DIR2WRITE, 'written_by.csv'), 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        if WRITEHEADER: writer.writerow(['article_id', 'author_id'])
        for obj in data:
            for author in obj['authors']:
                if author: writer.writerow([obj['id'], authors[author]])

if __name__ == '__main__':
    preproc_file = './processed-sample.csv'
    data = clean_data(preproc_file)
    domains, types, authors, keywords = create_simple_tables(data)
    create_article_table(data, types)
    create_webpage_table(data, domains)
    create_tags_table(data, keywords)
    create_writtenby_table(data, authors)