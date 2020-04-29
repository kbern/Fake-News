-- CREATE TABLE articles_per_domain_and_type(
--     domain ,
--     type ,
--     num_articles ,
-- )

CREATE articles_per_domain_and_type created_by(
    SELECT D.domain_url, T.type_name, COUNT(*)
    FROM Domain D, Webpage W, Article A, Typ T
    WHERE D.domain_id = W.domain_id
    AND A.article_id = W.article_id 
    AND A.type_id = T.type_id
    GROUP BY T.type_name, D.domain_url;

)

ALTER TABLE articles_per_domain_and_type
ADD CONSTRAINT domain_type PRIMARY KEY (DOMAIN_url, type_name)
