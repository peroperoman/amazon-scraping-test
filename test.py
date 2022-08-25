import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.select import Select

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(
    executable_path='/Users/ireba-pc/webdriver/chromedriver',
    options=options)

driver.get('https://www.amazon.co.jp/')
driver.implicitly_wait(10)
sleep(1)

driver.find_element_by_id('nav-search-dropdown-card').click()
select_category = Select(driver.find_element_by_id('searchDropdownBox'))
select_category.select_by_value('search-alias=stripbooks')

driver.find_element_by_css_selector('div.nav-search-field > input').send_keys('ボクシング 井上尚弥')
driver.find_element_by_css_selector('div.nav-right > div > span > input').click()

a_tags = driver.find_elements_by_css_selector('ul.a-pagination > li.a-selected > a')
a_tags += driver.find_elements_by_css_selector('ul.a-pagination > li.a-normal > a')
page_links = [a_tag.get_attribute('href') for a_tag in a_tags]

book_list = []
for page_link in page_links:
    driver.get(page_link)
    sleep(1)
    source = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(source, 'lxml')
    product_soup = soup.select('div.a-section.a-spacing-medium')

    for i in range(len(product_soup) - 1):
        miso_soup = product_soup[i]
        title = miso_soup.find('span', class_='a-size-medium a-color-base a-text-normal').text
        tmp_price = miso_soup.find('span', class_='a-price-whole')
        price = tmp_price.text if tmp_price else None
        tmp_review_avg = miso_soup.find('span', class_='a-icon-alt')
        review_avg = tmp_review_avg.text if tmp_review_avg else None
        tmp_review_num = miso_soup.select_one('div.a-row.a-size-small > span:nth-of-type(2) > a > span')
        review_num = tmp_review_num.text if tmp_review_num else None

        book_list.append({
            'title': title,
            'price': price,
            'review_avg': review_avg,
            'review_num': review_num
        })

driver.quit()

df = pd.DataFrame(book_list)
df.index = df.index + 1
df.to_csv('inoue-sama-books.csv', encoding='utf-8-sig')
