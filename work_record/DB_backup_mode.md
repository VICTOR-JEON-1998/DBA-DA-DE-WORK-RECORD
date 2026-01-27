```sql
-- SIMPLE 복구 모델 데이터베이스 조회
SELECT 
    name AS DatabaseName,
    database_id AS DB_ID,
    recovery_model_desc AS RecoveryModel,
    state_desc AS State,
    log_reuse_wait_desc AS LogReuseWait,
    create_date AS CreateDate,
    compatibility_level AS CompatLevel
FROM sys.databases
WHERE recovery_model_desc = 'SIMPLE'
    AND name NOT IN ('tempdb')  -- tempdb는 기본 제외
    AND state_desc = 'ONLINE'
ORDER BY name;


ALTER DATABASE INTERFACE set recovery full
ALTER DATABASE KSNET set recovery full
ALTER DATABASE KTNET set recovery full
ALTER DATABASE NPRO_FH set recovery full
ALTER DATABASE NPRO_FK set recovery full
ALTER DATABASE NPRO_FK_AUTH set recovery full
ALTER DATABASE SECOM set recovery full
ALTER DATABASE SECUREDB set recovery full
ALTER DATABASE SMILEEDI set recovery full
ALTER DATABASE TABSMAILER set recovery full
```
