ETL 작업 일지

#0126 PLM_STYL_CD PK 관련

소스 DB (MSSQL)
타겟 DB (VERTICA)

소스 DB에서 PK를 STYL_CD => PLM_STYL_CD  로 수정한 항목들이 존재함.
STYL_CD,PLM_STYL_CD는 둘 다 기존에 존재하던 컬럼들임.

변경 exmaple ) as-is PK  (COMP_CD,STYL_CD,CLR_CD) => to-be PK (COMP_CD,PLM_STYL_CD,CLR_CD)

타겟 테이블에서 PK를 변경해줘야함.

문제는 일대일 매핑이었던 ODS테이블을 변경해주더라도, 뒷단에 존재하는 FT , DM 테이블들을 구성하는 영역임
FT 테이블 , DM 테이블은 여러 ODS 테이블들의 조합이나 FT 테이블들의 조합으로 생성되는데,
이때 바뀐 PK값들에 대한 영향을 받는 테이블들이 소스에 존재하는지 확인해야함.

### 현재 상황
<img width="753" height="170" alt="image" src="https://github.com/user-attachments/assets/313b5a6d-1065-4172-b71d-979e74fb2530" />

### 소스에 FT 테이블들 다수 존재
### Step Source FT 테이블들의 목록을 추출 후 PK 값을 수정하여 오류를 해결하였다.

