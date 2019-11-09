from splinter import Browser
from bs4 import BeautifulSoup
import time

def init_browser():

    executable_path = {"executable_path": "c:/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
## News Data ##

    # initiate the browser
    browser = init_browser()
    time.sleep(3)

    # visit the site
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(3)

    # scrape page into soup
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, 'html.parser')

    # get data
    title_results = news_soup.find_all('div', class_='content_title')
    news_title = title_results[0].text

    article_results = news_soup.find_all('div', class_='article_teaser_body')
    news_p = article_results[0].text

## Mars Images ##

    # initiate the browser
    browser = init_browser()
    time.sleep(1)

    # visit the site
    image_url = 'https://www.jpl.nasa.gov/spaceimages/'
    browser.visit(image_url)

    # scrape page into soup
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')

    # get data
    image_results = image_soup.find('img', class_='thumb')
    image_results = image_results['src'].replace("/spaceimages/", "")
    featured_image_url = image_url + image_results

## Mars Weather ##

    # initiate the browser
    browser = init_browser()
    time.sleep(1)

    # visit the site
    weather_url = 'https://twitter.com/marswxreport'
    browser.visit(weather_url)

    # scrape page into soup
    weather_html = browser.html
    weather_soup = BeautifulSoup(weather_html, 'html.parser')

    # get data
    weather_results = weather_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars_weather = weather_results

## Mars Heispheres ##

    # initiate the browser
    browser = init_browser()
    time.sleep(1)

    # visit the site
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    # scrape page into soup
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')

    # get data
    time.sleep(1)
    hemi_results = hemi_soup.find_all('div', class_='description')

    hemi_title_list = []
    hemi_url_list = []

    for result in hemi_results:
    # Error handling
        try:
            # Identify and return title of hemisphere
            hemi_name = result.find('h3').text.replace(" Enhanced", "")
            hemi_image = result.a['href'].replace("/search/map","")

        
            # Update hemi image URL based on href text
            hemi_image_url = "https://astropedia.astrogeology.usgs.gov/download" + hemi_image + ".tif/full.jpg"

            hemi_title_list.append(hemi_name)
            hemi_url_list.append(hemi_image_url)
        
        except AttributeError as e:
            print(e)
    
    # store dictionaries

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather" : mars_weather,
        "title_0" : hemi_title_list[0],
        "img_url_0": hemi_url_list[0],
        "title_1" : hemi_title_list[1],
        "img_url_1": hemi_url_list[1],
        "title_2" : hemi_title_list[2],
        "img_url_2": hemi_url_list[2],
        "title_3" : hemi_title_list[3],
        "img_url_3": hemi_url_list[3],
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data