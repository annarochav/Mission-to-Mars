#!/usr/bin/env python
# coding: utf-8

# # Scrape Mars Data: The News

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


#set your executable path, then set up the URL NASA Mars News for scraping.

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


#we'll assign the url and instruct the browser to visit it.
# Visit the mars nasa news site

url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
#we're searching for elements with a specific combination of tag (div) and attribute (list_text).
#we're also telling our browser to wait one second before searching for components. 
#The optional delay is useful because sometimes dynamic pages take a little while to load

browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


#we'll set up the HTML parser

html = browser.html
news_soup = soup(html, 'html.parser')

#look for the <div /> tag and its descendent (This is our parent element)
# The . is used for selecting classes
#CSS works from right to left
# with select_one, the first matching element returned is <li /> element with a class of slide and all nested elements.

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


#We'll want to assign the title and summary text to variables
#let's begin our scraping
#Which HTML attribute will we use to scrape the article’s title?
# R: class = “content_title”
# we've specified by saying, "The specific data is in a <div /> with a class of 'content_title'."

slide_elem.find('div', class_='content_title')


# In[6]:


#But we need to get just the text, and the extra HTML stuff isn't necessary.
# Use the parent element to find the first `a` tag and save it as `news_title`

news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


#Next we need to add the summary text.
# Use the parent element to find the paragraph text
#.find() is used when we want only the first class and attribute we've specified.
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# # Scrape Mars Data: Featured Image

# In[8]:


#  The next step is to scrape the featured image from another Mars website.
# Once the image is scraped, we'll want to add it to our web app as well.
# Let's start getting our code ready to automate all of the clicks.
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


#Next, we want to click the "Full Image" button.
#This button will direct our browser to an image slideshow.
#Let's take a look at the button's HTML tags and attributes with the DevTools.
# Since there are only three buttons, we can go ahead and use the HTML tag in our code.
# Find and click the full image button
#The indexing chained at the end stipulates that we want our browser to click the SECOND button.

full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


#We need to click the More Info button to get to the next page.
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


#Now we need to find the relative image URL. 
#It's important to note that the value of the src will be different every time the page is updated.
#We'll use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image.
## Find the relative image url
#Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."


img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


#if we copy and paste this link into a browser, it won't work. This is because it's only a partial link.
#we just need to add the first portion to our app.
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# # Scrape Mars Data: Mars Facts

# In[13]:


# the information we want to scrap is held in a table format.
# we'll just be copying the table's information from one page and place it into our application.
#Tables in HTML are basically made up of many smaller containers.The main container is the <table /> tag. 
#inside the table is <tbody />, which is the body of the table—the headers, columns, and rows.
#<tr /> is the tag for each table row. 
#the table data is stored in <td /> tags. This is where the columns are established.
# Instead of scraping each row, we're going to scrape the entire table with Pandas' .read_html() function.


# we're creating a new DataFrame from the HTML table.
# read_html() specifically searches for and returns a list of tables found in the HTML.
# By specifying an index of 0, we're telling Pandas to pull only the first table it encounters.

df = pd.read_html('https://galaxyfacts-mars.com')[0]

# Here, we assign columns to the new DataFrame for additional clarity.
df.columns=['Description', 'Mars', 'Earth']

#we're turning the Description column into the DataFrame's index. 
#inplace=True means that the updated index will remain in place

df.set_index('Description', inplace=True)
df


# In[14]:


# How do we add the DataFrame to a web application?
# Our data is live—if the table is updated, then we want that change to appear in the app also.
# Pandas also has a way to easily convert our DF back into HTML-ready code using the .to_html() function.

df.to_html()


# In[15]:


# Now we have everything, we can end the automated browsing session.
#This is an important line to add to our web app also.
# Without it, the automated browser won't know to shut down—it will continue to listen for instructions.
#it may put a strain on memory or a laptop's battery if left on. 

browser.quit()


# In[16]:


# Live sites are a great resource for fresh data, but the layout of the site may be updated
# there's a good chance your scraping code will break and need to be reviewed


# # Export to Python

# In[17]:


# we can't automate the scraping using the Jupyter Notebook. 
# To fully automate it, it will need to be converted into a .py file.
# The next step in making this an automated process is to download the current code into a Python file.
# it won't transition over perfectly, we'll need to clean it up a bit
#you need to delete the unnecesary comments and your done!


# # Store the Data

# In[18]:


# now we need to store the data in a spot where they can be easily accessed and retrieved as needed. 
# SQL isn't a good option because it works with tabular data.
# Mongo, a NoSQL database, is designed for exactly this task.
# Mongo is a non-relational database that stores data in Binary JavaScript Object Notation (JSON), or BSON format.
# We'll access data stored in Mongo the same way we access data stored in JSON files.


# In[19]:


#A Mongo database contains collections. 
#These collections contain documents, and each document contains fields, and fields are where the data is stored.


# # Deliverable 1: Scrape Full-Resolution Mars Hemisphere Images and Titles 

# ### Hemispheres

# In[22]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# In[23]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)

browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[24]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Parse the html with beautifulsoup

html = browser.html
hemi_soup = soup(html, 'html.parser')

# Get the links for each of the hemispheres
hemi_links = hemi_soup.find_all('h3')


# loop through each hemisphere

for hemi in hemi_links:
    # Navigate and click the link of the hemisphere
    img_page = browser.find_by_text(hemi.text)
    img_page.click()
    html= browser.html
    img_soup = soup(html, 'html.parser')
    img_url = 'https://astrogeology.usgs.gov/' + str(img_soup.find('img', class_='wide-image')['src'])
    title = img_soup.find('h2', class_='title').text
    hemi_dict = {'img_url': img_url,'title': title}
    hemisphere_image_urls.append(hemi_dict)
    browser.back()


# In[25]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[26]:


# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




