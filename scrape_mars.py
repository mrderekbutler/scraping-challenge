import pandas as pd
import numpy as np
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import requests
import time

# --------------------------------------------------------------------------
# Initialize splinter Browser object
# --------------------------------------------------------------------------
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


# --------------------------------------------------------------------------
# Convert Jupyter notebook into a Python script called scrape_mars.py with
# a function called scrape that will execute all of scraping code and return
# one Python dictionary containing all of the scraped data.
# --------------------------------------------------------------------------
def scrape():
    # Scrape all functions and return all the data collected into a dictionary
    mars_scrape_data = {}
    mars_scrape_data["news_data"] = mars_news()
    mars_scrape_data["featured_image_url"] = mars_featured_image()
    mars_scrape_data["mars_weather"] = mars_weather()
    mars_scrape_data["mars_facts"] = mars_facts()
    mars_scrape_data["mars_hemispheres"] = mars_hemispheres()
    return mars_scrape_data

# --------------------------------------------------------------------------
# NASA Mars News 
# --------------------------------------------------------------------------
def mars_news():
    browser = init_browser()
    
    # URL of page to be scraped using splinter to open the web page
    url_mars_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_mars_news)
    time.sleep(2)
    
    # Scrape page into Soup
    html_mars_news = browser.html
    soup_mars_news = bs(html_mars_news, "html.parser")
    
    # find most recent article
    article = soup_mars_news.find("div", class_="list_text")
    
    # find article title
    mars_news_title = article.a.text.strip()

    # find article summary
    mars_news_summary = article.find("div", class_="article_teaser_body").text.strip()
    
    # Close the browser after scraping
    browser.quit()

    return mars_news_title, mars_news_summary

# --------------------------------------------------------------------------
# JPL Mars Space Images - Featured Image 
# --------------------------------------------------------------------------
def mars_featured_image():
    browser = init_browser()
    
    # Mars Space Images using splinter to create featured_image_url
    url_mars_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_mars_image)
    time.sleep(2)
    
    # fnd the image url to the full size .jpg image. Click on full image
    browser.click_link_by_id("full_image")
    time.sleep(2)

    # Scrape new page using beautiful Soup
    html_mars_image = browser.html
    soup_mars_image = bs(html_mars_image, "html.parser")

    # find the featured image by looking at images that use the fancybox-image class
    mars_image_url = soup_mars_image.find("img",class_="fancybox-image")["src"]
    
    # complete url string for this image
    featured_img_url = "https://www.jpl.nasa.gov" + mars_image_url

    # Close the browser after scraping
    browser.quit()
 
    return featured_img_url

# --------------------------------------------------------------------------
# Mars Weather - Visit the Mars Weather twitter account and scrape the
# latest Mars weather tweet from the page. Save the tweet text for the
# weather report as a variable called mars_weather
# --------------------------------------------------------------------------
def mars_weather():
    browser = init_browser()
    # URL of page to be scraped using splinter to open the web page
    url_mars_news = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_mars_news)
    time.sleep(2)
        
    # Scrape page into Soup
    html_mars_weather = browser.html
    soup_mars_weather = bs(html_mars_weather, "html.parser")

    # find the first tweet  
    mars_weather_tweet = soup_mars_weather.find('div', class_ = "js-tweet-text-container")
    
    # strip the text portion from the first tweet
    # first find the second tag <a> within the <p> tag
    # then get the prev tag 
    second_tag = mars_weather_tweet.find("a")
    mars_weather = second_tag.previousSibling.strip()

    # Close the browser after scraping
    browser.quit()

    return mars_weather

# --------------------------------------------------------------------------
# Mars Facts 
# --------------------------------------------------------------------------
def mars_facts():
    browser = init_browser()
    
    # URL of page to be scraped using splinter to open the web page
    url_mars_facts = "https://space-facts.com/mars/"
    browser.visit(url_mars_facts)
    time.sleep(2)

    # create the dataframe using pandas html read
    mars_facts_df = pd.read_html(url_mars_facts)
    mars_facts_df = (mars_facts_df[0])
    mars_facts_df.columns = ["Type", "Fact"]

    # use Pandas to_html method to generate HTML tables from DataFrames.
    mars_facts_html_table = mars_facts_df.to_html()
    mars_facts_html_table

    # strip unwanted newlines to clean up the table.
    mars_facts_html_table.replace('\n', '')
    
    # Close the browser after scraping
    browser.quit()
 
    return mars_facts_html_table

# --------------------------------------------------------------------------
# Mars Hemisperes 
# --------------------------------------------------------------------------
def mars_hemispheres():
    browser = init_browser()
    
    # URL of page to be scraped using splinter to open the web page,
    url_mars_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # allow browser to open the url
    browser.visit(url_mars_hemisphere)
    # wait 5 seconds for page to load
    time.sleep(2)

    # Scrape page into Soup
    #html_mars_hemisphere = browser.html
    #soup_mars_hemisphere = bs(html_mars_hemisphere, "html.parser")
    
    # list to contain the image url string for the full resolution hemisphere image, 
    # and the Hemisphere title containing the hemisphere name
    mars_hemispheres_list = []

    # Iterate through all 4 hemisphere images on mars
    for x in range(4):
        # wait 5 seconds before clicking on each image
        time.sleep(3)
    
        # Use splinter method "find by tag" to navigate and retrieve image link
        img_mars_hemisphere = browser.find_by_tag('h3')
    
        # click the link to pull up the image page
        img_mars_hemisphere[x].click()
    
        # Parse HTML with Beautiful Soup
        html_mars_hemisphere_image = browser.html
        soup_mars_hemisphere_image = bs(html_mars_hemisphere_image, 'html.parser')
    
        # Retrieve element that contain image information 
        url_mars_hemisphere_image = soup_mars_hemisphere_image.find("img", class_="wide-image")["src"]
    
        # Retrieve element that contain image title
        img_title_mars_hemisphere = soup_mars_hemisphere_image.find("h2",class_="title").text
    
        # Retrieve element that contain image url
        url_img_title_mars_hemisphere = 'https://astrogeology.usgs.gov'+ url_mars_hemisphere_image
    
        # Save both the image url string for the full resolution hemisphere image, 
        # and the Hemisphere title containing the hemisphere name to a 
        # Python dictionary to store the data using the keys img_url and title.
        mars_hemispheres_dict = {"title":img_title_mars_hemisphere,"img_url":url_img_title_mars_hemisphere}
    
        # Append the dictionary with the image url string and the hemisphere title to a list
        mars_hemispheres_list.append(mars_hemispheres_dict)
        
        # wiat 2 secondsbe before clicking the browser back arrow to get to the previous page
        time.sleep(2)
        browser.back()

    # Close the browser after scraping
    browser.quit()
           
    return mars_hemispheres_list

