from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import sys
import subprocess
import random
import re

intermediary_article_list = []
master_article_list = []
master_title_list = []


def proxy_disconnect():

    disconnect = subprocess.Popen(['windscribe', 'disconnect'], stdout=subprocess.PIPE)
    d_output_raw = str(disconnect.communicate())
    regex = r'(\w*)'
    d_output_final = str(re.findall(regex, d_output_raw)).replace(",", "").replace("'", "").replace(u'x08', "")

    disconnected_proxy = "DISCONNECTED" in d_output_final

    if disconnected_proxy:
        print("successfully disconnected from proxy")
    else:
        print("URGENT: unable to disconnect, kill process")

    sys.exit()


def intermediary_article_tracker():

    print("Intermediary article list length:" + str(len(intermediary_article_list)))
    # print(str(intermediary_article_list))

    if len(intermediary_article_list) >= 4:

        print("Maximum length of intermediary articles reached. Transferring articles to master list")
        for i in intermediary_article_list:
            master_article_list.append(i)
            print("master article list appended")
        intermediary_article_list.clear()
        print("Intermediary articles cleared.")
        print("master article list:" + str(master_article_list))
        for i in master_article_list:
            with open('ttArticles.csv', 'a') as wtArticles:
                wtArticles.write(str(i) + ',')
                print("Master article written to CSV.")
        master_article_list.clear()
        print("Master articles cleared.")
        proxy_disconnect()

    else:
        fill_temp_articles()


def fill_temp_articles():

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'/path_to/geckodriver')
    print("Loading Toutiao main page.")
    driver.get('http://www.toutiao.com')

    driver.get("https://www.toutiao.com")
    driver.find_element_by_xpath("//input[@class='tt-input__inner']").send_keys("美国")

    driver.find_element_by_xpath("//button[@type='button']").click()
    print("Search terms entered. Loading results")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("Sleeping 10 seconds.")
    time.sleep(10)

    temp_articles_list = []
    links = driver.find_elements_by_xpath("//*[@class='link title']")

    for link in links:
        try:
            link.click()
            time.sleep(10)
            print("First related article clicked.")
            print("Sleeping 10 seconds.")
            driver.switch_to.window(driver.window_handles[1])
            print("temporary articles list:" + str(temp_articles_list))
            title = driver.find_element_by_xpath("//h1[@class='article-title']").text
            with open('ttTitles.csv', 'r') as rttitles:
                rrtitles = rttitles.read()
                if title in rrtitles:
                    print("Title already in ttTitles.csv")
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                else:
                    with open('ttTitles.csv', 'a') as wttitles:
                        wttitles.write(title + ",")
                        print(title + " written to CSV.")
                        body_element_list = driver.find_elements_by_xpath("//p")
                        body_list = []
                        for p in body_element_list:
                            body_list.append(p.text)
                        body = str(body_list).replace(",", "").replace("'", "").replace(u'\\u200c', "")
                        article_dict = {title: body}
                        if article_dict in temp_articles_list:
                            pass
                        elif article_dict in intermediary_article_list:
                            pass
                        elif article_dict in master_article_list:
                            pass
                        else:
                            temp_articles_list.append(article_dict)
                            print("Article added to temporary article list:" + title)
                            print("temporary article list:" + str(temp_articles_list))
                            if len(temp_articles_list) >= 2:
                                print("Maximum length for temporary articles reached.")
                                for i in temp_articles_list:
                                    intermediary_article_list.append(i)
                                    print("Intermediary articles appended.")
                                temp_articles_list.clear()
                                print("Temporary articles cleared.")
                                intermediary_article_tracker()
                        print("closing window")
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
        except NoSuchElementException:
            print("Article unavailable.")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except StaleElementReferenceException:
            print("Stale element.")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])


def proxy_connect():

    server_list = ["Paris", "Frankfurt", "Amsterdam", "Oslo", "Bucharest", "Zurich"]
    random_location = random.choice(server_list)
    print("connecting to random server")
    random_connect = subprocess.Popen(['windscribe', 'connect', random_location], stdout=subprocess.PIPE)
    rc_output_raw = str(random_connect.communicate())

    regex = r'(\w*)'
    rc_output_final = str(re.findall(regex, rc_output_raw)).replace(",", "").replace("'", "").replace(u'x08', "")

    proxy_connected = "Connected" in str(rc_output_final)

    if proxy_connected:
        print("successfully connected to proxy")
        for i in server_list:
            if i in rc_output_final:
                print("server: " + i)
            else:
                pass
        fill_temp_articles()
    else:
        print("connection unsuccessful")


# fill_temp_articles()
proxy_connect()

