---
title: "Data Type 변경하기 || MSSQL VS Vertica"
date: 2026-05-06
type: DBA
project: "Data Type 변경하기"
tags: [DBA, work-log]
---

# Data Type 변경하기 || MSSQL VS Vertica

- Column의 Data type을 변경하기 위해선 어떤 과정이 필요할지, 또 DB별 어떤 차이가 있는지 알아보자.
- Vertica DB에서 한 컬럼의 Data type을
- Decimal (10,4) 에서 Decimal (20,4) 로 변경하기 위해서는 단순히 alter , set data type문으로는 해결되지 않는다.
- Vertica에서 아래 쿼리를 수행하면 실패한다.
```sql
ALTER TABLE TABLE_NAEM ALTER COLUMN_NAME SET DATA TYPE Numeric(20,4);
```
- ​반면에 MSSQL에서는 아래 쿼리를 수행하면 에러가 발생하지는 않는다.
```sql
ALTER TABLE TABLE_NAME
ALTER COLUMN COLUMN_NAME NUMERIC(20,4);
```
- ​
- 왜 이런 문제가 일어나냐면, 구조적으로 차이가 있기 때문이다.
- MSSQL은 데이터 저장을 행(Row)기반으로 한다.
- => 지금의 케이스처럼 Decimal(10,4) -> Decimal(20,4)로 크기를 늘릴 때는 내부적으로 메타데이터만 변경하고
- 실제 데이터 변환을 안함.
- Vertica는 데이터 저장을 컬럼(Column) 기반으로 한다.
- =>컬럼 하나가 통째로 하나의 물리 파일임. 데이터 타입을 바꾸려면 그 파일 전체를 새로 써야하기 때문에 ALTER로 처리하는 기능이 없음

---

*DBA | Data Type 변경하기 | 2026-05-06*
