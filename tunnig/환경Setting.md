### AWS RDS

<img width="916" height="765" alt="image" src="https://github.com/user-attachments/assets/ea31c806-fd25-4d6c-b1a5-d48c6b69b8e5" />

연결은 MY IP 만 접근 가능하도록 설정 후에 DB연결 완료하였다.

## PGVector 설치 + 랜덤데이터 생성

<img width="916" height="765" alt="image" src="https://github.com/user-attachments/assets/e67f4d06-1f0d-4971-beb0-4f4872723fb4" />

```sql
CREATE EXTENSION IF NOT EXISTS vector;

drop table if exists items;

CREATE TABLE items (
    id bigserial PRIMARY KEY,
    content text,                  -- 실제 텍스트가 들어갈 곳 (이번엔 비워둠)
    embedding vector(1536)         -- 핵심: 1536개의 숫자가 들어갈 벡터 컬럼
);

--- 의미없는 랜덤 백터 1만개 생성

INSERT INTO items (embedding)
SELECT array_agg(random())::vector(1536)
FROM generate_series(1, 10000) AS id_gen  -- 1만 행 생성
CROSS JOIN generate_series(1, 1536) AS dim_gen -- 각 행당 1536개 차원 생성
GROUP BY id_gen;

SELECT id, embedding 
FROM items 
LIMIT 5;
```
