# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_info():
    # NASA Mars News

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit URL redplanetscience.com
    url = "https://redplanetscience.com/"
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the latest news title
    news_title = soup.find('div', class_='content_title').text
    news_title

    # Get the paragraph text of latest news title
    news_p = soup.find('div', class_='article_teaser_body').text
    news_p

    # JPL Mars Space Images - Featured Images

    # Visit URL spaceimages-mars.com
    jpl_url = "https://spaceimages-mars.com/"
    browser.visit(jpl_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    # assign the url string to a variable called `featured_image_url`.
    relative_image_path = soup.find_all('img')[1]["src"]
    featured_image_url = jpl_url + relative_image_path

    featured_image_url

    # Mars Facts

    # Visit URL https://galaxyfacts-mars.com
    mars_url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(mars_url)
    tables

    # Check to ensure data is in tabular form
    type(tables)

    # Normalize indexing
    facts_df = tables[0]

    # Drop Earth column
    facts_df = facts_df.drop(columns=[2])

    # Rename columns
    facts_df = facts_df.rename(columns={0: "Mars Profile", 1: "Measurements"})

    # Drop first row of data
    facts_df = facts_df.drop([0])

    # Display DataFrame
    facts_df

    # Convert data to HTML string
    mars_facts = facts_df.to_html()
    mars_facts

    # Strip unwanted newlines to clean up the table
    mars_facts.replace('\n', '')
    print(mars_facts)

    # Mars Hemispheres

    # Visit URL https://marshemispheres.com/
    # Locate image url path
    mars_hem_url = "https://marshemispheres.com/"
    browser.visit(mars_hem_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Find image url links
    links = browser.find_by_css('a.product-item img')

    # Extract hemispheres item elements
    mars_items = soup.find_all('div', class_='item')

    # Create empty dictionary for hemisphere urls
    hem_img_urls=[]

    # Loop through each hemisphere item
    for item in mars_items:
        
        # Try/except for error handling
        try:
            # Extract title
            hem = item.find('div',class_='description')
            hem_title=hem.h3.text
            
            # Extract image url
            hem_url = hem.a['href']
            browser.visit(mars_hem_url + hem_url)
            
            # Visit URL and extract image link
            html=browser.html
            soup=bs(html,'html.parser')
            img_src=soup.find('li').a['href']

            if (hem_title and img_src):
                # Print results
                print('-'*25)
                print(hem_title)
                print(mars_hem_url+img_src)
                
            # Create dictionary for title and url
            hem_dict={
                'title': hem_title,
                'image_url': mars_hem_url + img_src
            }
            hem_img_urls.append(hem_dict)
        except Exception as e:
            print(e)

    # Create dictionary for all scraped data:
    mars_dict = {
        'hem_imgs': hem_img_urls,
        'news_title': news_title,
        'news_p': news_p,
        'featured_img': featured_image_url,
        'mars_facts': mars_facts
        
    }

        # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict