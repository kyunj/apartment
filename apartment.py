import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import date


sns.set_theme(style='whitegrid', font_scale=1.5)
sns.set_palette('Set2', n_colors=10)
plt.rc('font', family='malgun gothic')
plt.rc('axes', unicode_minus=False)

#Page Setting
st.set_page_config(page_title='Apartments Management Price Visualization',
                   page_icon='🐋', layout='wide')
st.title("Apartments Management Price Visualization")
#APP_TITLE = 'Apartments Management Price Visualization'
APP_SUB_TITLE = '단위: 만원'
#st.set_page_config(APP_TITLE)
#st.title(APP_TITLE)
st.caption(APP_SUB_TITLE)

#Data loading & preprocessing
df = pd.read_csv('OPST.csv', encoding = 'euc-kr')
df.drop(index = list(df[df['address'] == '0'].index), inplace = True)
df.drop(index = list(df[df['cost'] == 0].index), inplace = True)
city,gu,dong = [],[],[]
for i in df['address']:
    if i != '0':
        city.append(i.split()[0])
        gu.append(i.split()[1])
        dong.append(i.split()[2])
    else:
        continue
df['city'] = city
df['gu'] = gu
df['dong'] = dong

#df.groupby(['gu'])[['cost']].mean().plot()

#side bar
my_df = df
st.sidebar.header('위치 선택')

option01 = st.sidebar.multiselect('구 선택',
                                  df['gu'].unique(),
                                  default = ['강남구'])
check01 = st.sidebar.checkbox("전체 구 선택", value=False)
if check01:
    my_df = df
else:
    my_df = df[df['gu'].isin(option01)]

option02 = st.sidebar.multiselect('동 선택',
                                  my_df['dong'].unique(),
                                  default = ['삼성동'])
check02 = st.sidebar.checkbox("전체 동 선택", value = False)
if check02:
    my_df = my_df
else:
    my_df = my_df[my_df['dong'].isin(option02)]
st.sidebar.header('조건 선택')
option03 = st.sidebar.slider("최소 평 수", round(my_df['space'].min()),round(my_df['space'].max()),(21,38))
st.sidebar.write("평수는",option03,"사이 입니다")
st.sidebar.tabs(['가','나','다'])

st.sidebar.write("필터 적용을 눌러야 보입니다!")

start_button = st.sidebar.button(
    "필터 적용📊"
)

if start_button:
    my_df = my_df[my_df['space'].between(option03[0],option03[1])]
    st.sidebar.success("필터 적용 되었습니다!")
    st.balloons()
    st.table(my_df)

import time 

# 방법 1 progress bar 
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
# Update the progress bar with each iteration.
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 2)
    time.sleep(0.025)
  # 0.05 초 마다 1씩증가
    #st.balloons()
    # 시간 다 되면 풍선 이펙트 보여주기

#Visualization
st.header('0. Overview')
col1, col2, col3 = st.columns(3)
col1.metric(label = '평균 월세가격(단위:만원)', value = round(1),
            delta = round(0))
col2.metric(label = '평균 전세가격(단위:만원)', value = round(1),
            delta = round(0))
col3.metric(label = '평균 관리비(단위:만원)', value = round(my_df['cost'].mean() / 10000, 3),
            delta = round(my_df['cost'].mean() / 10000 - df['cost'].mean() / 10000, 3))

st.header('1. 가격 현황 분석')
st.subheader('전체')
time_frame = st.selectbox("전세/월세/관리비",("전세","월세","관리비"))
#whole_values = my_df.groupby(time_frame)[['cost']].sum()
