MSSQL 관리용 주요 시스템 저장 프로시저들을 카테고리별로 정리해드리겠습니다.

## 객체 정보 조회

**sp_help** [object_name]
- 객체의 전체 정보 조회 (컬럼, 인덱스, 제약조건 등)
- `EXEC sp_help 'dbo.TableName'`

**sp_helptext** [object_name]
- 저장 프로시저, 함수, 뷰 등의 정의 조회
- `EXEC sp_helptext 'dbo.sp_ProcName'`

**sp_depends** [object_name]
- 객체 간 종속성 확인
- `EXEC sp_depends 'dbo.TableName'`

**sp_columns** [table_name]
- 테이블 컬럼 상세 정보
- `EXEC sp_columns 'TableName'`

**sp_helpindex** [table_name]
- 테이블의 인덱스 정보
- `EXEC sp_helpindex 'TableName'`

## 성능 모니터링

**sp_who** / **sp_who2**
- 현재 세션 및 프로세스 정보
- `EXEC sp_who2 'active'` (활성 세션만)

**sp_lock**
- 현재 락 정보 조회

**sp_monitor**
- SQL Server 통계 정보 (CPU, I/O 사용량 등)

**sp_BlitzFirst** (Brent Ozar 도구)
- 실시간 성능 분석

## 데이터베이스 관리

**sp_helpdb** [database_name]
- 데이터베이스 정보 조회
- `EXEC sp_helpdb 'DatabaseName'`

**sp_spaceused** [object_name]
- 데이터베이스/테이블 공간 사용량
- `EXEC sp_spaceused 'TableName'`

**sp_MSforeachdb** / **sp_MSforeachtable**
- 모든 DB/테이블에 명령 실행
- `EXEC sp_MSforeachdb 'USE ? EXEC sp_spaceused'`

**sp_helpfile**
- 데이터베이스 파일 정보

## 보안 관리

**sp_helpuser** [username]
- 데이터베이스 사용자 정보

**sp_helplogins** [login_name]
- 로그인 계정 정보

**sp_helprole**
- 데이터베이스 역할 정보

**sp_helprotect** [object_name]
- 객체 권한 정보

## 성능 튜닝

**sp_updatestats**
- 모든 테이블 통계 업데이트

**sp_recompile** [object_name]
- 저장 프로시저 실행 계획 재컴파일

**sp_executesql**
- 동적 SQL 실행 (파라미터화)

## 시스템 정보

**sp_configure**
- 서버 설정 조회/변경
- `EXEC sp_configure 'show advanced options', 1`

**sp_helpserver**
- 연결된 서버 정보

**sp_databases**
- 모든 데이터베이스 목록

## 실무 활용 팁

```sql
-- 1. 데드락 찾기
EXEC sp_who2
-- SPID 확인 후
DBCC INPUTBUFFER(SPID번호)

-- 2. 큰 테이블 찾기
CREATE TABLE #temp (
    table_name NVARCHAR(128),
    rows BIGINT,
    reserved VARCHAR(50),
    data VARCHAR(50)
)
EXEC sp_MSforeachtable 'INSERT INTO #temp EXEC sp_spaceused ''?'''
SELECT * FROM #temp ORDER BY rows DESC

-- 3. 미사용 인덱스 찾기
SELECT 
    OBJECT_NAME(i.object_id) AS TableName,
    i.name AS IndexName,
    i.index_id
FROM sys.indexes i
LEFT JOIN sys.dm_db_index_usage_stats s 
    ON i.object_id = s.object_id AND i.index_id = s.index_id
WHERE s.index_id IS NULL AND i.index_id > 1
```

현재 개발 중인 MSSQL 관리 프로그램에 이런 프로시저들을 활용하시면 좋을 것 같습니다. 특히 sp_who2, sp_lock, sp_spaceused는 모니터링 UI에 자주 사용됩니다.

추가로 궁금한 특정 프로시저나 활용 사례가 있으신가요?
