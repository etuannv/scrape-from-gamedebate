#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = ["Tuan Nguyen"]
__copyright__ = "Copyright 2018, Tuan Nguyen"
__credits__ = ["Tuan Nguyen"]
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Production"
__author__ = "TuanNguyen"
__email__ = "etuannv@gmail.com"
__website__ = "https://webscrapingbox.com"


# Start import other
from base import *
import re
import requests
import csv
import shutil
from lxml import html
from lxml import etree
from urllib.parse import urljoin




def isBlocked(html_source):
    
    if "Access Denied" in html_source:
        return True
    else:
        return False
    

def getPropertyUrlFromPage(url):
    ''' Get all property url a page. Return list of dictionary'''
    is_next_page = False
    while not browser.getUrl(url):
        time.sleep(20)
        browser.getUrl(url)
        pass

    while isBlocked(browser.getPageSource()):
        logging.info('Proxy is blocked. Restarting the browser ...')
        browser.restartDriver()
        time.sleep(1)
        browser.getUrl(url)
    
    result = []  #{'category' :'-', 'url':'-',}

    #while not browser.isExistByXPath(".//*[@class='placard-details']//a", 2):
    #    logging.info("Waiting for page loading")
    #    pass
    
    root = lxml.html.fromstring(browser.getPageSource())

    cate = 'PC'
    # # cate
    # tag = root.xpath(".//li[@class='active']/a/text()")
    # if tag:
    #     cate = tag[0].strip()

    tag = root.xpath(".//div[@class='srRowFull']/div[1]/a/@href")
    for item in tag:
        if item is not None:
            result.append({'category': cate, 'url':  urljoin("http://www.game-debate.com",item.strip())})
    
    # Check next page
    # next_page = browser.findByXpath(".//a[@class='next_page']", 5)
    next_page = False
    if next_page:
        is_next_page = True
    

    return result, is_next_page

