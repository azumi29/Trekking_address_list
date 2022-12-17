import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv

# # Chromを開いたままにする
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)

# headless mode
from selenium.webdriver.chrome.options import Options
options = Options()
# options.add_argument('--headless') # ←←←headless modeの切り替え


# Chromを呼び出す
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
target_url = 'https://www.google.com'
driver.get(target_url)  
sleep(3)
print('動作確認')


# 「ログインせずに使う」ボタンクリック
try:
    sleep(3)
    iframe = driver.find_element(By.CSS_SELECTOR,'#gb > div > div:nth-child(3) > iframe')# iframeに切り替える
    driver.switch_to.frame(iframe)# iframeに切り替える
    button = driver.find_element(By.CSS_SELECTOR,'#yDmH0d > c-wiz > div > div > c-wiz > div > div > div > div.DRc6kd.bdn4dc > div.QlyBfb > button')
    sleep(3)
    button.click()
    sleep(3)

except Exception:
    error_flg = True
    print('×ボタン押下時にエラーが発生しました。')


# iframeからデフォルトに切り替える
driver.switch_to.default_content()


# shop_list作成
shop_list = []
with open('Trekking_shop_address.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        shop_list.append(row[1])
    del shop_list[0] # 1行目削除


# url_list作成
url_list = []
for shop in shop_list:
    driver.get(target_url)  
    serch_word_input = driver.find_element(By.NAME,'q')
    serch_word_input.send_keys(shop)
    sleep(1)
    serch_word_input.submit()
    sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.select_one('.yuRUbf a')
    url_list.append(urls.attrs['href'])
print(url_list)


# csvへ出力
df_trekking_shop_addess = pd.DataFrame({'会社名':shop_list,'URL':url_list})
print(df_trekking_shop_addess)
df_trekking_shop_addess.to_csv('df_trekking_shop_addess.csv',encoding='cp932', errors='ignore')