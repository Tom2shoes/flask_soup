from bs4 import BeautifulSoup as bs
from splinter import Browser
from time import sleep
import pandas as pd
import requests


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    scrape_data = {}
    browser = init_browser()
# Part 1
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    nasa_soup = bs(browser.html, 'lxml')
    # save to dictionary scrape_data
    scrape_data["news_title"] = nasa_soup.find("div", class_="content_title").find("a").text
    scrape_data["news_p"] = nasa_soup.find("div", class_="article_teaser_body").text
# Part 2
    jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl)
    browser.click_link_by_partial_text('FULL IMAGE')
    sleep(2)
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
    facts_df.to_html('html_table.html')
# Part 5
    hemisphere_image_urls = []
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    usgs_soup = bs(browser.html, 'lxml')

    image_titles = usgs_soup.find_all("h3")

    for title, x in zip(image_titles, range(1, 5)):
        browser.click_link_by_partial_text(title.text)
        browser.click_link_by_partial_href('.jpg')
        img_url = browser.windows[x].url
        browser.windows[0]
        browser.back()
        hemisphere_image_urls.append({"title": title.text, "img_url": img_url})
    # save to dictionary scrape_data
    scrape_data["hemisphere_image_urls"] = hemisphere_image_urls

    print(scrape_data)
    return scrape_data


scrape()
