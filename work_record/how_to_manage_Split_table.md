"달리는 자동차의 바퀴를 갈아 끼우는 법: 대용량 테이블 무중단 리팩토링 사례"

데이터 엔지니어링 업무를 하다 보면 필연적으로 비대해진 레거시 테이블을 마주하게 됩니다. 최근 운영 중인 DB에서 수백 개의 컬럼을 가진 핵심 마스터 테이블을 성격에 따라 3개의 서브 테이블로 수직 분할(Vertical Partitioning) 하는 과제를 수행했습니다.

가장 큰 제약사항은 **"매일 수행되는 ETL 파이프라인에 단 1초의 중단이나 에러도 허용하지 않는 것"**이었습니다.

저는 '뷰(View)를 활용한 추상화 계층(Abstraction Layer)' 전략을 통해 이 문제를 해결했습니다.

접근 방법 (Macro View) 핵심은 애플리케이션(ETL)과 데이터 저장소(DB) 간의 결합도(Coupling)를 끊는 것입니다. ETL이 물리 테이블을 직접 참조하는 구조에서, View라는 논리적 인터페이스를 참조하도록 변경하여 DB 구조 변경이 외부 시스템에 영향을 주지 않도록 격리했습니다.

🛠 기술적 해결 (Micro View)

Composite Key 최적화: 복합키(PK) 구조를 가진 테이블 분할 시, 자식 테이블에도 동일한 Clustered Index를 구성하여 Merge Join을 유도, 조회 성능 저하를 방지했습니다.

Alias View Pattern: 레거시 이슈로 테이블 리네임이 불가능한 상황에서, 통합 뷰를 생성하고 ETL 쿼리를 선제적으로 수정하여 Zero-Downtime Migration을 달성했습니다.

Collision Handling: 분리된 테이블 간 중복되는 속성 값은 비즈니스 우선순위에 따라 ISNULL 처리하여 데이터 정합성을 보장했습니다.


1. Background (문제 정의)
Situation: Product_Master 테이블에 과도한 컬럼이 집중되어 유지보수 효율성 저하.

Task: 해당 테이블을 Base, Extension_A, Extension_B 3개로 수직 분할(Vertical Partitioning).

Constraint: 기존 테이블 명칭 변경 불가 & ETL Job 중단 불가.

2. Solution Strategy (해결 전략)
Abstraction Layer: 물리적 테이블은 분리하되, 논리적으로는 하나의 테이블처럼 보이는 통합 View 제공.

Migration Path: 신규 테이블 생성 -> 데이터 Sync -> View 생성 -> ETL 타겟 변경 -> 기존 컬럼 삭제 순서로 진행하여 리스크 최소화.

3. Pseudo Code (구현 예시)
A. 복합키(Composite Key) 성능 최적화 PK가 복합키(예: CompanyID + ItemID)인 경우, 단순 Join은 성능 이슈를 유발할 수 있음. 자식 테이블 인덱스 전략이 핵심.

SQL

-- [View Definition Example]
-- 실제 컬럼명 대신 일반적인 명칭으로 기술함
```sql
CREATE VIEW dbo.V_Product_Master_Full AS
SELECT 
    -- 1. Base Table Columns
    A.CompanyID, A.ItemID, A.ProductName, ... 
    
    -- 2. Extension Table A (Online Info)
    B.DetailDescription, B.ImageURL, ...
    
    -- 3. Extension Table B (Additional Info)
    C.ExtraAttribute, ...

    -- 4. Column Collision Handling
    ISNULL(B.IsActive, C.IsActive) AS IsActive_Combined

FROM dbo.Product_Master_Base A
LEFT JOIN dbo.Product_Extension_A B 
    ON A.CompanyID = B.CompanyID AND A.ItemID = B.ItemID -- Composite Key Join
LEFT JOIN dbo.Product_Extension_B C 
    ON A.CompanyID = C.CompanyID AND A.ItemID = C.ItemID;
```
4. Lessons Learned (배운 점)
Merge Join 유도: 수직 분할된 테이블을 다시 조인하여 뷰로 제공할 때, 조인 키에 적절한 인덱스가 없으면 심각한 성능 저하 발생. 실행 계획(Execution Plan) 확인 필수.

안전한 배포: 컬럼 삭제(Drop Column)는 모든 애플리케이션이 뷰를 바라보게 변경된 후, 가장 마지막에 수행해야 함.



