from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

webpage1 = requests.get("https://www.flipkart.com/search?q=smartwayches&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off") # page 1
webpage2 = requests.get("https://www.flipkart.com/search?q=smartwayches&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=2") # page 2
content1 = BeautifulSoup(webpage1.content, "html.parser")
content2 = BeautifulSoup(webpage2.content, "html.parser")
div_tags1 = content1.find_all('div', {'class' : ['_4rR01T', '_30jeq3']}) # classes of names and price in div tags
div_tags2 = content2.find_all('div', {'class' : ['_4rR01T', '_30jeq3']})
span_tags1 = content1.find_all('span', {'class' : ['_1lRcqv', '_2_R_DZ']}) # classes of rating and number of ratings in span tags
span_tags2 = content2.find_all('span', {'class' : ['_1lRcqv', '_2_R_DZ']})
names = []
sellingPrice = []
rating = []
numOfRatings = []
counter = 1 # so that redundant values are not read
for tag in div_tags1 :
    if tag.get('class')[0] == '_4rR01T':
        names.append(tag.text)
    elif tag.get('class')[0] == '_30jeq3' and counter <= 24:
        sellingPrice.append(tag.text)
        counter += 1

counter = 1 # counter reset
for tag in div_tags2:
    if tag.get('class')[0] == '_4rR01T':
        names.append(tag.text)
    elif tag.get('class')[0] == '_30jeq3' and counter <= 24:
        sellingPrice.append(tag.text)
        counter += 1
for tag in span_tags1 :
    if tag.get('class')[0] == '_1lRcqv':
        rating.append(tag.text)
    else:
        text = tag.text
        num = re.findall('[^\s]+', text)
        numOfRatings.append(num[0])
for tag in span_tags2 :
    if tag.get('class')[0] == '_1lRcqv':
        rating.append(tag.text)
    else:
        text = tag.text
        num = re.findall('[^\s]+', text)
        numOfRatings.append(num[0])

Data = {
'Name' : names,
'Selling Price' : sellingPrice,
'Rating' : rating,
'Number of Ratings' : numOfRatings
}
DataFrame = pd.DataFrame(Data)
DataFrame.to_excel('Wrist Watches on Flipkart.xlsx')
