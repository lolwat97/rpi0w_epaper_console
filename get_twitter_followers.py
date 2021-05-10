from selenium import webdriver
import time
#from selenium import TimeUnit.SECONDS

PHANTOMJS_PATH = '/home/pi/bin/phantomjs'

driver = webdriver.PhantomJS(PHANTOMJS_PATH)
#driver.manage().timeouts().pageLoadTimeout(10, TimeUnit.SECONDS)
driver.set_window_size(1920, 1080)
driver.get("https://www.twitter.com/lolwatve")
time.sleep(5)
followers_element = driver.find_elements_by_css_selector('.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0.r-b88u0q')[1]
followers = followers_element.text
print(followers)
driver.close()