def getPropertyDetail(url, category):

    
    result = {
                'url': "-",
                'category': "-",
                'gtitle': "-",
                'image_url': "-",
                #'flatform': "-",
                'release_EU_UK': "-",
                'release_US': "-",
                'release_AU': "-",
                'release_date': "-",
                
                'm_intel_cpu': "-",
                'm_amd_cpu': "-",
                'm_nivdia_card': "-",
                'm_amd_card': "-",
                'm_vram': "-",
                'm_ram': "-",
                'm_os': "-",
                'm_directx': "-",
                'm_hdd': "-",
                'm_gd': "-",

                'r_intel_cpu': "-",
                'r_amd_cpu': "-",
                'r_nivdia_card': "-",
                'r_amd_card': "-",
                'r_vram': "-",
                'r_ram': "-",
                'r_os': "-",
                'r_directx': "-",
                'r_hdd': "-",
                'r_gd': "-",
                
            }
    
    browser.getUrl(url)
    time.sleep(1)

    while isBlocked(browser.getPageSource()):
        logging.info('Proxy is blocked. Restarting the browser ...')
        browser.restartDriver()
        time.sleep(1)
        browser.getUrl(url)

    # retry = 3
    # while not browser.isExistByXPath(".//th[text()='Symbol']/following-sibling::td",10):
    #     time.sleep(1)
    #     retry -= 1
    #     logging.info("Refesh page")
    #     browser.getUrl(url)
    #     if retry < 0:
    #         return None

    

    result['url'] = browser.getCurrentUrl()
    result['category'] = category


    root = lxml.html.fromstring(browser.getPageSource())
    
    # gtitle
    tag = root.xpath(".//span[@itemprop='name']/text()")
    if tag:
        result['gtitle'] = tag[0].strip()
    
    # image_url
    tag = root.xpath(".//img[@itemprop='image']/@src")
    if tag:
        result['image_url'] = tag[0].strip() 

    # image_url
    tag = root.xpath(".//img[@itemprop='image']/@src")
    if tag:
        result['image_url'] = tag[0].strip()
    
    # release_EU_UK
    tag = root.xpath(".//table[@class='tableRelease']/tbody/tr/td[text()='EU/UK:']/following::td[1]/a/text()")
    if tag:
        result['release_EU_UK'] = tag[0].strip()
    else:
        result['release_EU_UK'] = 'Unknown' 
    
    # release_US
    tag = root.xpath(".//table[@class='tableRelease']/tbody/tr/td[text()='US:']/following::td[1]/a/text()")
    if tag:
        result['release_US'] = tag[0].strip()
    else:
        result['release_US'] = 'Unknown' 

    # release_AU
    tag = root.xpath(".//table[@class='tableRelease']/tbody/tr/td[text()='AU:']/following::td[1]/a/text()")
    if tag:
        result['release_AU'] = tag[0].strip()
    else:
        result['release_AU'] = 'Unknown'
    
    # release_date
    tag = root.xpath(".//div[@class='gdateData']/text()")
    if tag:
        result['release_date'] = tag[0].strip()
    else:
        result['release_date'] = 'Unknown'
    

    #### Minimum requirement
    tag = root.xpath(".//div[@class='systemRequirementsTitle' and contains(text(),'Minimum')]/parent::div")
    if tag:
        tag = tag[0]
        # m_intel_cpu
        child = tag.xpath(".//div[@class='systemRequirementsLinkSubTop']/a/text()")
        if child:
            result['m_intel_cpu'] = child[0].strip()
        
        # m_amd_cpu
        child = tag.xpath(".//div[@class='systemRequirementsLinkSubBtm']/a/text()")
        if child:
            result['m_amd_cpu'] = child[0].strip()
        
        # m_nivdia_card
        child = tag.xpath(".//div[@class='systemRequirementsLinkSubTop graphics']/a/text()")
        if child:
            result['m_nivdia_card'] = child[0].strip()

        # m_amd_card
        child = tag.xpath(".//div[@class='systemRequirementsLinkSubBtm graphics']/a/text()")
        if child:
            result['m_amd_card'] = child[0].strip()
        
        # m_vram
        child = tag.xpath(".//span[contains(@title,'Minimum VRAM')]/text()")
        if child:
            result['m_vram'] = child[0].strip()
        
        # m_ram
        child = tag.xpath(".//span[contains(@title,'Minimum RAM')]/text()")
        if child:
            result['m_ram'] = child[0].strip()
        

        # m_os
        child = tag.xpath(".//span[contains(@title,'Minimum Operating System')]/text()")
        if child:
            result['m_os'] = child[0].strip()
        

        # m_directx
        child = tag.xpath(".//span[contains(@title,'Minimum Direct X')]/text()")
        if child:
            result['m_directx'] = child[0].strip()

        # m_hdd
        child = tag.xpath(".//span[contains(@title,'Minimum Hard Disk Drive Space')]/text()")
        if child:
            result['m_hdd'] = child[0].strip()
        
        
    
    #### Recommended requirement
    tag = root.xpath(".//div[@class='systemRequirementsTitle' and contains(text(),'Recommended')]/parent::div")
    if tag:
        tag = tag[0]
        # r_intel_cpu
        child = tag.xpath(".//div[@class='systemRequirementsLinkSubTop']/a/text()")
        if child:
            result['r_intel_cpu'] = child[0].strip()
        
        # r_amd_cpu
        child = tag.xpath(".//div[@class='systemRequirementsLinkSubBtm']/a/text()")
        if child:
            result['r_amd_cpu'] = child[0].strip()
        
        # r_nivdia_card
        child = tag.xpath(".//div[@class='systemRequirementsLinkSubTop graphics']/a/text()")
        if child:
            result['r_nivdia_card'] = child[0].strip()

        # r_amd_card
        child = tag.xpath(".//div[@class='systemRequirementsLinkSubBtm graphics']/a/text()")
        if child:
            result['r_amd_card'] = child[0].strip()
        
        # r_vram
        child = tag.xpath(".//span[contains(@title,'Recommended VRAM')]/text()")
        if child:
            result['r_vram'] = child[0].strip()
        
        # r_ram
        child = tag.xpath(".//span[contains(@title,'Recommended RAM')]/text()")
        if child:
            result['r_ram'] = child[0].strip()
        

        # r_os
        child = tag.xpath(".//span[contains(@title,'Recommended Operating System')]/text()")
        if child:
            result['r_os'] = child[0].strip()
        

        # r_directx
        child = tag.xpath(".//span[contains(@title,'Recommended Direct X')]/text()")
        if child:
            result['r_directx'] = child[0].strip()
        

        # r_hdd
        child = tag.xpath(".//span[contains(@title,'Recommended Hard Disk Drive Space')]/text()")
        if child:
            result['r_hdd'] = child[0].strip()
        

    
    return result


