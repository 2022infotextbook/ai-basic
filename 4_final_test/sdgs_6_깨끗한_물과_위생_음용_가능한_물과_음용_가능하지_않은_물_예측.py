# -*- coding: utf-8 -*-
"""SDGs 6 깨끗한 물과 위생: 음용 가능한 물과 음용 가능하지 않은 물 예측

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10uGCkWrLq_X2ZVAYavjbT1wc9LMFUq_a

## 주제:

지속가능발전목표 6 깨끗한 물과 위생

음용 가능한 물과 음용 가능하지 않은 물 예측

## 1. 문제 정의

이 프로젝트의 목표는 캐글(Kaggle)에서 제공되는 물의 음용 가능성 데이터를 사용하여 인공지능 모델을 개발하는 것이다. 이 모델은 주어진 물 샘플의 여러 화학적, 물리적 속성을 분석하여 해당 물이 음용 가능한지 여부를 예측할 것이다. 성공적인 모델은 정확하고 신뢰할 수 있는 예측을 제공하여 음용수 관리 및 처리 분야에서 의사결정을 지원하는 데 사용될 수 있다.

## 2. 데이터 수집 및 전처리

# 2-1 데이터 수집
"""

import pandas as pd

# GitHub에서 데이터셋 로드
url = 'https://raw.githubusercontent.com/2022infotextbook/ai-basic/main/4_ai_project/4_final_test/water_potability.csv'
data = pd.read_csv(url)

# 데이터 확인
data.head()

# 데이터 탐색: 데이터의 기본적인 구조, 결측치, 데이터 타입 등을 파악
data.info()

"""# 2-2 결측치 처리"""

# 결측치 처리: 결측치가 있는 경우 이를 채우거나 해당 행/열을 제거
# 예: 결측치를 평균값으로 채우기
# 결측치 확인
data.isnull().sum()

#평균값 확인
data.groupby(['Potability']).mean()

# # 음용가능하지 않은 물(0)과 음용가능한 물의 평균 ph값, Sulfate값, Trihalomethanes값을 결측치 데이터에 채우기
ph_mean = data.groupby(['Potability'])['ph'].transform('mean')
Su_mean = data.groupby(['Potability'])['Sulfate'].transform('mean')
Tr_mean = data.groupby(['Potability'])['Trihalomethanes'].transform('mean')
data['ph']=data['ph'].fillna(ph_mean)
data['Sulfate']=data['Sulfate'].fillna(Su_mean)
data['Trihalomethanes']=data['Trihalomethanes'].fillna(Tr_mean)

# 결측치 처리 후 결측치 확인
data.isnull().sum()

"""# 2-3 데이터 편향성 확인"""

# 데이터 편향성 확인
data['Potability'].value_counts()

from imblearn.over_sampling import RandomOverSampler

# 오버샘플링 설정
ros = RandomOverSampler(random_state=0)

# 데이터와 레이블 분리
X = data.drop('Potability', axis=1)
y = data['Potability']

# 오버샘플링 적용
X_resampled, y_resampled = ros.fit_resample(X, y)

# 새로운 데이터프레임 생성
data_resampled = pd.DataFrame(X_resampled, columns=X.columns)
data_resampled['Potability'] = y_resampled

# 데이터 편향성 확인
data_resampled['Potability'].value_counts()

"""# 2-4 훈련 데이터와 테스트 데이터 분리"""

from sklearn.model_selection import train_test_split

# 특성과 레이블 분리
X = data_resampled.drop('Potability', axis=1)
y = data_resampled['Potability']

# 데이터 분할(기본설정값: 75:25)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=40)

# 훈련세트와 테스트세트 갯수 확인
print(f'훈련 세트 갯수: {X_train.shape[0]}')
print(f'테스트 세트 갯수: {X_test.shape[0]}')

"""# 2-5 정규화 처리"""

from sklearn.preprocessing import StandardScaler

# 정규화
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

#정규화 처리된 데이터 확인
print(X_train)

"""## 3. 기계학습 유형과 알고리즘 선정(kNN, 랜덤포레스트)

## 4. 기계학습을 통한 모델 생성
"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 모델 초기화 및 훈련
models = {
    "KNN": KNeighborsClassifier(),
    "Random Forest": RandomForestClassifier()
}

# 각 모델의 정확도 출력
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"{name} Accuracy: {accuracy_score(y_test, y_pred):.2f}")

"""## 5. 성능 평가 및 수정"""

# 각각의 모델 별 최적 하이퍼파라미터 찾기
import numpy as np
from sklearn.model_selection import GridSearchCV

kn = KNeighborsClassifier()
rf = RandomForestClassifier()

#k-NN
para_kn = {'n_neighbors':np.arange(1, 50)}
grid_kn = GridSearchCV(kn, param_grid=para_kn, cv=5)
#랜덤포레스트
params_rf = {'n_estimators':[100, 200, 350, 500], 'min_samples_leaf':[2, 10, 30]}
grid_rf = GridSearchCV(rf, param_grid=params_rf, cv=5)

# 머신러닝 모델을 학습시키며 하이퍼파라미터의 최적값 찾기
score_df_kn = grid_kn.fit(X_train, y_train)
score_df_rf = grid_rf.fit(X_train, y_train)

print(f'최적 파라미터 k-NN: {grid_kn.best_params_}')
print(f'최적 파라미터 랜덤포레스트: {grid_rf.best_params_}')

#최적의 모델 대입
kn = grid_kn.best_estimator_
rf = grid_rf.best_estimator_

# 모델 초기화 및 훈련
models = {
    "KNN": kn,
    "Random Forest": rf
}

# 각 모델의 정확도 출력
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"{name} Accuracy: {accuracy_score(y_test, y_pred):.2f}")