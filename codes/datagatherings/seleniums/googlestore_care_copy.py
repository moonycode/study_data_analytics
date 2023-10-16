from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import pandas as pd
import pymongo as mg

base_url = "https://play.google.com/store/apps/details?id="

url_ids = [
    'kr.carenation.protector&hl=ko',  # 케어네이션 - 간병인찾기
    'kr.carenation.caregiver&hl=ko',  # 케어네이션 - 일자리찾기
    'com.soomgo&hl=ko',  # 숨고
    'net.nrise.wippy&hl=ko', # 위피
    'kr.nacommunity.anyman&hl=ko' # 애니맨 - 실시간 도움 요청 앱

]

full_urls = [base_url + url_id for url_id in url_ids]

client = mg.MongoClient(host='mongodb://localhost:27017')
database = client['care_apps_reviews']
collection = database['google_playstore']

# open chrome browser
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

cnt_total_db = 0

for url in full_urls:
    # List생성, Column명 지정
    reviews_list = []
    columns_name = ['title', 'downloads', 'rating', 'release_date',
                    'info', 'reviewer', 'stars', 'review_date', 'content']

    # 어플 페이지 접속
    browser.get(url)
    browser.implicitly_wait(3)
    time.sleep(1)
    title = browser.find_element(By.CSS_SELECTOR, value='div > h1 > span').text
    downloads = browser.find_element(
        By.CSS_SELECTOR, value='div > div > div:nth-child(2) > div.ClM7O').text
    try:
        rating = browser.find_element(
            By.CSS_SELECTOR, value='div:nth-child(1) > div.ClM7O > div > div').get_attribute('aria-label')
    except Exception as e:
        print('※', title, '은 안돼.')
        continue

    browser.find_element(
        By.CSS_SELECTOR, value='c-wiz > div > section > header > div > div > button').click()
    time.sleep(1)

    info = browser.find_element(
        By.CSS_SELECTOR, value='div > div.fysCi > div:nth-child(1)').text
    try:
        release_date = browser.find_element(
            By.CSS_SELECTOR, value='div.VfPpkd-wzTsW > div > div > div > div > div.fysCi > div.G1zzid > div:nth-child(9) > div.reAt0').text
    except:
        release_date = browser.find_element(
            By.CSS_SELECTOR, value='div.VfPpkd-wzTsW > div > div > div > div > div.fysCi > div.G1zzid > div:nth-child(7) > div.reAt0').text
    print("■", title, downloads, rating)
    print(release_date)
    print(info)

    browser.find_element(
        By.CSS_SELECTOR, value='div > div.t8iiQe > button').click()  # 앱정보 닫기
    browser.find_element(
        By.CSS_SELECTOR, value='div:nth-child(5) > div > div > button').click()  # 리뷰 모두 보기

    time.sleep(2)

    total_review_count = 0

    while True:
        try:
            reviews_bundle = browser.find_elements(
                By.CSS_SELECTOR, value='div.fysCi > div > div:nth-child(2) > div')
            current_review_count = len(reviews_bundle)
            print('current reviews_bundle count: {}'.format(current_review_count))

            # 만약 현재 리뷰 개수가 이전과 동일하다면 더 이상 총 리뷰 갯수가 갱신되지 않은 것이므로 종료합니다.
            if current_review_count == total_review_count:
                print('Total review count is not updating. Exiting the loop.')
                break

            # 현재 리뷰 개수를 total_review_count에 업데이트합니다.
            total_review_count = current_review_count

            # 마지막 리뷰를 클릭하고 잠시 기다립니다.
            reviews_bundle[current_review_count - 1].click()
            time.sleep(2)

        except Exception as e:
            print('An error occurred:', str(e))
            break

    print('Total review count: ', total_review_count)

    time.sleep(2)

    reviews_bundle = browser.find_elements(
        By.CSS_SELECTOR, value='div.fysCi > div > div:nth-child(2) > div')

    for review in reviews_bundle:
        try:
            reviewer = review.find_element(
                By.CSS_SELECTOR, value='div.fysCi > div > div> div> header > div.YNR7H > div.gSGphe > div').text
            review_date = review.find_element(
                By.CSS_SELECTOR, value='div.fysCi > div > div> div > header > div > span').text
            stars = review.find_element(
                By.CSS_SELECTOR, value='div.fysCi > div > div > div > header > div.Jx4nYe > div').get_attribute('aria-label')
            content = review.find_element(
                By.CSS_SELECTOR, value='div.fysCi > div > div:nth-child(2) > div > div.h3YV2d').text
            review_list = [title, downloads, rating, release_date,
                           info, reviewer, stars, review_date, content]
            reviews_list.append(review_list)
        except Exception as e:
            print('An error occurred:', str(e))
            break
    print(reviews_list[0:10])

    # reviews_list를 Mongodb에 추가
    df_reviews = pd.DataFrame(data=reviews_list, columns=columns_name)
    data_dict = df_reviews.to_dict(orient='records')
    collection.insert_many(data_dict)
    cnt = len(reviews_list)
    print("전체 댓글  :", len(reviews_bundle))
    print("저장된 댓글 :", cnt)
    cnt_total_db += cnt
    print("DB 업로드 댓글 :", cnt_total_db)

browser.quit()
