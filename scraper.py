from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import discord
import time
import os
TOKEN = os.environ["ACCESS_TOKEN"]
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
while True:
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    streets = []
    areas = []
    prices = []
    availables = []
    links = []
    images = []
    sent_reqs = []
    import_csv = pd.read_csv("save.csv")
    import_csv.head()
    with open("sent_req.txt", "r") as f:
        sent_request = f.readlines()
        for i in range(len(sent_request)):
            sent_request[i] = sent_request[i].strip()


    def sent(link):
        if link in sent_request:
            return "FALSE"
        return ""


    def ireland():
        driver.get('''https://www.daft.ie/sharing/dublin-2-dublin''')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(3, document.body.scrollHeight/3*2);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(3, document.body.scrollHeight);")
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        for a in soup.find('ul', attrs={'data-testid': 'results'}).findAll('li'):
            addr = a.find('p', attrs={'data-testid': 'address'}).text
            street = addr.split(',')[1]
            area = ' '.join(addr.split(',')[2:]).strip()
            available =  "Now"
            price = a.find('div', attrs={'data-testid': 'price'}).find('span').text
            link = '''https://www.daft.ie''' + \
                a.find("a")['href']
            imageR = a.find("picture").find('img')["src"]
            if imageR:
                image = imageR
            else:
                image = None
            streets.append(street)
            areas.append(area)
            availables.append(available)
            prices.append(price)
            images.append(image)
            links.append(link)
            sent_reqs.append(sent(link))


    def irelandRent():
        driver.get('''https://www.daft.ie/property-for-rent/dublin-2-dublin''')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(3, document.body.scrollHeight/3*2);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(3, document.body.scrollHeight);")
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        for a in soup.find('ul', attrs={'data-testid': 'results'}).findAll('li', attrs={'class': 'SearchPage__Result-gg133s-2'}):
            subUnits = a.find('div', attrs={'data-testid': 'sub-units-container'})
            if subUnits:
                addr = a.find('p', attrs={'data-testid': 'address'}).text
                street = addr.split(',')[0]
                area = ' '.join(addr.split(',')[1:]).strip()
                image = None
                available = "Now"
                for b in subUnits.findAll('li'):
                    link = '''https://www.daft.ie''' + \
                    b.find("a")['href']
                    price = b.find('p', attrs={'data-testid': 'sub-title'}).text
                    streets.append(street)
                    areas.append(area)
                    availables.append(available)
                    prices.append(price)
                    images.append(image)
                    links.append(link)
                    sent_reqs.append(sent(link))
            else:
                addr = a.find('p', attrs={'data-testid': 'address'}).text
                street = addr.split(',')[0]
                area = ' '.join(addr.split(',')[1:]).strip()
                available =  "Now"
                price = a.find('div', attrs={'data-testid': 'price'}).find('span').text
                link = '''https://www.daft.ie''' + \
                    a.find("a")['href']
                imageR = None
                if imageR:
                    image = imageR
                else:
                    image = None
                streets.append(street)
                areas.append(area)
                availables.append(available)
                prices.append(price)
                images.append(image)
                links.append(link)
                sent_reqs.append(sent(link))

    ireland()
    irelandRent()
    strings = []
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
            string = " Found: {5}\n{0}, {1}\n Price: {2}\n Available From: {3}\n{4}".format(*[v['Street'],v['Area'],v['Price'],v['Available'],v['Link'],v['Added']])
            strings.append(string)
    n_df = pd.DataFrame(n_df, columns=import_csv.columns.values.tolist()[1:])
    n_df.to_csv("save.csv")
    driver.close()
    if len(strings) > 0:
        client = discord.Client()
        @client.event
        async def on_ready():
            channel = client.get_channel(1009529852728197274)
            for j in strings:
                await channel.send(j)
            await client.close()
        client.run(TOKEN)
    time.sleep(300)