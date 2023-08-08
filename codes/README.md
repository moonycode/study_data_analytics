### DDA
# 📕 Data Dictionary

<details open>
<summary>Titanic - Machine Learning from Disaster</summary>

Dataset from : https://www.kaggle.com/c/titanic

| Variable | Definition | Key | 분석가 의견 |
| --- | --- | --- | --- |
| passengerid | PassengerId | 0, 1, 2, 3, ... | 범주형 :  unique id나 index의 개념으로 사용됨. |
| survival | Survival | 0 = No, 1 = Yes | 범주형 :  Yes와 No를 구분하기 위한 데이터. |
| pclass | Ticket class | 1 = 1st, 2 = 2nd, 3 = 3rd | 범주형 :  객실 등급을 나타냄. |
| sex | Sex | male, female | 범주형 |
| Age | Age in years | 22.0, 38.0, 26.0, ... | 수치형(float). 이산형 데이터임. 다만 null값이 있는 177개 레코드 있음. |
| sibsp | # of siblings / spouses aboard the Titanic | 0 = No, 1 = Yes | 범주형 :  Yes와 No를 구분하기 위한 데이터. |
| parch | # of parents / children aboard the Titanic | 0 = No, 1 = Yes  | 범주형 :  Yes와 No를 구분하기 위한 데이터. |
| ticket | Ticket number | A/5 21171, PC 17599, STON/O2. 3101282, 113803, ... | 범주형-명목형 :  |
| fare | Passenger fare | 7.2500, 71.2833, 7.9250, ... | 수치형-연속형/이산형 :  티켓의 요금을 나타냄. |
| cabin | Cabin number | C85, C123, B42, ... | 범주형 :  객실 번호(객실명)를 나타냄. |
| embarked | Port of Embarkation | C = Cherbourg, Q = Queenstown, S = Southampton | 범주형 :  승선한 항구 이름을 나타냄. |

</details>


<details open>
<summary>Type Of Contract Channel</summary>

Dataset from : https://blog.naver.com/data_station/222493245799

| Variable | Definition | Key | Data Type |
| --- | --- | --- | --- |
| id | | 66758234, 66755948, 66756657, ... | 범주형-명목형 :  각 고객의 unique id를 나타냄.|
| type_of_contract | | 렌탈, 멤버십 |  범주형-명목형 :  |
| type_of_contract2 | | Normal, Extension_Rental, TAS, ... |  범주형-명목형 :  |
| channel | | 서비스 방문, 홈쇼핑/방송, 렌탈재계약, ... |  범주형-명목형 |
| datetime | | 2019-10-20, 2019-11-25, 2020-01-06 |  수치형-이산형 or 범주형-순서형? |
| Term | | 60, 36, 12, 39 |  수치형-이산형 :  유의미한 수치데이터임. |
| payment_type | | CMS, 카드이체, 무통장, ... |  범주형-명목형 |
| product | | K1, K2, ... |  범주형-명목형 :  제품모델을 구분하기 위한 id임. |
| amount | | 96900, 102900, 81900, ... |  수치형-이산형 :  할인폭에 따라 결제가격이 비교적 다양하여 연속형과 헷갈리나 이산형에 속함. |
| state | | 계약확정, 해약확정, 기간만료, ... |  범주형-명목형 |
| overdue_count | | 0, 1, 3, -1, ... |  수치형-이산형 :  유의미한 수치데이터임. |
| overdue | | 없음, 없음 |  범주형-명목형 :  |
| credit rating | | 9.0, 2.0, 8.0, ... |  수치형-이산형 :  수치의 크기가 유의미함 |
| bank | | 새마을금고, 현대카드, ... |  범주형-명목형 : |
| cancellation | | 정상, 해약 |  범주형-명목형 :  |
| age | | 43.0, 62.0, 60.0, 60.0, 51.0 |  수치형-이산형 :  나이는 이산형에 속함. |
| Mileage | | 1862.0, 2532.0, 2363.0 |  수치형-연속형 :  연속적인 정수값을 가짐.|

</details>