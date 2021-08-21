from selenium import webdriver

# Firefox
from selenium.webdriver.firefox.options import Options
# Chrome
# from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

import time
from datetime import datetime, date
from dateutil.parser import parse
import os
import datetime
import webbrowser
import pandas as pd
#import pync
# Debugging
import logging
import traceback

#logging.basicConfig(level=logging.INFO)
delay = 1  # seconds

# BSE Announcements Scraper | Formatter


def bse_data(from_date, to_date, segment):
    try:
        # File Save Location
        t = datetime.datetime.now().time()
        print("Current Time", t)
        #base_path = os.getcwd() + '/data/BSE_{}_{}_{}.html'
        #path = base_path.format(fd, td, t)
        driver_path = os.getcwd() + '/drivers/linux/geckodriver'
        base_path = os.getcwd() + '/data/BSE_{}_{}'
        fd = datetime.datetime.strptime(from_date, "%d/%m/%Y").date()
        td = datetime.datetime.strptime(to_date, "%d/%m/%Y").date()
        path = base_path.format(fd, td)

        # Default Operations
        op = Options()
        op.add_argument("--incognito")
        op.add_argument("--headless")
        op.add_argument("--maximize_window")
        driver = webdriver.Firefox(options=op, executable_path=driver_path)
        driver.maximize_window()
        #driver = webdriver.Firefox(executable_path=r'/home/vh/Documents/geckodriver') # ipython command
        driver.delete_all_cookies()

        # Start Scraping Data
        driver.get("https://www.bseindia.com/corporates/ann.html")
        time.sleep(0.8)
        no_of_announcements = driver.find_element_by_xpath(
            '/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div[2]')
        print(no_of_announcements.text)

        #elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'ddlAnnType')))
        #elem.send_keys("MF/ETFs").click()
        # Categories | INPUT Data
        segment_bar = driver.find_element_by_id('ddlAnnType')
        segment_bar.send_keys(segment)
        category_bar = driver.find_element_by_id('ddlPeriod')
        category_bar.send_keys('Result')
        from_bar = driver.find_element_by_id('txtFromDt')
        from_bar.clear()
        from_bar.send_keys(from_date)
        to_bar = driver.find_element_by_id('txtToDt')
        to_bar.clear()
        to_bar.send_keys(to_date)

        driver.find_element_by_id('btnSubmit').click()

        #baseTable = driver.find_element_by_id("lblann")
        # Check if any Announcements are available
        try:
            data = driver.find_element_by_xpath(
                '/html/body/div[1]/div[4]/div[2]/div[2]/div[2]').text
            if data == "No Records Found":
                print("No Records Found")
        except:
            #traceback.print_exc()
            pass
        # Next Button/Page
        n = 2
        try:
            p = len(driver.find_elements_by_xpath(
                '/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div[1]/ul/li'))
            print("Next Pages:", p)
        except Exception as e:
            print(e)
            p = 3

        matching_keywords = ["Presentation", "Transcript", "Press Release", "Amalgamation", "Buyback", "Contract",
                             "Delisting", "Demerger", "DRHP", "FDA", "Preference Shares", "Annual Report", "Result", "Board Meeting", "Dividend"]
        pd.set_option('display.max_colwidth', None)
        col = ["Symbol", "Subject", "Date", "More Info", "Category"]
        df = pd.DataFrame(columns=col)
        df1 = pd.DataFrame(columns=["PDF"])
        # Loop to get data from multiple pages of Announcements
        while True:
            n += 1
            rows = len(driver.find_elements_by_xpath(
                '/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table'))
            #cols = len(driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[1]/tbody/tr[1]/td'))
            cols = 3
            print("Rows", rows)
            # Loop through all the Announcements and save in a Dataframe
            for r in range(1, rows):
                column_info = []
                pdf_links = []
                my_links = driver.find_elements_by_xpath(
                    "/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[{}]/tbody/tr[1]/td[1]".format(str(r)))
                # Get Announcements Information from BSE
                for link in my_links:
                    link.click()
                    symbol = driver.find_element_by_xpath(
                        '/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[2]/td[2]').text
                    subject = driver.find_element_by_xpath(
                        '/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[1]/td').text
                    date = driver.find_element_by_xpath(
                        '/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[3]/td/b[1]').text
                    # Get More Information about Announcements from BSE
                    try:
                        more_info = driver.find_element_by_xpath(
                            '/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[5]/td').text
                    except:
                        more_info = driver.find_element_by_xpath(
                            '/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[6]/td').text
                        pass
                    # Get PDF Link from BSE
                    try:
                        pdf = driver.find_element_by_xpath(
                            '/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[2]/td[5]/a').get_attribute('href')
                    except Exception as e:
                        print(e)
                        pdf = 'NO PDF'
                        pass

                    column_info.extend([symbol, subject, date, more_info])
                    pdf_links.append(pdf)
                    print(pdf_links)

                    try:
                        elem = driver.find_element_by_xpath(
                            '/html/body/div[5]/div/div/div[2]/button').click()
                        #ActionChains(driver).move_to_element(elem).click()
                    except:
                        pass
                    time.sleep(0.1)
                # Scrolling of website
                try:
                    columns = driver.find_element_by_xpath(
                        '/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[{}]/tbody/tr[1]/td[2]'.format(str(r))).text
                    WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
                        (By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[{}]/tbody/tr[1]/td[2]'.format(str(r)))))
                except:
                    print("Website Not Scrolled")
                    pass
                column_info.append(columns)
                df1.loc[len(df1)] = pdf_links
                df.loc[len(df)] = column_info
            print("Processing BSE DATA")
            # Check for multiple pages of Announcements
            try:
                if n < p:
                    elem = driver.find_element_by_xpath(
                        '/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div[1]/ul/li[{}]/a'.format(str(n)))
                    elem.click()
                    print("Next Page")
                else:
                    break
            except Exception as e:
                print(e)
                pass
        path_html = path + '.html'
        path_csv = path + '.csv'
        df2 = pd.merge(df, df1, left_index=True, right_index=True)
        #df2.to_html(path+'.html', escape=False, render_links=True)
        df2.to_csv(path+'.csv', index=False)
    except Exception as e:
        print("Error in getting Data:", e)
        traceback.print_exc()
        df2 = pd.DataFrame()
    finally:
        driver.close()
        driver.quit()
        print("Completed")
        return path_csv, t


if __name__ == '__main__':
    now = datetime.date.today().strftime("%d/%m/%Y")
    print(now)
    segment = "MF/ETFs"
    df, path = bse_data(now, now, segment)
    webbrowser.open(path)
