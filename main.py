from selenium import webdriver

# Firefox
from selenium.webdriver.firefox.options import Options
# Chrome
#from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time
#import pync
import logging
import os
import datetime
import webbrowser
import pandas as pd

#logging.basicConfig(level=logging.DEBUG)
try:
    # Default Operations
    Options = Options()
    Options.add_argument("--incognito")
    #Options.add_argument("--headless")
    driver = webdriver.Firefox(options=Options, executable_path=r'/home/vh/Documents/geckodriver')
    #driver = webdriver.Firefox(executable_path=r'/home/vh/Documents/geckodriver')
    driver.delete_all_cookies()

    # + Add Feature to Select the Date Range
    #driver.find_element_by_id('btnSubmit').click()
    #driver.find_element_by_xpath("//select[@id='ddlAnnType']/option[text()='Equity']").click()
    #driver.find_element_by_xpath("//select[@id='ddlPeriod']/option[text()='Result']").click()


    # Start Scraping Data
    driver.get("https://www.bseindia.com/corporates/ann.html")
    #no_of_announcements = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div[2]')
    #print(no_of_announcements.text)

    #baseTable = driver.find_element_by_id("lblann")


    rows = len(driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[1]/tbody/tr'))
    #cols = len(driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[1]/tbody/tr[1]/td'))
    cols = 4
    print(rows)
    print(cols)

    pd.set_option('display.max_colwidth', None)
    #exc_time = ["Exchange Received Time", "Ex Disseminated Time", "Time Taken"]
    names = ["Company Name", "Update Type", "Symbol", "Exchange Time", "Announcement", "Security Code", "Subject", "PDF"]
    col = names
    df = pd.DataFrame(columns = col)

    for r in range(1, rows+1):
        column_info = []
        for c in range(1, cols):
            try:
                columns =  driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[{}]/tbody/tr[1]/td[{}]'.format(str(r), str(c))).text
                column_info.append(columns)

            except Exception as e:
                print(e)

        my_links = driver.find_elements_by_xpath("/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[{}]/tbody/tr[1]/td[1]/a").format(str(r))
        for link in my_links:
            link.click()
            announce = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[1]/td[1]').text
            co_name = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[1]/td[4]').text
            sec_code = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[1]/td[2]').text
            pdf = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[2]/td[5]/a').text

            column_info.extend([announce, co_name, sec_code])
            print(column_info)
            df['PDF'] = df['PDF'].apply(lambda pdf: '<a href="https://bseindia.com/{}">pdf link</a>'.format(pdf))
        print(column_info)

        for c in range(1, 2):
            try:
                columns = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[{}]/tbody/tr[2]/td/b[{}]'.format(str(r), str(c))).text
                column_info.append(columns)
            except Exception as e:
                print(e)
        print(column_info)

        #df.append(column_info)
        df.loc[len(df)] = column_info


    print("Processing BSE DATA")
    print(df)


    '''# Next Button
    #elem = driver.find_element_by_link_text('Next')
    try:
        elem = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div[1]/ul/li[9]/a')
        elem.click()
    except:
        pass'''

    #df = pd.read_csv("bse.txt", sep=" ", header=None, error_bad_lines=False)
    df.to_html("bse.html", escape=False)
    webbrowser.open("bse.html")

except Exception as e:
    print(e)
finally:
    driver.close()
    driver.quit()
