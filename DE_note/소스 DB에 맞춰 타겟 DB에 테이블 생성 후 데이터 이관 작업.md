BIDW 구매발주(PO) 데이터 이관 작업 — 2026.07.24
1. 배경
ERP(MSSQL) 구매발주(PO) 관련 테이블 14건을 BIDW(Vertica)
BIDWADM_CO
스키마로 이관 요청받음.
2. 존재 여부 확인
v_catalog.tables
/
v_catalog.views
로 Vertica 기 존재 여부 조회
14건 중
1건(
OD_PO_PRCH_ESTM_M
)만 이미 존재
, 나머지 13건 신규 생성 필요
이름 매칭 시 완전 일치가 아니라
원본명 앞에
OD_
접두사가 붙는 네이밍 규칙
확인 후 정확 매칭으로 전환
3. 원본 스키마 이슈 해결
PO_PRCH_ESTM_WRK_MTRL_COST_M
(요청명)이 ERP에 실제로는 존재하지 않음을 확인
LIKE
검색으로 실제 테이블명이
PO_PRCH_ESTM_MTRL_COST_M
(WRK 없음)임을 특정
dbo
/
SETUP
두 스키마에 동일명 테이블(
PDITEM_M
,
PDITEM_SIZE_M
)이 존재하는 경우 발견 →
dbo
기준으로 확정
하여 진행
4. Vertica DDL 생성
INFORMATION_SCHEMA.COLUMNS
기반으로 MSSQL 원본 컬럼 스펙(타입/길이/precision/scale/nullable) 추출
MSSQL → Vertica 타입 매핑 규칙 수립 (char/varchar/nvarchar/numeric/datetime 등)
문자형(CHAR/VARCHAR) 길이 및 NUMERIC precision을 원본 대비 3배로 확장
하는 규칙 적용 (datetimeoffset → TIMESTAMPTZ, datetime → TIMESTAMP)
13개 테이블 CREATE TABLE DDL 작성 → Vertica 실행 완료
5. DataStage ETL 잡 구성
잡명:
m_OD_P_STG_a01
Source(MSSQL) → Transformer → Target(Vertica) 구조로
13개 테이블 개별 잡
구성
처리 방식:
Full Load (Truncate 후 재적재)
잡 실행 완료, 각 잡별 처리 건수 확인

![image_1](images/소스 DB에 맞춰 타겟 DB에 테이블 생성 후 데이터 이관 작업-1.png)

6. 결과 검증
Vertica 실제 생성 컬럼 수를
v_catalog.columns
로 재조회하여 ERP 원본과 1:1 대조 →
전체 일치 확인
적재 결과:
테이블명
컬럼 수
적재 건수
PO_LBL_PO_D
26
0
PO_LBL_PO_M
28
0
PO_PRCH_ESTM_WRK_COST_M
19
15,722
PO_PRCH_ESTM_MTRL_COST_M
20
159,888
PO_STYL_BOX_M
15
1,332
PO_STYL_PO_ASSORT_M
17
733,210
PO_STYL_PO_D_H
27
82
PO_STYL_PO_M_H
61
8
PO_STYL_PO_PDITEM_H
40
60
PO_STYL_PO_PDITEM_HTS_M
20
0
PO_STYL_PO_PDITEM_M
39
252,768
PO_STYL_PO_PDITEM_SIZE_H
21
82
PO_STYL_PO_PDITEM_SIZE_M
20
848,380
총 컬럼 353개 / 총 적재 2,011,532건
적재 0건 테이블 3건은 ERP 원본 데이터 자체가 없는 상태로 확인 (정상)
7. 권한 부여
신규 생성 13개 테이블에 대해
P_STG
계정 권한(SELECT/INSERT/DELETE/TRUNCATE) 부여
8. 완료 보고
위 내역 종합하여 작업 요청자에게 완료 보고 메일 발송 (DataStage 잡 스크린샷 첨부)
참고할 점 (다음에 비슷한 작업 시)
Vertica 존재 확인 시 이름이 완전 일치하지 않을 수 있으니
OD_
접두사 등 네이밍 컨벤션 먼저 확인
ERP 요청 테이블명이 실제 원본명과 다를 수 있음 (
WRK_MTRL
vs
MTRL
사례) —
LIKE
검색으로 먼저 존재 여부 크로스체크
동일 테이블명이 여러 스키마(
dbo
/
SETUP
)에 있을 수 있음 — 운영 스키마 기준 명확히 확정 필요
DataStage RCP(Runtime Column Propagation) 활용 시 테이블별 컬럼 구조가 달라도 범용 잡 구조로 대응 가능하나, 이번 작업은 테이블/컬럼 수기 로드 방식으로 진행되어 시간 소요됨
