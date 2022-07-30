from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
while True:
    driver = webdriver.Edge("C:\\Users\\Fin\\Desktop\\web_scrapper\\edgedriver_win64\\msedgedriver.exe")
    # import os
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    streets = []
    areas = []
    prices = []
    availables = []
    links = []
    images = []
    sent_reqs = []
    import_csv = pd.read_csv("public/save.csv")
    import_csv.head()
    with open("public/sent_req.txt", "r") as f:
        sent_request = f.readlines()
        for i in range(len(sent_request)):
            sent_request[i] = sent_request[i].strip()


    def sent(link):
        if link in sent_request:
            return "FALSE"
        return ""


    def djAlex():
        driver.get('''https://djalexander.co.uk/properties/?filter_search_
        type=to-let&filter_region=glasgow&filter_bedrooms_328=1-2&filter_filterprice_4960=95-900''')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(3, document.body.scrollHeight/3*2);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(3, document.body.scrollHeight);")
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        for a in soup.findAll('div', attrs={'class': 'w-grid-item-h'}):
            street = a.find('h3', attrs={'class': 'usg_post_custom_field_1'}).find(
                'span', attrs={'class': 'w-post-elm-value'}).text
            area = a.find('h3', attrs={'class': 'usg_post_custom_field_8'}).find(
                'span', attrs={'class': 'w-post-elm-value'}).text
            available = a.find('h6', attrs={'class': 'available_from'}).find(
                'span', attrs={'class': 'w-post-elm-value'}).text
            price = a.find('h2', attrs={'class': 'tag-property-price'}).find('span', attrs={'class': 'w-post-elm-value'}).text
            link = a.find('a')['href']
            image =a.find('img', attrs={'class': 'attachment-us_600_400'})['src']
            streets.append(street)
            areas.append(area)
            availables.append(available)
            prices.append(price)
            images.append(image)
            links.append(link)
            sent_reqs.append(sent(link))


    def rightMove():
        driver.get('''https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22av%7BsIr%7D%60YeqA%7CDaTal%40Ict%40Hcm%40zBmj%40bJcOnPq%40rHdBrKbHvJbHzU~MzUfXlJxRaAxv%40%7DEhh%40mJzS%22%7D&maxBedrooms=2&minBedrooms=1&maxPrice=800&sortType=2&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords=''')
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        for a in soup.findAll('div', attrs={'class': 'l-searchResult'}):
            addr = a.find('address', attrs={'class': 'propertyCard-address'}).text
            street = addr.split(',')[0]
            area = ' '.join(addr.split(',')[1:])
            available = a.find(
                'span', attrs={'class': 'propertyCard-branchSummary-addedOrReduced'}).text
            price = a.find('span', attrs={'class': 'propertyCard-priceValue'}).text
            link = '''https://www.rightmove.co.uk''' + \
                a.find('a', attrs={'class': 'propertyCard-priceLink'})['href']
            image = a.find('div', attrs={'class': 'propertyCard-img'}).find('img')['src']
            streets.append(street)
            areas.append(area)
            availables.append(available)
            prices.append(price)
            images.append(image)
            links.append(link)
            sent_reqs.append(sent(link))


    def zoopla():
        driver.get('''https://www.zoopla.co.uk/to-rent/property/glasgow/?beds_min=1&price_frequency=per_month&price_max=800&q=Glasgow&results_sort=newest_listings&search_source=to-rent&radius=0&hidePoly=false&polyenc=un~sIpbaYwM%7D%5By%40aVzRwwBbJwXrN_GjlAvn%40%7CH%60VaA%60e%40yVxtAiyAlL''')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(3, document.body.scrollHeight/4*2);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(3, document.body.scrollHeight/4*3);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(3, document.body.scrollHeight);")
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        for a in soup.findAll('div', attrs={'data-testid': 'search-result'}):
            addr = a.find('p', attrs={'data-testid': 'listing-description'}).text
            street = addr.split(',')[0]
            area = ' '.join(addr.split(',')[1:])
            available = a.find(
                'span', attrs={'data-testid': 'available-from-date'}).text
            price = a.find(
                'div', attrs={'data-testid': 'listing-price'}).find('p').text
            link = '''https://www.zoopla.co.uk''' + \
                a.find('a', attrs={'data-testid': 'listing-details-link'})['href']
            image = a.findAll('img')[0]['src']
            streets.append(street)
            areas.append(area)
            availables.append(available)
            prices.append(price)
            images.append(image)
            links.append(link)
            sent_reqs.append(sent(link))


    def onTheMarket():
        driver.get('''https://www.onthemarket.com/to-rent/property/glasgow-city/?max-bedrooms=2&max-price=800&polygons0=aa~sIbr%60YjC_rAlDkn%40vR_%5B%7Cb%40_Ux%5Bb%7B%40uSzjC''')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(3, document.body.scrollHeight/4*2);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(3, document.body.scrollHeight/4*3);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(3, document.body.scrollHeight);")
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        for a in soup.findAll('li', attrs={'class': 'otm-PropertyCard'}):
            addr = a.find('span', attrs={'class': 'address'}).text
            street = addr.split(',')[0]
            area = ' '.join(addr.split(',')[1:])
            available = "No Info"
            price = a.find('div', attrs={'class': 'otm-Price'}).text
            link = '''https://www.onthemarket.com''' + \
                a.find('div', attrs={'class': 'otm-PropertyCardMedia'}).find('a')['href']
            imageR = a.find(
                'div', attrs={'class': 'swiper-slide swiper-slide-active'})
            if imageR:
                image = imageR.find('img')['src']
            else:
                image = None
            streets.append(street)
            areas.append(area)
            availables.append(available)
            prices.append(price)
            images.append(image)
            links.append(link)
            sent_reqs.append(sent(link))

    def openRent():
        driver.get('''https://www.openrent.co.uk/properties-to-rent/glasgow-city?term=Glasgow%20City&area=2&prices_min=594&prices_max=854''')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(3, document.body.scrollHeight/3*2);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(3, document.body.scrollHeight);")
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        for a in soup.find('div', attrs={'class': 'property-list'}).findAll('a', attrs={'class': 'pli'}):
            addr = a.find('span', attrs={'class': 'listing-title'}).text
            street = ' '.join(addr.split(',')[1:])
            area = addr.split(',')[0]
            available =  "Now"
            price = a.find('div', attrs={'class': 'pl-title'}).find('h2').text
            if 'Let' in price:
                continue
            link = '''https://www.openrent.co.uk''' + \
                a['href']
            imageR = a.find(
                'img', attrs={'class': 'propertyPic'})
            if imageR:
                image = "https:" + imageR['src']
            else:
                image = None
            streets.append(street)
            areas.append(area)
            availables.append(available)
            prices.append(price)
            images.append(image)
            links.append(link)
            sent_reqs.append(sent(link))

    djAlex()
    rightMove()
    zoopla()
    onTheMarket()
    openRent()
    times = [time.strftime("%H:%M %Y/%m/%d")] * len(availables)
    df = pd.DataFrame({"Req": sent_reqs, "Street": streets, "Area": areas, "Price": prices, "Available": availables, "Link": links, "Added":  times, "Image": images})
    n_df = []
    for l, v in df.iterrows():
        if v["Link"] in import_csv.values:
            val = import_csv.loc[import_csv['Link'] == v["Link"]].values.tolist()[0][1:]
            old_date = datetime.strptime(val[6], "%H:%M %Y/%m/%d")
            current = datetime.now()
            if (current - old_date).seconds > 14400 or (current - old_date).days != 0:
                val[0] = ""
            else:
                val[0] = "TRUE"
            n_df.append(val)
        else:
            v["Req"] = "TRUE"
            n_df.append(v.values.tolist())
    n_df = pd.DataFrame(n_df, columns=import_csv.columns.values.tolist()[1:])

    with open('out.html', 'w') as fo:
        fo.write(n_df.to_html(render_links=True, escape=False))
    n_df.to_csv("public/save.csv")
    driver.close()
    driver.quit()
    time.sleep(600)