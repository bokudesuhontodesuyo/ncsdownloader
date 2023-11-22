from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import urllib.request
import sys
import re

if __name__ == '__main__':
    totalimgs = 0
    wantimgs = 0
    nowpagenum = 1
def typeq():
    global totalimgs,wantimgs

    q = str(input('検索ワードを入力:')).replace('0','０').replace('1','１').replace('2','２').replace('3','３').replace('4','４').replace('5','５').replace('6','６').replace('7','７').replace('8','８').replace('9','９')
    wantimgs = int(input('取得枚数を入力:'))
    return str(q).replace(' ','%20').replace('　','%20')

def login():
    mail = 'mamamap777@gmail.com'
    pw = 'autopw0281'

    login_btn_xpath = '/html/body/div[1]/div/div/div/div[2]/a'
    login_btn = driver.find_element(by=By.XPATH, value = login_btn_xpath)
    login_btn.click()

    mail_form_xpath = '/html/body/div[2]/div/div/div[1]/form/p[1]/input'
    pw_form_xpath = '/html/body/div[2]/div/div/div[1]/form/p[2]/input'
    submit_btn_xpath  = '/html/body/div[2]/div/div/div[1]/form/p[3]/input'
    mail_form = driver.find_element(by=By.XPATH, value = mail_form_xpath)
    pw_form = driver.find_element(by=By.XPATH, value = pw_form_xpath)
    submit_btn = driver.find_element(by=By.XPATH, value = submit_btn_xpath)
    mail_form.send_keys(mail)
    pw_form.send_keys(pw)
    submit_btn.click()
    

options=Options()
# options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--log-level=1')

qw = typeq()
print('-----Start!!!-----')
print('↓↓↓↓↓トータル↓↓↓↓↓↓')

tar_url = f'https://seiga.nicovideo.jp/search/{qw}?page=1&target=illust&sort=comment_created'

driver = webdriver.Chrome(options=options)

driver.get(tar_url)

def getimgs():
    global totalimgs,wantimgs

    for i in range(100):
        driver.execute_script('window.scrollBy(0, 100);')
    sleep(0.5)

    mahirons = driver.find_elements(by=By.CSS_SELECTOR, value='.center_img_inner')

    count = 0

    for i in range(len(mahirons)):
        if totalimgs < wantimgs:
            mahirons[count].click()
            sleep(0.5)
            try:
                img_element1 = driver.find_element(By.ID, "illust_link")
                img_element1.click()
                sleep(0.5)
                img_xpath = '/html/body/div/div[2]/img'
                sleep(0.1) 
                driver.switch_to.window(driver.window_handles[1])
                img_element2 = driver.find_element(by=By.XPATH, value=img_xpath)
                img_url = img_element2.get_attribute('src') 
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.back()

                opener=urllib.request.build_opener()
                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(img_url,'dls\\'+str(count)+'.png')

                print(totalimgs)
                count += 1
                totalimgs += 1

                mahirons = driver.find_elements(by=By.CSS_SELECTOR, value='.center_img_inner')
            except:
                print('NONO')
                pass
        else:
            endpage()

def gonextpage():
    global nowpagenum
    numcount = nowpagenum + 1
    print(f'---次ページ{numcount}へ!---')
    next_url = re.sub('\d',str(numcount),tar_url)
    nowpagenum += 1
    driver.get(next_url)

def endpage():
    global totalimgs,wantimgs

    print('-----Finish!!!-----')
    print('設定:'+str(wantimgs))
    print('取得:'+str(totalimgs))
    print('-------------------')

    driver.quit()
    sys.exit()

login()
sleep(1)
while totalimgs < wantimgs:
    getimgs()
    sleep(0.1)
    gonextpage()
    sleep(1)

    driver.quit()