def checkContinue():
    result = False
    if os.path.exists(TempPath):
        #ask for continue
        os.system('clear')
        print ("============== ATTENTION !!! The previous session has not finished ==============")
        print("\n")
        is_continue = confirm(prompt='DO YOU WANT CONTINUE THE PREVIOUS SESSION?', resp=True)
        if not is_continue:
            logging.info("You choice start new session")
            print("\n")
            print("\n")
            try:
                # Delete all file in temp folder
                shutil.rmtree(TempPath)
                # Delete previous result
                # if ResultPath:
                #     os.remove(ResultPath)
            except OSError:
                
                sys.exit("Error occur when delete temp folder")
            result = False
        else:
            logging.info("You choice continue previous session")
            print("\n")
            print("\n")
            result = True
    createFolderIfNotExists(TempPath)
    return result

def getCateUrls(url):
    browser.getUrl(url)
    tags = browser.findAllByXpath(".//*[@class='PopCategories']//a", 5)
    result = []
    if tags:
        for tag in tags:
            result.append(tag.get_attribute('href'))
        return result
    else:
        return None

def getFilterUrl(url):
    browser.getUrl(url)
    time.sleep(1)
    tag = browser.findByXpath(".//button[contains(@ng-click,'toggleAdvancedFilters')]")
    if tag is None:
        return None
    
    browser.clickElement(tag)
    time.sleep(1)
    tag = browser.findByXpath(".//form[@name='advancedFilter']//input[@name='PriceRangeMax']")
    if tag:
        tag.send_keys("750000")
        time.sleep(0.5)
    
    tag = browser.findByXpath(".//button[contains(@ng-click,'filteredSearch')]")
    if tag:
        browser.clickElement(tag)
    
    time.sleep(2)
    while browser.getCurrentUrl == url:
        logging.info("Wating for page load...")
        time.sleep(1)
    
    return browser.getCurrentUrl()


