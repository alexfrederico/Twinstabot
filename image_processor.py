import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import cv2

def create_word_cloud_image(text,image,stopwords_list,image_name,width=1080,height=1080):
    array_image = np.array(image)

    wordcloud = WordCloud(stopwords=stopwords_list,
                        background_color="white",
                        width=width, height=height, max_words=2000,
                        mask=array_image, max_font_size=200,
                        min_font_size=1).generate(text)

    fig, ax = plt.subplots(figsize=(15,15))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    plt.tight_layout(pad=0)
    plt.savefig(image_name)

def create_image(width = 1080,height = 1080,rgb = (0, 0, 0)):
    # Creates a new image (3 RGB channels)
    image = np.zeros((height, width, 3), dtype = np.uint8)
    # Fill the black background
    cv2.rectangle(image, (0, 0), (width, height), rgb, -1)
    return image