### 용량분석

<img width="935" height="327" alt="image" src="https://github.com/user-attachments/assets/63920985-1388-46ae-9b54-dbaf8bf30f2b" />

```sql

SELECT 
    pg_size_pretty(pg_total_relation_size('items')) AS total_size,
    pg_size_pretty(pg_relation_size('items')) AS table_size,
    pg_size_pretty(pg_total_relation_size('items') - pg_relation_size('items')) AS index_size,
    (pg_relation_size('items') / 10000) || ' bytes' AS avg_row_size
;

```

---

### R&D

“10만 건의 1536차원 벡터 데이터를 인덱스 없이 검색하면, DB는 모든 데이터를 메모리에 올려야 하므로 **t3.micro의 1GB RAM 환경에서는 과도한 I/O와 버퍼 교체**가 발생할 것이다."
시

- 실행계획 분석

<img width="849" height="876" alt="image" src="https://github.com/user-attachments/assets/71fa58f1-982f-4871-af5f-21124e031a6d" />

```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
WITH query_vec AS (
    -- 가상의 쿼리 벡터 하나 생성
    SELECT array_agg(random())::vector(1536) as q_emb 
    FROM generate_series(1, 1536)
)
SELECT id, embedding <=> (SELECT q_emb FROM query_vec) as distance
FROM items
ORDER BY distance ASC
LIMIT 5;

-----

Limit  (cost=388.17..388.19 rows=5 width=16) (actual time=55.135..55.139 rows=5 loops=1)
  Output: items.id, ((items.embedding <=> (InitPlan 2).col1))
  Buffers: shared hit=30077
  CTE query_vec
    ->  Aggregate  (cost=23.04..23.06 rows=1 width=32) (actual time=1.403..1.404 rows=1 loops=1)
          Output: (array_agg(random()))::vector(1536)
          ->  Function Scan on pg_catalog.generate_series  (cost=0.00..15.36 rows=1536 width=0) (actual time=0.094..0.191 rows=1536 loops=1)
                Output: generate_series.generate_series
                Function Call: generate_series(1, 1536)
  InitPlan 2
    ->  CTE Scan on query_vec  (cost=0.00..0.02 rows=1 width=32) (actual time=1.407..1.407 rows=1 loops=1)
          Output: query_vec.q_emb
  ->  Sort  (cost=365.10..390.10 rows=10000 width=16) (actual time=55.134..55.134 rows=5 loops=1)
        Output: items.id, ((items.embedding <=> (InitPlan 2).col1))
        Sort Key: ((items.embedding <=> (InitPlan 2).col1))
        Sort Method: top-N heapsort  Memory: 25kB
        Buffers: shared hit=30077
        ->  Seq Scan on public.items  (cost=0.00..199.00 rows=10000 width=16) (actual time=1.444..53.321 rows=10000 loops=1)
              Output: items.id, (items.embedding <=> (InitPlan 2).col1)
              Buffers: shared hit=30074
Query Identifier: -2423508547675002591
Planning:
  Buffers: shared hit=19 read=1
  I/O Timings: shared read=0.664
Planning Time: 0.858 ms
Execution Time: 56.031 ms
```