def main(argv):
    global browser, CurrentPath, TempPath, ConfigPath
    # CurrentPath = os.path.dirname(os.path.realpath(__file__))
    CurrentPath = os.path.dirname(os.path.realpath(sys.argv[0]))
    ConfigPath = os.path.join(CurrentPath, 'config.ini')
    TempPath = os.path.join(CurrentPath, 'temp')
    ResultPath = os.path.join(TempPath, "result_temp.csv")
    

    # ======= CHECK IF WANT TO CONTINUE PREVIOUS SESSION ========
    checkContinue()
    
    # READ PREVIOUS SESSION
    # Get done category url list
    done_cate_file_path = os.path.join(TempPath, "done_cate.txt")
    done_cate_list = readTextFileToList(done_cate_file_path)


    # get current page
    current_page_file_path = os.path.join(TempPath, "current_page.txt")
    current_page = readTextFileToList(current_page_file_path)
    if current_page:
        current_page = int(current_page[0]) + 1
    else:
        current_page = 1

    # proxy_list = []
    # for row in proxies.split():
    #     if row:
    #         proxy_list.append(row.strip())
    
    # # start browser
    # browser = WebBrowser(timeout = 10, isDisableImage = True, isDisableJavascript = True, proxyIpList=proxy_list, changeProxyTotal=50)

    input_file_path = os.path.join(CurrentPath, "input.txt")
    browser = WebBrowser(timeout = 10, isDisableImage = True, isDisableJavascript = True, changeProxyTotal=50)
    # ====== STEP 1: GET ALL PROPERTIES URL FOR A CATEGORY =======
    logging.info("=============== STEP 1: COLLECT PROPERTIES URL =============== ")

    # cate links
    
    cate_links = readTextFileToList(input_file_path)

    # File path to save property url
    property_urls_file_path = os.path.join(TempPath, "property_urls.csv") # category | url
    total = len(cate_links)
    counter = 0
    for link in cate_links:
        counter += 1
        logging.info('Process %d/%d urls', counter, total)
        # Check if link done
        if link in done_cate_list:
            # logging.info("The category link is done: %s", link)
            logging.info('Done %d/%d urls', counter, total)
            continue

        while  True:
            
            url = link.format(12*(current_page-1))
            logging.info("Page %d at url: %s", current_page, url)
            # Get from current page
            result, is_next_page = getPropertyUrlFromPage(url)
            if result:
                # Write result to file
                writeDictToCSV(result, property_urls_file_path, 'a')
                # Save current page status
                writeListToTextFile([current_page], current_page_file_path, 'w')
                # Increase page
                current_page += 1
            
            if not result or not is_next_page:
                current_page = 1
                # Save current page status
                writeListToTextFile([current_page], current_page_file_path, 'w')
                # Save this link done
                writeListToTextFile([link], done_cate_file_path, 'a')
                # Finish this link
                break



    # ======= STEP 2: GO TO EACH URL TO GET PROPERTIES DETAIL ========
    logging.info("=============== STEP 2: COLLECT PROPERTIES DETAIL =============== ")

    # get done properties list
    done_pro_file_path = os.path.join(TempPath, "done_pro.txt")
    done_pro_list = readTextFileToList(done_pro_file_path)

    p_link_list = readCsvToListDict(property_urls_file_path) # category | url
    total = len(p_link_list)
    counter = 0
    for item in p_link_list:
        
        counter += 1
        logging.info('Process %d/%d properties', counter, total)
        if item['url'] in done_pro_list:
            #logging.info("The property link is done: %s", item['url'])
            logging.info('Done %d/%d properties', counter, total)
            continue
        result = getPropertyDetail(item['url'], item['category'])
        if result:
            header = [
                
                'url',
                'category',
                'gtitle',
                'image_url',
                #'flatform',
                'release_EU_UK',
                'release_US',
                'release_AU',
                'release_date',
                
                'm_intel_cpu',
                'm_amd_cpu',
                'm_nivdia_card',
                'm_amd_card',
                'm_vram',
                'm_ram',
                'm_os',
                'm_directx',
                'm_hdd',
                'm_gd',

                'r_intel_cpu',
                'r_amd_cpu',
                'r_nivdia_card',
                'r_amd_card',
                'r_vram',
                'r_ram',
                'r_os',
                'r_directx',
                'r_hdd',
                'r_gd',
                
                ]
            # Write result to file
            writeDictToCSV([result], ResultPath, 'a', header)

            # Save link done
            writeListToTextFile([item['url']], done_pro_file_path, 'a')
        else:
            logging.info("Fail or not to get: %s", item['url'])
        

    
    # ========= POST DONE ===========
    # Move result file to project directory
    if os.path.isfile(ResultPath):
        result_folder = os.path.join(CurrentPath, "result")
        createFolderIfNotExists(result_folder)
        final_result_file_path = os.path.join(result_folder, "result_at_" + getCurrentDateString("%Y%m%d_%H%M%S") + ".csv")
        shutil.move(ResultPath, final_result_file_path)
    # Rename temp folder
    if os.path.exists(TempPath):
        temp_done = os.path.join(CurrentPath, "temp_at_" + getCurrentDateString("%Y%m%d_%H%M%S"))
        shutil.move(TempPath, temp_done)
        #shutil.rmtree(TempPath)

    browser.exitDriver()


if __name__ == "__main__":
    main(sys.argv)
    logging.info("DONE !!! etuannv@gmail.com ;)")