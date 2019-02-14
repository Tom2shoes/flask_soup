from bs4 import BeautifulSoup as bs
from splinter import Browser
from time import sleep
import pandas as pd
import requests
import os
from selenium import webdriver


def init_browser():
    driver_path = os.environ.get('GOOGLE_CHROME_SHIM', None)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = driver_path
    chrome_options.add_argument('no-sandbox')
    chrome_options.add_argument('--headless')
    return Browser('chrome',
                   executable_path="chromedriver",
                   options=chrome_options,
                   headless=True)


def scrape():
    scrape_data = {}
    browser = init_browser()

    # Part 1
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    # save to dictionary scrape_data
    xpath_t = '//*[@id="page"]/div[2]/div/article/div/section/div/ul/li[1]/div/div/div[2]/a'
    scrape_data["news_title"] = browser.find_by_xpath(xpath_t).text
    xpath_p = '//*[@id="page"]/div[2]/div/article/div/section/div/ul/li[1]/div/div/div[3]'
    scrape_data["news_p"] = browser.find_by_xpath(xpath_p).text

    # Part 2
    jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl)
    browser.click_link_by_partial_text('FULL IMAGE')
    sleep(3)
    browser.click_link_by_partial_text('more info')
    sleep(1)
    browser.click_link_by_partial_text('.jpg')
    jpl_soup = bs(browser.html, 'lxml')
    # save to dictionary scrape_data
    scrape_data["featured_image_url"] = jpl_soup.find("img")["src"]

    # Part 3
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    twitter_response = requests.get(twitter_url)
    twitter_soup = bs(twitter_response.text, 'lxml')
    mars_weather = twitter_soup.find\
    ('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    # save to dictionary scrape_data
    scrape_data["mars_weather"] = mars_weather

    # Part 4
    facts_url = "http://space-facts.com/mars/"
    facts_table = pd.read_html(facts_url)

    facts_df = facts_table[0]
    facts_df.columns = ["Description", "Values"]
    facts_df.set_index('Description', inplace=True)

    html_table = facts_df.to_html()
    html_table.replace('\n', '')
    scrape_data["mars_facts"] = facts_df.to_html()

    # Part 5
    hemisphere_image_urls = []
    browser = init_browser()
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    usgs_soup = bs(browser.html, 'lxml')

    image_titles = usgs_soup.find_all(["h3"])

    if image_titles:
        for title, x in zip(image_titles, range(1, 5)):
                browser.click_link_by_partial_text(title.text)
                browser.click_link_by_partial_href('.jpg')
                img_url = browser.windows[x].url.strip()
                browser.windows[0]
                browser.back()
                hemisphere_image_urls.append({"title": title.text, "img_url": img_url})

    else:
        for i in range(1, 5):
            hemisphere_image_urls.append({"title": "Unavaliable due to Government Furlough", "img_url": "http://i.imgur.com/Zl0A6erm.jpg"})

    # save to dictionary scrape_data
    scrape_data["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()
    return scrape_data
