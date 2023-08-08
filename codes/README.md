# Titanic - Machine Learning from Disaster
Dataset from : https://www.kaggle.com/c/titanic

### DDA

<details open>
<summary>📕 Data Dictionary</summary>

| Variable | Definition | Key | 분석가 의견 |
| --- | --- | --- | --- |
| passengerid | PassengerId | 0, 1, 2, 3, ... | 범주형. unique id나 index의 개념으로 사용됨. |
| survival | Survival | 0 = No, 1 = Yes | 범주형. Yes와 No를 구분하기 위한 데이터. |
| pclass | Ticket class | 1 = 1st, 2 = 2nd, 3 = 3rd | 범주형. 객실 등급을 나타냄. |
| sex | Sex | male, female | 범주형 |
| Age | Age in years | 22.0, 38.0, 26.0, ... | 수치형(float). 이산형 데이터임. 다만 null값이 있는 177개 레코드 있음. |
| sibsp | # of siblings / spouses aboard the Titanic | 0 = No, 1 = Yes | 범주형. Yes와 No를 구분하기 위한 데이터. |
| parch | # of parents / children aboard the Titanic | 0 = No, 1 = Yes  | 범주형. Yes와 No를 구분하기 위한 데이터. |
| ticket | Ticket number | A/5 21171, PC 17599, STON/O2. 3101282, 113803, ... | 범주형-명목형. |
| fare | Passenger fare | 7.2500, 71.2833, 7.9250, ... | 수치형-연속형/이산형. 티켓의 요금을 나타냄. |
| cabin | Cabin number | C85, C123, B42, ... | 범주형. 객실 번호(객실명)를 나타냄. |
| embarked | Port of Embarkation | C = Cherbourg, Q = Queenstown, S = Southampton | 범주형. 승선한 항구 이름을 나타냄. |

</details>

