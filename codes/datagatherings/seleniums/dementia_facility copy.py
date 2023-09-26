#!/usr/bin/env python
# coding: utf-8

# ### 중앙치매센터 치매시설정보 크롤링
# - https://www.nid.or.kr/info/facility_list.aspx

# In[1]:


from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import pymongo as mg
import traceback


# In[2]:


client = mg.MongoClient(host='mongodb://localhost:27017')
database = client['facility_infos']
collection = database['dementia']


# In[16]:
# Chrome 브라우저를 headless 모드로 실행하기 위한 옵션 생성
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")

# open chrome browser
# browser = webdriver.Chrome(executable_path='C:\\Users\\01-03\\Develops\\chromedriver.exe', chrome_options=options)
browser = webdriver.Chrome(executable_path='C:\\Users\\01-03\\Develops\\chromedriver.exe')

# In[17]:

browser.set_window_size(1920, 1080)
url = 'https://www.nid.or.kr/info/facility_list.aspx#'
browser.get(url)
browser.implicitly_wait(3)


# ### Tags
# ['시설명', '주소', '시설분류정보', '전화번호', '홈페이지']<br>
# ['name', 'address', 'category', 'number', 'website']<br>
# ['시설명', '주소', '위도', '경도', '대분류', '중분류', '소분류', '전화번호', '홈페이지']<br>
# ['name', 'address', 'latitude', 'longitude', 'main_category', 'sub_category', 'sub_category_2', 'number', 'website']
# - 상세 버튼 : #dev_tbody > tr:nth-child({1~10, 마지막페이지 8}) > td:nth-child(4) > a
# - 상세 버튼 목록 : #dev_tbody > tr > td:nth-child(4) > a
# - 닫기 버튼 : div > div.popTitle > a
# 
# - 페이지 버튼 목록 : #div_paging > div > ol > li > a
# - 페이지 버튼 : #div_paging > div > ol > li:nth-child({1~10}, 마지막 1) > a



# - 다음 페이지 목록 : xpath : //*[@id="div_paging"]/div/a/img[@alt="다음"]
# - 시설명 : div.list_tbl_01.fix > table > tbody > tr:nth-child(1) > td:nth-child(2)
# - 주소 : div.list_tbl_01.fix > table > tbody > tr:nth-child(2) > td
# - 시설분류정보 : div.list_info > div.dx_fa_div > ul > li
# - 전화번호 : div.list_tbl_01.fix > table > tbody > tr:nth-child(1) > td:nth-child(4)
# - 홈페이지 : div.list_tbl_01.fix > table > tbody > tr:nth-child(3) > td
# 

last_btn = browser.find_element_by_xpath('//*[@id="div_paging"]/div/a/img[@alt="마지막으로"]')
last_btn.click()
time.sleep(1) 

page_cnt = 4152
desired_page = 1

while True : 
    if page_cnt < desired_page : 
        break
    time.sleep(1)
    facility_list = []
    columns_name = ['name', 'address', 'category', 'number', 'website']
    page_list = browser.find_elements_by_css_selector('#div_paging > div > ol > li > a')
    
    print("actual page :", page_list[0].text)
    print(f"page {page_cnt-len(page_list)}~{page_cnt-1}")
    
    
    for index, page in enumerate(page_list) :
        try:
            page_cnt -= 1
            print(page_cnt)
            detail_btns = browser.find_elements_by_css_selector('#dev_tbody > tr > td:nth-child(4) > a') 


            for idx, btn in enumerate(detail_btns) :

                # 상세보기 클릭
                element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#dev_tbody > tr:nth-child({}) > td:nth-child(4) > a'.format(idx+1))))


                element.click()

                browser.switch_to.frame('frameLayer_frame') # 상세페이지로 browser 전환
                name = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/div[2]/div[2]/table/tbody/tr[1]/td[1]')))
                name = name.text 
                address = browser.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div[2]/table/tbody/tr[2]/td').text
                category = browser.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div[1]/ul').text
                number = browser.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div[2]/table/tbody/tr[1]/td[2]').text
                website = browser.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div[2]/table/tbody/tr[3]/td').text
                facility_info = [name, address, category, number, website]
                facility_list.append(facility_info)

                # 상세페이지 닫기
                close_btn = browser.find_element_by_xpath('/html/body/div/div[1]/a/img[@alt="닫기"]')
                browser.execute_script("arguments[0].click();", close_btn)
                browser.switch_to.parent_frame()

            try: 
                next_page = browser.find_element_by_css_selector('div > ol > li:nth-child({})'.format(index+2))
                next_page.click()
                
            except Exception as e:
                print(f"에러 발생: {str(e)}")                               
                traceback.print_exc() 
                
                try:
                    next_btn = browser.find_element_by_xpath('//*[@id="div_paging"]/div/a/img[@alt="이전"]')
                    next_btn.click()
                    time.sleep(1)                    
                    
                except Exception as e:
                    print(f"에러 발생: {str(e)}")                               
                    traceback.print_exc() 
                    break
        except Exception as e:
            print(f"에러 발생: {str(e)}")                               
            traceback.print_exc() 
            continue
    else:
        # DB에 추가
        df_dementia_facility = pd.DataFrame(data=facility_list, columns=columns_name)
        data_dict = df_dementia_facility.to_dict(orient='records')
        collection.insert_many(data_dict)  
        continue
    break 
 

# browser.quit()



cursor = collection.find({})
list_cursors = list(cursor)


# In[9]:


df_total = pd.DataFrame(list_cursors)


# In[10]:


df_total[:3]


# In[11]:


df_drop_id = df_total.drop('_id', axis=1)
df_drop_id[:3]


# In[12]:


df_drop_id.info()


# In[13]:


df_drop_dup = df_drop_id.drop_duplicates()
df_drop_dup.info()


# In[14]:


df_drop_dup.to_csv('./dementia_facility.csv')

# {"content": {"$regex": "수술"}}
# {"hospital": {"$regex": "연세백퍼센트병원"}}
# {"name": {"$regex": "동동"}}

