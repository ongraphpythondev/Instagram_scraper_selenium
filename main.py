from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time
from collections import defaultdict

my_dict = defaultdict(list)
load_dotenv()
username = os.getenv('INS_USERNAME')
password = os.getenv('PASSWORD')
search_query = os.getenv('SEARCH_QUERY')



chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-notifications')
driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.instagram.com/'
# driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)

WebDriverWait(driver, 50).until(EC.presence_of_element_located((
    By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input'))).send_keys(username)
time.sleep(1)
WebDriverWait(driver, 50).until(EC.presence_of_element_located((
    By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input'))).send_keys(password)
time.sleep(1)

WebDriverWait(driver, 50).until(EC.element_to_be_clickable((
    By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div'))).click()
time.sleep(2)

# click search
WebDriverWait(driver, 50).until(EC.element_to_be_clickable((
    By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span/div/a/div/div[2]/div/div/span'))).click()
time.sleep(2)

# enter input
WebDriverWait(driver, 50).until(EC.presence_of_element_located((
    By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/input'))).send_keys(search_query)
time.sleep(2)
WebDriverWait(driver, 50).until(EC.presence_of_element_located((
    By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/a[1]/div[1]'))).click()



#number of post 
post_count = WebDriverWait(driver, 50).until(EC.presence_of_element_located((
    By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span'))).text


followers = WebDriverWait(driver, 50).until(EC.presence_of_element_located((
    By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span'))).text

following =WebDriverWait(driver, 50).until(EC.presence_of_element_located((
    By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span'))).text


print('post',post_count)
print('followers',followers)
print('following',following)



# last_height = driver.execute_script("return document.body.scrollHeight")

            
            

all_post = driver.find_elements(By.CLASS_NAME,"_aagw")
all_src = driver.find_elements(By.CLASS_NAME,'_aagv')
count=0
SCROLL_PAUSE_TIME = 2

scroll_post = 1

print('all_post',len(all_post))
for p in range(len(all_post)):
    scroll_post +=1
    print('scroll_post',scroll_post)
    if scroll_post == len(all_post):
        
        print("inside")
        print(last_height)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            
            driver.execute_script(f"window.scrollTo({last_height}, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            last_height = new_height
            scroll_post=0
            post = driver.find_elements(By.CLASS_NAME,"_aagw")
            src = driver.find_elements(By.CLASS_NAME,'_aagv')
            all_post.clear()
            all_src.clear()
            all_post.extend(post)
            all_src.extend(src)
            
            break           
            
    try:
        
        image = all_src[p].find_element(By.TAG_NAME, 'img')
        src = image.get_attribute('src')
    except:
        src=''
    my_dict['Post_Url'].append(src)

    print(dict(my_dict))
    print('--------------------------------------------')
    all_post[p].click()
    time.sleep(2)
    SCROLL_PAUSE_TIME=2
    while True:
        last_height = driver.execute_script("return document.querySelectorAll('._a9z6')[0].scrollHeight")
        driver.execute_script(f"document.querySelectorAll('._a9z6')[0].scrollTo(0, {last_height});")
        last_height = last_height + last_height
        time.sleep(SCROLL_PAUSE_TIME)
        comments = driver.find_elements(By.CLASS_NAME,'_a9zs')
        count +=len(comments)
        print('comments',len(comments),' | ', 'count',count)
        for i in comments:
            print(i.text)
        if count >= 100:
            # break
            count=0
            cut_off = driver.find_element(By.CSS_SELECTOR,'body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x160vmok.x10l6tqk.x1eu8d0j.x1vjfegm > div > div')
            cut_off.click()
            time.sleep(3)
            break
            
        try:
            load_more = driver.find_element(By.CSS_SELECTOR,'body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe.x1qjc9v5.xjbqb8w.x1lcm9me.x1yr5g0i.xrt01vj.x10y3i5r.xr1yuqi.xkrivgy.x4ii5y1.x1gryazu.x15h9jz8.x47corl.xh8yej3.xir0mxb.x1juhsu6 > div > article > div > div._ae65 > div > div > div._ae2s._ae3v._ae3w > div._ae5q._akdn._ae5r._ae5s > ul > li > div')
            load_more.click()
            time.sleep(2)
        except:
            count=0
            cut_off = driver.find_element(By.CSS_SELECTOR,'body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x160vmok.x10l6tqk.x1eu8d0j.x1vjfegm > div > div')
            cut_off.click()
            time.sleep(3)
            break
            
    
driver.quit()