from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager

def extract_tweets(driver,search_page,css_selector,search_word,max_page_down):
    tweets = set()
    driver.get(search_page.replace('*YOUR_SEARCH*',search_word))
    sleep(2)
    for i in range(max_page_down):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight")
        sleep(2)
        for element in driver.find_elements_by_css_selector(css_selector):
            tweets.add(element.text.replace('\n',' '))
    return list(tweets)

def extract_tweet_list(driver,search_page,css_selector,search_word,max_page_down=30,max_attempts=5):
    search_word = search_word.replace('#','%23').replace(' ','%20')
    tweet_list = []
    attempts = 1
    while(True):
        try:
            tweet_list = extract_tweets(driver,search_page,css_selector,search_word,max_page_down)
            break
        except Exception as error:
            if(attempts>=max_attempts):
                raise Exception(str(attempts)+' failed attempts')
            print(search_word,error)
            attempts +=1
    if(len(tweet_list)==0):
        raise Exception('No tweets were extracted')
    return tweet_list

def extract_trends(driver,css_selector):
    trends=[]
    for element in driver.find_elements_by_css_selector(css_selector):
            trends += [element.text.replace('\n',' ').lower()]
    return trends

def driver_creation(page):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(page)
    sleep(2)
    driver.maximize_window()
    sleep(2)
    return driver
