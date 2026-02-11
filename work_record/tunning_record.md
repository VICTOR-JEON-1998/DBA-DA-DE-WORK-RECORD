1.튜닝이 필요한 부분을 확인하는 방법

 1-1.튜닝이 필요한 프로시저를 수행
 <img width="1732" height="1199" alt="image" src="https://github.com/user-attachments/assets/69ebff35-9d69-4403-a22b-ae08fa54f565" />

 1-2.프로시저의 수행 시간은 오래 걸림. 이때 어디서 막히는지 확인이 필요함.
 모니터링하는 쿼리를 통해 현재 실행중인 세션들을 확인
```
SELECT * FROM MONITOR.dbo.fn_dba_activesession() 
```
실행중인 세션 확인 
<img width="2228" height="594" alt="image" src="https://github.com/user-attachments/assets/cc217db6-2606-40be-ab96-173228c8d052" />
잠시 후 실행중인 세션 다시 확인
<img width="2208" height="369" alt="image" src="https://github.com/user-attachments/assets/0c1f6456-d687-4631-af52-d79c92755c9e" />

이때 SQL이 같은 곳에서 계속 실행중인 것을 볼 수 있음.
이것을 통해 해당 SQL의 수행 시간이 오래 걸리는 것을 파악할 수 있음.

2. 실제 프로시저 쿼리 분석
   2-1. 오래 걸리는 부분을 파악하였으니, 실제 프로시저 쿼리에서 그 구분을 중점으로 쿼리를 분석함.

----------------- ing-----
   
