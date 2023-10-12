from selenium import webdriver
import pymysql

import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import os


HOST = os.environ['DB_HOST']
PORT = int(os.environ['DB_PORT'])
USER = os.environ['DB_USER']
PASSWARD = os.environ['DB_PASSWARD']
DATABASE = os.environ['DB_DATABASE']
try:
    conn = pymysql.connect(host=HOST, port=PORT, user=USER,
                           passwd=PASSWARD, db=DATABASE, charset='utf8mb4')
    curr = conn.cursor()

    print('開始連接資料庫')
except:
    print('資料庫連接失敗')
    raise


options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 背景執行設定
driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.implicitly_wait(10)  # 如果在規定時間內網頁加載完成，則執行下一步，否則一直等到時間終止

url = 'https://tcfa30niusnews.tk/coupon/user/Coupon'
driver.get(url)
# 填入登入的帳號密碼
account = driver.find_element_by_xpath('//input[@id="LoginModel_Account"]')
account.send_keys("testuser")
password = driver.find_element_by_xpath('//input[@id="LoginModel_Password"]')
password.send_keys("12345678")
# 進行登入
driver.find_element_by_xpath(
    '//button[@class="btn btn-sm btn-primary"]').send_keys(Keys.ENTER)

# 取頁數
pageCount = driver.find_element_by_xpath(
    '/html/body/div[2]/div[2]/div/div/div/div/div/div[3]/div[2]/div/ul').find_elements(By.TAG_NAME, "a")

for table_index, table in enumerate(pageCount):
    if table_index > 2 or table_index < len(pageCount) - 2:
        driver.implicitly_wait(10)
        # 取td
        table = driver.find_element_by_xpath(
            '//*[@id="simple-table"]/tbody').find_elements(By.TAG_NAME, "td")
        arr = []
        for index, td in enumerate(table):
            # index % 10 == 0 表示一個tr的結束
            if index % 10 == 0 and index != 0:

                if int(arr[8]) == 0:
                    percent = '0.00%'
                else:
                    percent = '{:.2f}%'.format(int(arr[9])/int(arr[8])*100)

                curr.execute(
                    "SELECT `getCount`, `useCount` FROM `coupon`  where `title`= %s and `subTitle` =%s ORDER BY `data_time` DESC limit 1", (arr[3], arr[4]))

                row = curr.fetchone()

                # 表示過去沒有這筆主標題+副標題的資料
                if row == None:

                    curr.execute("""INSERT INTO `coupon`(`title`, `subTitle`, `getTime`, `useTime`, `publishCount`, `getCount`, `getSubCount`, `useCount`, `useSubCount`, `usePercent`) VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                                 (arr[3], arr[4], arr[5], arr[6], arr[7], int(arr[8]), int(arr[8]), int(arr[9]), int(arr[9]), percent))
                    conn.commit()  # 確認送出(必要)
                else:
                    curr.execute("""INSERT INTO `coupon`(`title`, `subTitle`, `getTime`, `useTime`, `publishCount`, `getCount`, `getSubCount`, `useCount`, `useSubCount`, `usePercent`) VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                                 (arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], str(int(row[0]) - int(arr[8])), arr[9], str(int(row[1]) - int(arr[9])), percent))
                    conn.commit()  # 確認送出(必要)
                arr = ['']
            elif index != 0 and (index % 10 == 8 or index % 10 == 9):
                data = td.text.split('\n')
                dataSplit = data[0].split(":")
                arr.append(dataSplit[1])
                if index + 1 == len(table):
                    curr.execute(
                        "SELECT `getCount`, `useCount` FROM `coupon`  where `title`= %s and `subTitle` =%s ORDER BY `data_time` DESC limit 1", (arr[3], arr[4]))

                    row = curr.fetchone()

                    # 表示過去沒有這筆主標題+副標題的資料
                    if row == None:

                        curr.execute("""INSERT INTO `coupon`(`title`, `subTitle`, `getTime`, `useTime`, `publishCount`, `getCount`, `getSubCount`, `useCount`, `useSubCount`, `usePercent`) VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                                     (arr[3], arr[4], arr[5], arr[6], arr[7], int(arr[8]), int(arr[8]), int(arr[9]), int(arr[9]), percent))
                        conn.commit()  # 確認送出(必要)
                    else:
                        curr.execute("""INSERT INTO `coupon`(`title`, `subTitle`, `getTime`, `useTime`, `publishCount`, `getCount`, `getSubCount`, `useCount`, `useSubCount`, `usePercent`) VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                                     (arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], str(int(row[0]) - int(arr[8])), arr[9], str(int(row[1]) - int(arr[9])), percent))
                        conn.commit()  # 確認送出(必要)
            else:
                arr.append(td.text)
        ul = driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div/div/div/div/div[3]/div[2]/div/ul').find_elements(By.TAG_NAME, "a")
        ul[table_index + 1].click()

curr.close()
conn.close()
driver.quit()
