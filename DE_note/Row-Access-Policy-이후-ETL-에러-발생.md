---
title: "Row Access Policy 이후 ETL 에러 발생"
date: 2026-04-28
type: DE
project: "-"
tags: [DE, work-log]
---

# Row Access Policy 이후 ETL 에러 발생

- [장애 현상]
- 전날 특정 계정이 사용할 Row Access Policy 정책 설정 이후 ETL 에러 다수 발생
- [원인]
- Row Access Policy : 테이블에 쿼리가 실행될 때 자동으로 Where 조건처럼 추가되는 보안 정책.
- 사용자, Role 에 따라서 볼 수 있는 Row 자체를 제한함.
* 전일 신규 계정(P_MAL) 생성 시 160개 테이블에 Row Access Policy를 일괄 적용하였음.
- 이 과정에서 ETL 계정(bidwetl)이 Policy 허용 조건에 포함되지 않아서 D002 데이터에 대한 Delete가 차단됨.
```sql
-- 기존 Policy
(enabled_role('D025_ROLE') AND COMP_CD = 'D025') OR enabled_role('dbadmin')
```
- ​위와 같은 Policy가 설정되어 있을 때 select * from table를 하게 된다면
```sql
SELECT * FROM table
WHERE (enabled_role('D025_ROLE') AND COMP_CD = 'D025') OR enabled_role('dbadmin')
```
- ​내부적으로 위 처럼 동작하게 된다.
* Grant Trusted 옵션 부재
- Grant Trusted가 설정되어 있을 경우 "이 계정은 신뢰할 수 있으니 보이지 않는 행에 DML을 시도해도 오류내지 말고 그냥 0건으로 처리해줘" 라는옵션이다.
- 원래 Policy에 Grant Trusted 옵션이 없었기 때문에, 조건에 포함되지 않은 계정이 DML 실행 시 오류 발생함.
- GRANT TRUSTED 없음
- 0건 반환
- 오류 발생 ← 오늘 케이스
- GRANT TRUSTED 있음
- 0건 반환
- 0건 처리 (오류 없음)
- [해결 및 조치]
- Row Access Policy의 허용 조건에 ETL Role을 추가하고, Grant Trusted 옵션을 함께 적용하여 ETL 계정이 전체 데이터에 대한 DML을 정상 수행할 수 있도록 해두었습니다.
```sql
(enabled_role('D025_ROLE') AND COMP_CD = 'D025') OR enabled_role('dbadmin')
OR enabled_role('bidwadm_co_etl_rl')   -- BIDWADM_CO 스키마
OR enabled_role('bidwadm_eis_etl_rl')  -- BIDWADM_EIS 스키마
OR enabled_role('bidwadm_etl_rl')       -- BIDWADM 스키마
```
- ​============
- Role : 권한의 묶음. 권한을 Role에 담고 -> Role을 사용자에게 부여하는 구조
- Policy : 테이블 단위로 적용

---

*DE | - | 2026-04-28*
