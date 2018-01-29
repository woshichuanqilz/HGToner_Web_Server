# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
def get_Exchange ():
    driver = webdriver.PhantomJS()
    driver.get('http://finance.sina.com.cn/money/forex/hq/USDCNY.shtml')
    usdexchange = WebDriverWait(driver, 60).until(lambda driver : driver.find_element_by_xpath('//*[@id="quoteWrap"]')).text.split()[0]
    driver.close()
    driver.quit()
    return usdexchange

def get_TONER_NEWS():
    url = 'https://www.rtmworld.com/2d/cn/news-rtm/'
    xpath = '/html/body/div[2]/div[6]/div/div[1]/div[2]/div/ul/li'
    driver = webdriver.PhantomJS()
    driver.get(url)
    link_dict = {}
    for idx, p_ele in enumerate(driver.find_elements_by_xpath(xpath)):
        brief = p_ele.find_element_by_xpath('div[2]/span').text
        link  = p_ele.find_element_by_xpath('div[3]/div/a').get_attribute('href')
        link_dict[brief] = link
    driver.close()
    driver.quit()

    html = ''
    for key, value in link_dict.items():
        res = "<a href=\"" + value + "\">" + key + "</a>"
        html = html + "<br />" + res + "<br />"
    html = '<html>\n<body>\n<h1>耗材行业动态</h1>' + html + '</body>\n</html>'
    with open('TONER_NEWS.html', 'a') as the_file:
       the_file.write(html)

    return link_dict

if __name__ == '__main__':
    print(get_Exchange())
