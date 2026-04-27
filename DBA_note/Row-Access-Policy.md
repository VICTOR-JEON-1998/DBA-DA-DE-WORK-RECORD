---
title: "Row Access Policy"
date: 2026-04-27
type: DBA
project: "버티카 DB Row별 권한 제어 설정"
tags: [DBA, work-log]
---

# Row Access Policy

- Row Access Policy : 테이블 자체에 Row 필터 조건을 내장하여, 사용자/롤에 따라 조회 가능한 행을 자동으로 제한하는 DB 보안 기능
- DB: Vertica v24.2.0
- 회사코드 컬럼(COMP_CD)으로 법인 구분
- <CASE>
- 말레이시아 법인에서 말레이시아 관련 데이터들만 볼 수 있도록 조치해줘야함.
- 현재는 법인별로 테이블이 분리되어있지는 않고 테이블 하나에 여러 법인 데이터들이 모두 공존하고있음.
- => RAP를 사용하여 해결함.
- <장점>
- 테이블에 직접 정책을 내장 → 원본 테이블명 그대로 사용 가능
- 모든 쿼리에 자동 적용 → 관리 도구(DBeaver 등)에서도 동일하게 동작
- 신규 데이터 INSERT 시 별도 작업 없이 즉시 필터링 적용
- Role 기반으로 유연한 다중 조건 설정 가능
- <주의사항>
- 테이블당 Row Policy는 1개만 생성 가능
- 임시 테이블(Temp Table)에는 적용 불가
- COMP_CD 없는 테이블은 Policy 대신 권한 미부여로 차단
- 적용 방법
1. 계정 생성
```sql
CREATE USER P_MAL IDENTIFIED BY '비밀번호';
```
- ​
2. Role 생성
```sql
-- Role 생성
CREATE ROLE D025_ROLE;
-- 계정에 Role 부여
GRANT D025_ROLE TO P_MAL;
```
- ​
3. 테이블에 권한 부여
```sql
-- 스키마 접근 권한
GRANT USAGE ON SCHEMA BIDWADM     TO D025_ROLE;
GRANT USAGE ON SCHEMA BIDWADM_CO  TO D025_ROLE;
GRANT USAGE ON SCHEMA BIDWADM_EIS TO D025_ROLE;
-- 테이블 SELECT 권한 (개별 테이블)
GRANT SELECT ON TABLE BIDWADM_CO.OD_SP_SL_M TO D025_ROLE;
-- Access Policy 적용 (Row 필터링)
CREATE ACCESS POLICY ON BIDWADM_CO.OD_SP_SL_M
FOR ROWS WHERE (
ENABLED_ROLE('D025_ROLE') AND COMP_CD = 'D025'
) OR ENABLED_ROLE('dbadmin')
ENABLE;
```
- ​
4. 권한 활성화
```sql
-- P_MAL로 접속 후 Role 활성화
SET ROLE D025_ROLE;
-- 활성화 확인
SELECT ENABLED_ROLES();
-- 조회 테스트
SELECT DISTINCT COMP_CD FROM BIDWADM_CO.OD_SP_SL_M;
-- → D025만 나오면 정상
```
- ​

---

*DBA | 버티카 DB Row별 권한 제어 설정 | 2026-04-27*
