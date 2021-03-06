from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np

import time
import re

# Data crawling
def getContent(driver):

    html = driver.page_source
    # to access html tag for likes, content, hashtag, time, place

    soup = BeautifulSoup(html, 'html.parser')
    # to receive and store info using html tag

    # content(본문 내용)
    try:
        content = soup.select('div.MOdxS')[0].text
        # access content by its html tag and store them as text string
    except:
        content = None
        # if there is no content

    # hashtag
    instagram_tags = []
    ## create a list for storing hashtag contents
    # (each hashtag is treated as individual components)

    try:
        data = driver.find_element(By.CSS_SELECTOR, ".C7I1f.X7jCj") 
        # access content by its html tag
        tag_raw = data.text
        # store them as text string
        tags = re.findall('#[A-Za-z0-9가-힣]+', tag_raw)
        # find hashtag symbol(#) in the text string

        tag = ''.join(tags).replace("#"," ")
        # Before storing the data, remove hashtag symbol(#)
        tag_data = tag.split()
        # acknowledge each component by space(빈 칸)

        for tag_one in tag_data:
            # for loop to store each hashtag content in the list
            instagram_tags.append(tag_one)
            # store them in the list
    except:
        pass
    #if there is no hashtag in the post

    # date
    try:
        date = soup.select('time._1o9PC')[0]['title']
        # access content by its html tag and store them as text string
    except:
        date = None
        # for exception handling

    # like
    try:
        like = soup.select('section.EDfFK.ygqzn')[0].findAll('span')[-1].text
        # access content by its html tag and store them as text string
    except:
        like = None
        # if the post did not receive any likes at current time

    # location
    try:
        place = soup.select('div.M30cS')[0].text
        # access content by its html tag and store them as text string
    except:
        place = None
        # if post does not specify the location

    post_data = [like, content, date, place, instagram_tags]
    #store them in a list

    print(post_data)
    return post_data





driver = webdriver.Chrome()
## webdriver

url = "http://www.instagram.com/accounts/login/"
## url for accessing

driver.get(url)
## open the site

time.sleep(3)
## wait for the page to fully open


# Log in
ID = str(input("아이디를 입력하세요 : "))
Passwd = str(input("비밀번호를 입력하세요 : "))

inputid = driver.find_element(By.NAME, 'username')
#inputid = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
#inputid.clear()
##first method is to find ID component by how web named the input textfield
##second method(hidden) is to find ID component by html tag

inputid.send_keys(ID)
print('sucess: id')

inputPw = driver.find_element(By.NAME, 'password')
#inputPw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
#inputPw.clear()
## first method is to find password component by how web named the input textfield
## second method(hidden) is to find password component by html tag

inputPw.send_keys(Passwd)
print('sucess: pw')

time.sleep(2)
## wait for the site to input given info

login_ok_button = driver.find_element(By.CSS_SELECTOR, ".sqdOP.L3NKy.y3zKF     ")
## find the html tag for log in button

login_ok_button.click()
## take action on the button

time.sleep(3)
print('sucess: login')
## wait for the site to fully log in

## Find the user and crawl data
follow_data = []
# list to store each influencer's follower number
crawling_data = []
# list to store each post's data


# Crawl until user wants to stop
while True:

    user = str(input("Search for the user: "))
    # search for user you'd want to find

    if user == 'endcrawling':
        break
        # if user wants to stop crawling, exit loop
    else:
        profile = "http://www.instagram.com/" + str(user)
        # find the user by altering url
        driver.get(profile)
        # open the user profile page
        time.sleep(5)
        # wait for the site to load

        first = driver.find_element(By.CSS_SELECTOR, '.v1Nh3.kIKUG._bz0w')
        # access the first post on the profile by its html tag
        first.click()
        # click the given html tag
        time.sleep(3)
        # wait for the post to load

        html = driver.page_source
        # to access html tag for followers
        soup = BeautifulSoup(html, 'html.parser')
        # to receive and store info using html tag

        followers = soup.select("span.g47SY")[1]['title'][:10]
        #get follower data from the profile
        print(followers)

        follow_data.append(followers)
        # store current user's data

        for i in range(9):

            crawling_data.append(getContent(driver))
            # store current post's data

            right = driver.find_element(By.CSS_SELECTOR, "div.l8mY4.feth3")
            # access the button to reach next post on the profile by its html tag
            right.click()
            time.sleep(3)
            # wait for the post to load


follower_output = pd.DataFrame(follow_data, columns = ['followers'])
# to handle large amount of data, use Dataframe supported by pandas
follower_output.to_csv('./instagram_crawling_follower_data.csv')
# save the output data as csv file (can be accessed using excel or notepad)

data_output = pd.DataFrame(crawling_data, columns = ['like', 'content', 'date', 'place', 'tags'])
# to handle large amount of data, use Dataframe supported by pandas
data_output.to_csv('./instagram_crawling_post_data.csv')
# save the output data as csv file (can be accessed using excel or notepad)