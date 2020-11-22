from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import cv2
import nltk
from nltk.corpus import stopwords
from multiprocessing import Process
import re
from instabot import Bot
import os
from config import LOGIN, PASSWORD, PAGE, CSS_SELECTOR, CSS_SELECTOR_2, SEARCH_PAGE

#alt shift
#palavras - https://github.com/pythonprobr

#LOGIN = 'twinstabot_br'
#PASSWORD = 'MaTHiaS01'
#PAGE = 'https://twitter.com/explore/tabs/trending'
#CSS_SELECTOR = 'div.css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-b88u0q.r-ad9z0x.r-bcqeeo.r-vmopo1.r-qvutc0'#'div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-b88u0q.r-ad9z0x.r-bcqeeo.r-vmopo1.r-qvutc0'
#CSS_SELECTOR_2 = 'div.css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0'#'div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0'
#SEARCH_PAGE = 'https://twitter.com/search?q=*YOUR_SEARCH*&src=trend_click&vertical=trends'

def post_on_instagram(image_name, caption_instagram,login,senha):
    """
    docstring
    """
    bot = Bot()
    bot.login(username=login,password=senha)
    bot.upload_photo(image_name,caption=caption_instagram)

def delete_image(image_name):
    os.remove(image_name)
    os.remove(image_name+'.REMOVE_ME')

def create_stopwords():
    nltk.download('stopwords')
    stopwords_list = set(STOPWORDS)
    #stopwords.update(["da", "meu", "em", "você", "de", "ao", "os"])
    stopwords_list.update(stopwords.words('portuguese'))
    return stopwords_list

def regex_word_removal(text):
    filtered_text = re.sub(r'http[^ ]* ','', text) 
    filtered_text = re.sub(r'[^a-z]k+[^a-z]',' ', filtered_text) 
    for letter in 'abcdefghijklmnopqrstuvwxyzáãâàçéêíîóôõúûü':
        filtered_text = re.sub(r''+letter+'+',letter, filtered_text) 
    return filtered_text

def create_word_cloud_image(text,image,stopwords_list,image_name,width=1080,height=1080):
    #np.array(Image.open("example.jpg"))
    array_image = np.array(image)

    wordcloud = WordCloud(stopwords=stopwords_list,
                        background_color="white",
                        width=width, height=height, max_words=2000,
                        mask=array_image, max_font_size=200,
                        min_font_size=1).generate(text)
    fig, ax = plt.subplots(figsize=(15,15))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    plt.savefig(image_name)
    #plt.imshow(wordcloud)
    #return wordcloud

def create_image(width = 1080,height = 1080,rgb = (0, 0, 0)):
    # Creates a new image (3 RGB channels)
    image = np.zeros((height, width, 3), dtype = np.uint8)
    # Fill the black background
    cv2.rectangle(image, (0, 0), (width, height), rgb, -1)
    return image

def extract_tweets(driver,search_page,css_selector,search_word,max_page_down):
    tweets = []
    driver.get(search_page.replace('*YOUR_SEARCH*',search_word))
    sleep(2)
    for i in range(max_page_down):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight")
        sleep(2)
        for element in driver.find_elements_by_css_selector(css_selector):#find_elements_by_class_name('css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0')):#
            tweets += [element.text.replace('\n',' ').lower()]
    return tweets

def extract_concatenated_tweets(driver,search_page,css_selector,search_word,max_page_down=30,max_attempts=5):
    search_word = search_word.replace('#','%23').replace(' ','%20')
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver.get('https://twitter.com/search?q='+search_word+'&src=trend_click&vertical=trends')
    #sleep(2)
    #driver.maximize_window()
    #sleep(2)
    tweets = []
    attempts = 1
    while(True):
        try:
            tweets = extract_tweets(driver,search_page,css_selector,search_word,max_page_down)
            '''
            driver.get('https://twitter.com/search?q='+search_word+'&src=trend_click&vertical=trends')
            sleep(2)
            for i in range(max__page_down):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight")
                sleep(2)
                for element in driver.find_elements_by_css_selector('div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0'):#find_elements_by_class_name('css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0')):#
                    tweets += [element.text.replace('\n',' ').lower()]
            '''
            break
        except Exception as error:
            if(attempts>=max_attempts):
                #driver.close()
                raise Exception(str(attempts)+' failed attempts')
            print(search_word,error)
            attempts +=1
    concatenated_tweets = ' '.join(set(tweets))
    return concatenated_tweets
'''
def create_post(search_word,login,password):
    hashtag = search_word if '#' in search_word else '#'+search_word.replace(' ','')
    text = extract_tweets(search_word,30)
    text = regex_word_removal(text)
    stopwords_list = create_stopwords()
    image = create_image()
    create_word_cloud_image(text,image,stopwords_list,hashtag[1:])
    post_on_instagram(hashtag[1:],'Trend: '+search_word+'\n'+hashtag,login,password)
    #delete_image(hashtag[1:])
'''

def teste(x,y,z,a):
    post_on_instagram(x,y,z,a)

#'''
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


#bot = Bot()
#bot.login(username=LOGIN,password=PASSWORD)
driver = driver_creation(PAGE)
#trends = extract_trends(driver,CSS_SELECTOR)
trends = ['teste']
#bot.upload_photo('balançogeralrj.jpg',caption='#balançogeralrj')
#print(trends)
#exit(0)    

#if __name__ == "__main__":

for trend in trends:
    try:
        hashtag = trend if '#' in trend else '#'+trend.replace(' ','')
        image_name = hashtag[1:]+".jpg"

        text = extract_concatenated_tweets(driver,SEARCH_PAGE,CSS_SELECTOR_2,trend)
        print(text)
        text = regex_word_removal(text)

        stopwords_list = create_stopwords()
        image = create_image()

        create_word_cloud_image(text,image,stopwords_list,image_name)
        caption_instagram = str("Trend: "+trend+"\n"+hashtag)

        #bot.upload_photo(image_name,caption=caption_instagram)
        os.remove(image_name+'.REMOVE_ME')
    except Exception as error:
        print(trend,error)

driver.close()
#'''
#process = Process(target=create_post, args=(trend,'teste','teste',))
#process.start()
#process.join()
    
