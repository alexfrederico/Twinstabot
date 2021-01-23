# -*- encoding: utf-8 -*-
from instabot import Bot
import os
from word_processor import create_stopwords, regex_word_removal, remove_stop_words, create_hashtags, analyze_feeling
from twitter_scraper import extract_tweet_list, driver_creation, extract_trends
from image_processor import create_image, create_word_cloud_image
from docs.config import LOGIN, PASSWORD, PAGE, CSS_SELECTOR, CSS_SELECTOR_2, SEARCH_PAGE

if __name__ == "__main__":

    bot = Bot()
    bot.login(username=LOGIN,password=PASSWORD)
    driver = driver_creation(PAGE)
    trends = extract_trends(driver,CSS_SELECTOR)
    print(trends)

    for trend in trends[:5]:
        try:
            stopwords = create_stopwords()

            image_name = "generated_image.jpg"
            image = create_image()

            tweets = extract_tweet_list(driver,SEARCH_PAGE,CSS_SELECTOR_2,trend)

            filtred_tweets = [regex_word_removal(tweet) for tweet in tweets]
            filtred_tweets_without_stopwords = [remove_stop_words(tweet,stopwords) for tweet in filtred_tweets]

            hashtags = create_hashtags(filtred_tweets,filtred_tweets_without_stopwords)
            create_word_cloud_image(' '.join(filtred_tweets_without_stopwords),image,stopwords,image_name)

            sentiments = [analyze_feeling(tweet) for tweet in filtred_tweets]

            caption_instagram = str("Trend: "+trend+
                                    "\n"+str(len(tweets))+" tweets extraidos no qual:"
                                    "\n"+str(sentiments.count("neu"))+" são neutros;"
                                    "\n"+str(sentiments.count("neg"))+" são negativos;"
                                    "\n"+str(sentiments.count("pos"))+" são positivos."
                                    "\n"+hashtags)

            bot.upload_photo(image_name,caption=caption_instagram)
            os.remove(image_name+'.REMOVE_ME')
        except Exception as error:
            print(trend,error)

    driver.close()