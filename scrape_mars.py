from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# Create an instance of Flask
app = Flask(__name__)

def init_browser():
    executable_path = {"executable_path": "/Users/Soraiya Professional/Downloads/chromedriver_win32"}
    return Browser("chrome", **executable_path, headless=False)

scraped_data = {}

def scrape():
    browser = init_browser()

    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    news_html = browser.html
    news_soup = BeautifulSoup(news_html, "html.parser")

    scraped_data["news_title"] = news_soup.find("div", class_="content_title")[0].get_text()
    scraped_data["news_p"] = news_soup.find("div", class_="article_teaser_body")[0].get_text()
    
    browser.quit()

    browser = init_browser()
    
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, "html.parser")

    result_img = jpl_soup.find('article')['style']
    
    homepage = 'https://www.jpl.nasa.gov/'
    featured_image = result_img.replace("background-image: url('/","")
    featured_image = featured_image.replace("');","")

    featured_image_url = homepage + featured_image

    scraped_data["features_image_url"] = featured_image_url    

    browser.quit()

    browser = init_browser()

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    weather_html = browser.html
    weather_soup = BeautifulSoup(weather_html, "html.parser")

    scraped_data["mars_weather"] = weather_soup.find('p', class_= 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').get_text()

    browser.quit()

    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    mars_df = tables[0]
    mars_df.columns=['Description', 'Value']
    html_table = mars_df.to_html()
    html_table = html_table.replace('\n', '')

    scraped_data["mars_facts"] = html_table

    browser = init_browser()

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')

    results_hemi = hemisphere_soup.find_all('div', class_='item')

    homepage_url = 'https://astrogeology.usgs.gov'
    hemisphere_image_urls = []

        for result in results_hemi: 
            title = result.find('h3').text
            search_url = result.find('a')['href']
            browser.visit(homepage_url + search_url)
            image_html = browser.html
            image_soup = BeautifulSoup(image_html, 'html.parser')
            url = image_soup.find('div', class_='downloads')
            url = url.find_all('li')[1]
            url = url.a['href']
            hemisphere_image_urls.append({'title': title, 'image_url': url})
    
    scraped_data["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()

    return scraped_data
