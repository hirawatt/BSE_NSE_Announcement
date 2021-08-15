from selenium import webdriver

# Firefox
from selenium.webdriver.firefox.options import Options
# Chrome
#from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import time
from datetime import datetime
#import pync
import logging
import os
import datetime
import webbrowser
import pandas as pd

# GUI
#import dearpygui.dearpygui as dpg
import streamlit as st


logging.basicConfig(level=logging.INFO)

try:
    # Default Operations
    Options = Options()
    Options.add_argument("--incognito")
    Options.add_argument("--headless")
    #Options.add_argument("--maximize_window")
    driver = webdriver.Firefox(options=Options, executable_path=r'/home/vh/Documents/geckodriver')
    driver.maximize_window()
    #driver = webdriver.Firefox(executable_path=r'/home/vh/Documents/geckodriver')
    driver.delete_all_cookies()

    # + Add Feature to Select the Date Range
    #driver.find_element_by_id('btnSubmit').click()
    #driver.find_element_by_xpath("//select[@id='ddlAnnType']/option[text()='Equity']").click()
    #driver.find_element_by_xpath("//select[@id='ddlPeriod']/option[text()='Result']").click()


    # Start Scraping Data
    driver.get("https://www.bseindia.com/corporates/ann.html")
    time.sleep(0.8)
    #no_of_announcements = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div[2]')
    #print(no_of_announcements.text)

    #baseTable = driver.find_element_by_id("lblann")
    data = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[2]').text
    if data == "No Records Found":
        print("No Records Found")
    # Next Button/Page
    n = 2
    try:
        p = len(driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div[1]/ul/li'))
        print(p)
    except Exception as e:
        print(e)
        p = 3

    matching_keywords = ["Presentation", "Transcript", "Press Release", "Amalgamation", "Buyback", "Contract", "Delisting", "Demerger", "DRHP", "FDA", "Preference Shares", "Annual Report", "Result", "Board Meeting", "Dividend"]
    pd.set_option('display.max_colwidth', None)
    col = ["Symbol", "Subject", "Date", "More Info", "Category"]
    df = pd.DataFrame(columns = col)
    df1 = pd.DataFrame(columns=["PDF"])
    while True:
        n +=1
        rows = len(driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table'))
        #cols = len(driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[1]/tbody/tr[1]/td'))
        cols = 3
        print(rows)
        print(cols)

        for r in range(1, rows):
            column_info = []
            pdf_links = []
            my_links = driver.find_elements_by_xpath("/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[{}]/tbody/tr[1]/td[1]".format(str(r)))
            for link in my_links:
                link.click()
                symbol    = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[2]/td[2]').text
                subject   = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[1]/td').text
                date      = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[3]/td/b[1]').text
                try:
                    more_info = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[5]/td').text
                except:
                    more_info = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[6]/td').text
                    pass
                pdf       = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[2]/td[5]/a').get_attribute('href')

                column_info.extend([symbol, subject, date, more_info])
                pdf_links.append(pdf)
                print(pdf_links)

                try:
                    driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/button').click()
                    #element = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/button')
                    #ActionChains(driver).move_to_element(element).click()
                except:
                    pass
                time.sleep(0.1)
            try:
                columns =  driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[{}]/tbody/tr[1]/td[2]'.format(str(r))).text
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[{}]/tbody/tr[1]/td[2]'.format(str(r)))))
            except:
                print("Website Not Scrolled")
                pass
            column_info.append(columns)
            print(column_info)

            df1.loc[len(df1)] = pdf_links
            df.loc[len(df)] = column_info


        print("Processing BSE DATA")
        print(df)
        print(df1)
        if n < p:
            elem = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div[1]/ul/li[{}]/a'.format(str(n)))
            elem.click()
        else:
            break
    #df.join(df1)
    df2 = pd.merge(df, df1, left_index=True, right_index=True)
    df2.to_html("bse.html", escape=False, render_links=True)
    webbrowser.open("bse.html")
except Exception as e:
    print(e)
finally:
    driver.close()
    driver.quit()
