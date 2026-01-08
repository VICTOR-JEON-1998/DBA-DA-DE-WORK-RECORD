### AWS RDS

![image.png](attachment:3107ad68-676f-4cd4-a0a8-005c94ac197e:image.png)

연결은 MY IP 만 접근 가능하도록 설정 후에 DB연결 완료하였다.

## PGVector 설치 + 랜덤데이터 생성

![image.png](attachment:130c78bf-1e7f-4a40-99e3-e1b5131ea2a2:image.png)

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
