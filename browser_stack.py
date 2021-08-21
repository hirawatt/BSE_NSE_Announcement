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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from threading import Thread
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
delay = 1 # seconds

caps=[{
      'os_version': '10',
      'os': 'Windows',
      'browser': 'chrome',
      'browser_version': 'latest',
      'name': 'Parallel Test1', # test name
      'build': 'browserstack-build-1', # Your tests will be organized within this build
      'browserstack.networkLogs': 'true',
      'browserstack.console': 'errors'
      },
      {
      'os_version': '10',
      'os': 'Windows',
      'browser': 'firefox',
      'browser_version': 'latest',
      'name': 'Parallel Test2',
      'build': 'browserstack-build-1',
      'browserstack.networkLogs': 'true'
      },
      {
      'os_version': 'Big Sur',
      'os': 'OS X',
      'browser': 'safari',
      'browser_version': 'latest',
      'name': 'Parallel Test3',
      'build': 'browserstack-build-1',
      'browserstack.networkLogs': 'true'
}]
# BSE Announcements Scraper | Formatter
def bse_data(from_date, to_date, segment, desired_cap):
    try:
        # File Save Location
        t = datetime.datetime.now().time()
        print("Current Time", t)
        #base_path = os.getcwd() + '/data/BSE_{}_{}_{}.html'
        #path = base_path.format(fd, td, t)
        base_path = os.getcwd() + '/data/BSE_{}_{}.html'
        fd = datetime.datetime.strptime(from_date, "%d/%m/%Y").date()
        td = datetime.datetime.strptime(to_date, "%d/%m/%Y").date()
        path = base_path.format(fd, td)

        # Default Operations
        #op = Options()
        #op.add_argument("--incognito")
        #op.add_argument("--headless")
        #op.add_argument("--maximize_window")
        #driver = webdriver.Firefox(options=op, executable_path=r'/home/vh/Documents/geckodriver')
        driver = webdriver.Remote(command_executor='https://vh_egnq4w:QzBnVrtpX69BViKuYqyy@hub-cloud.browserstack.com/wd/hub', desired_capabilities=desired_cap)
        #driver.maximize_window()
        #driver = webdriver.Firefox(executable_path=r'/home/vh/Documents/geckodriver') # ipython command
        driver.delete_all_cookies()

        # Start Scraping Data
        driver.get("https://www.bseindia.com/corporates/ann.html")
        time.sleep(0.8)
        no_of_announcements = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div[2]')
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
            data = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[2]').text
            if data == "No Records Found":
                print("No Records Found")
        except:
            #traceback.print_exc()
            pass
        # Next Button/Page
        n = 2
        try:
            p = len(driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div[1]/ul/li'))
            print("Next Pages:", p)
        except Exception as e:
            print(e)
            p = 3

        matching_keywords = ["Presentation", "Transcript", "Press Release", "Amalgamation", "Buyback", "Contract", "Delisting", "Demerger", "DRHP", "FDA", "Preference Shares", "Annual Report", "Result", "Board Meeting", "Dividend"]
        pd.set_option('display.max_colwidth', None)
        col = ["Symbol", "Subject", "Date", "More Info", "Category"]
        df = pd.DataFrame(columns = col)
        df1 = pd.DataFrame(columns=["PDF"])
        # Loop to get data from multiple pages of Announcements
        while True:
            n +=1
            rows = len(driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table'))
            #cols = len(driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[1]/tbody/tr[1]/td'))
            cols = 3
            print("Rows", rows)
            # Loop through all the Announcements and save in a Dataframe
            for r in range(1, rows):
                column_info = []
                pdf_links = []
                my_links = driver.find_elements_by_xpath("/html/body/div[1]/div[4]/div[2]/div[2]/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[{}]/tbody/tr[1]/td[1]".format(str(r)))
                # Get Announcements Information from BSE
                for link in my_links:
                    link.click()
                    symbol    = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[2]/td[2]').text
                    subject   = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[1]/td').text
                    date      = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[3]/td/b[1]').text
                    # Get More Information about Announcements from BSE
                    try:
                        more_info = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[5]/td').text
                    except:
                        more_info = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[6]/td').text
                        pass
                    # Get PDF Link from BSE
                    try:
                        pdf       = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/table/tbody/tr[2]/td[5]/a').get_attribute('href')
                    except Exception as e:
                        print(e)
                        pdf = 'No PDF'
                        pass

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
                # Scrolling of website
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
            #print(df)
            #print(df1)
            # Check for multiple pages of Announcements
            try:
                if n < p:
                    elem = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div[1]/ul/li[{}]/a'.format(str(n)))
                    elem.click()
                    print("Next Page")
                else:
                    break
            except Exception as e:
                print(e)
                pass
        df2 = pd.merge(df, df1, left_index=True, right_index=True)
        df2.to_html(path, escape=False, render_links=True)
    except Exception as e:
        print("Error in getting Data:",e)
        traceback.print_exc()
        df2 = pd.DataFrame()
    finally:
        driver.close()
        driver.quit()
        print("Completed")
        return df2, path, t

if __name__ == '__main__':
    now = datetime.date.today().strftime("%d/%m/%Y")
    segment = "MF/ETFs"
    for cap in caps:
        Thread(target=bse_data, args=(now, now, segment, cap,)).start()
    #df, path = bse_data(now, now, segment)
    #webbrowser.open(path)
