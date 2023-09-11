#!/usr/bin/env python
# coding: utf-8

# ### 병원 네이버 플레이스 방문자 리뷰 크롤링
# - https://pcmap.place.naver.com/hospital/1623603444/review/visitor?entry=bmp&from=map&fromPanelNum=2&timestamp=202309081302&x=126.89195542957395&y=37.50627134485392

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import pymongo as mg


# In[2]:


client = mg.MongoClient(host='mongodb://localhost:27017')
database = client['ns_os_reviews']
collection = database['naver_place']


# In[3]:


# open chrome browser
browser = webdriver.Chrome(executable_path="C:\\Users\\01-03\\Develops\\chromedriver.exe")


# In[4]:


# 국내 척추 병원 리스트(검색 통해 선정함. 보건복지부 선정 척추/관절 병원 리스트가 있는데 나중에 그것도 참고할 예정)
# hospital_data = [
#     ["서울바른병원", 'https://pcmap.place.naver.com/hospital/37427012/home?entry=bmp&from=map&fromPanelNum=2&timestamp=202309111054&x=126.92009780794396&y=37.500217907168434'],
#     ["바로척척의원", 'https://pcmap.place.naver.com/hospital/37902519/home?entry=bmp&from=map&fromPanelNum=2&x=126.8395816&y=37.5588518&timestamp=202309111104'],
#     ["나누리병원 인천", 'https://pcmap.place.naver.com/hospital/37811460/home?entry=bmp&from=map&fromPanelNum=2&timestamp=202309111105&x=126.7308592&y=37.499572'],
#     ["연세더바로신경외과정형외과의원", 'https://pcmap.place.naver.com/hospital/1290271026/home?entry=bmp&from=map&fromPanelNum=2&timestamp=202309111106&x=127.02811010000002&y=37.525109099999995'],
#     ["참포도나무병원", 'https://pcmap.place.naver.com/hospital/30805681/home?entry=bmp&from=map&fromPanelNum=2&timestamp=202309111107&x=127.0386971&y=37.479931300000004'],
#     ["서울병원", 'https://pcmap.place.naver.com/hospital/21560637/home?entry=bmp&from=map&fromPanelNum=2&x=127.12467150000002&y=37.5039463&timestamp=202309111121'],
#     ["안산21세기병원", 'https://pcmap.place.naver.com/hospital/21560235/home?entry=bmp&from=map&fromPanelNum=2&timestamp=202309111125&x=126.8317939&y=37.3307826'],
#     ["바로척척의원", 'https://pcmap.place.naver.com/hospital/37281381/home?entry=bmp&from=map&fromPanelNum=2&x=127.1341414&y=37.5357686&timestamp=202309111127'],
#     ["의료법인본플러스재단분당병원", 'https://pcmap.place.naver.com/hospital/20742703/home?entry=bmp&from=map&fromPanelNum=2&x=127.1064897&y=37.3636242&timestamp=202309111137'],
#     ["기대플러스병원", 'https://pcmap.place.naver.com/hospital/86958121/home?entry=bmp&from=map&fromPanelNum=2&x=126.7364401&y=37.7287226&timestamp=202309111138'],
#     ["서울바른세상병원", 'https://pcmap.place.naver.com/hospital/37445922/home?entry=bmp&from=map&fromPanelNum=2&timestamp=202309111139&x=126.89781340040102&y=37.47119169978151'],
#     ["연세백퍼센트병원", 'https://pcmap.place.naver.com/hospital/1247579806/home?entry=bmp&from=map&fromPanelNum=2&timestamp=202309111140&x=126.7258778&y=37.4944746'],
#     ["오케이병원", 'https://pcmap.place.naver.com/hospital/35913572/home?entry=bmp&from=map&fromPanelNum=2&x=126.73374058126338&y=37.52834095985524&timestamp=202309111141'],
#     ["열린연세정형외과의원", 'https://pcmap.place.naver.com/hospital/1082253030/home?entry=bmp&from=map&fromPanelNum=2&timestamp=202309111141&x=126.93011169050402&y=37.36027717232209'],
#     ["국제바로병원", 'https://pcmap.place.naver.com/hospital/13205824/home?entry=bmp&from=map&fromPanelNum=2&timestamp=202309111143&x=126.69317347360611&y=37.46551276685047'],
#     ["나사렛국제병원", 'https://pcmap.place.naver.com/hospital/13349355/home?entry=bmp&from=map&fromPanelNum=2&timestamp=202309111147&x=126.67051078074321&y=37.40808057937737'],
#     ["나누리병원 주안", 'https://pcmap.place.naver.com/hospital/37350818/home?entry=bmp&from=map&fromPanelNum=2&x=126.69068909963093&y=37.45093300081088&timestamp=202309111150'],
#     ["부산우리들병원", 'https://pcmap.place.naver.com/hospital/12075325/home?entry=bmp&from=map&fromPanelNum=2&timestamp=202309111154&x=129.0856653&y=35.2216217'],
#     ["강북연세병원", 'https://pcmap.place.naver.com/hospital/13098049/home?entry=bmp&from=map&fromPanelNum=2&timestamp=202309111155&x=127.07550329951835&y=37.61918910116395']
# ]

## 테스트용
hospital_data = [
    ["안산21세기병원", 'https://pcmap.place.naver.com/hospital/21560235/home?entry=bmp&from=map&fromPanelNum=2&timestamp=202309111125&x=126.8317939&y=37.3307826'],
    ["나누리병원 주안", 'https://pcmap.place.naver.com/hospital/37350818/home?entry=bmp&from=map&fromPanelNum=2&x=126.69068909963093&y=37.45093300081088&timestamp=202309111150']
]

# DataFrame 생성
df_hospital = pd.DataFrame(hospital_data, columns=["hospital", "url"])

# DataFrame 출력
# pd.set_option('display.max_colwidth', None)
# print(df_hospital)


# ### Tags
# - 리뷰탭 클릭 : div.place_fixed_maintab > div > div > div > div > a:nth-child(2) > span
# 
# - 리뷰 박스 : div:nth-child(7) > div:nth-child(3) > div > div > ul > li
# 
# - 병원 이름 : #_title > span.Fc1rA
# 
# - 병원 주소 : li > div > div > div > span:nth-child(1) > span:nth-child(3)
# 
# - 작성자 : div > ul > li > div > a > div.VYGLG
# 
# - 리뷰 내용 : div.place_section_content > ul > li:nth-child({}) > div > a > span.zPfVt
# 
# - 리뷰 더보기 :  div.place_section_content > ul > li:nth-child({}) > div > a > span.rvCSr
# 
# - 리뷰 날짜 : li > div > div > div > span:nth-child(1) > span:nth-child(3)
# 
# - 방문 횟수 : li > div > div > div > span:nth-child(2)
# 
# - 더보기 클릭 : div > div > div > div.lfH3O > a
# 

# In[5]:


# 한 병원 url이 한 사이클
for url in df_hospital['url']:
    # 네이버플레이스 사이트 접속
    browser.get(url)
    browser.implicitly_wait(5)
    hospital = browser.find_element_by_css_selector('#_title > span.Fc1rA').text # 병원명
    address = browser.find_element_by_css_selector('div > div > a > span.LDgIH').text # 주소
    print("■", hospital, "-",address) # 병원명, 주소 출력
    
    # 리뷰탭 클릭
    browser.find_element_by_css_selector('div.place_fixed_maintab > div > div > div > div > a:nth-child(2) > span').click()
    time.sleep(2)
    # 전체 더보기 버튼 클릭
    while True:
        try:
            browser.find_element_by_css_selector('div > div > div > div.lfH3O > a').click()
        except:
            break
    browser.find_element_by_css_selector('body').send_keys(Keys.HOME) # 화면 상단으로 이동
    time.sleep(3)

#    # 리뷰 더보기 버튼 개수 찾기 (화면 크기에 따라 달라짐)
#    see_more_buttons = browser.find_elements_by_css_selector('div.place_section_content > ul > li > div > a > span.rvCSr')
#    print("긴 댓글    :", len(see_more_buttons))
#    # 리뷰 더보기 클릭
#    for num_see_more in range(len(see_more_buttons)): 
#        time.sleep(1)
#        see_more_path = see_more_buttons[num_see_more]
#        see_more_path.click()
        
    
    # List생성, Column명 지정
    reviews_list = []
    columns_name = ['hospital', 'address', 'name', 'content', 'date', 'visits']

    reviews_bundle = browser.find_elements_by_css_selector('div:nth-child(7) > div:nth-child(3) > div > div > ul > li')
    
    reviews_bundle.find_element_by_css_selector('li:nth-child({}) > div.ZZ4OK > a'.format(index)).click()


    pass

    # 리뷰박스에서 작성자명, 리뷰내용, 날짜, 방문횟수 수집 # 리스트에 추가
    cnt = 0 # 리뷰 저장 개수 카운트
    for index, review in enumerate(reviews_bundle, start=1):
        try :

            content = review.find_element_by_css_selector('div.place_section_content > ul > li > div.ZZ4OK > a').text
            name = review.find_element_by_css_selector('div > ul > li > div > a > div.VYGLG').text 
            date = review.find_element_by_css_selector('li > div > div > div > span:nth-child(1) > span:nth-child(3)').text
            visits = review.find_element_by_css_selector('li > div > div > div > span:nth-child(2)').text
            full_review = [hospital, address, name, content, date, visits]
            reviews_list.append(full_review)
            cnt += 1
        except : # 댓글 내용이 없고 사진만 있을 경우 제외 
            pass
        
    # reviews_list를 Mongodb에 추가     
    df_reviews = pd.DataFrame(data=reviews_list, columns=columns_name)
    data_dict = df_reviews.to_dict(orient='records')
    collection.insert_many(data_dict)        
    
    print("전체 댓글  :", len(reviews_bundle))
    print("저장된 댓글 :", cnt)     

print("DB 업로드 댓글 :", len(reviews_list))     
browser.quit()


# In[ ]:


# {"content": {"$regex": "수술"}}
# {"hospital": {"$regex": "연세백퍼센트병원"}}
# {"name": {"$regex": "동동"}}

