import requests
from bs4 import BeautifulSoup
import pandas as pd


def urls(link):
    r = requests.get(link)
    html_content = r.content
    soup = BeautifulSoup(html_content, 'html.parser')
    all_links = soup.select(".num")[3]
    last_page = all_links.get_text()
    return int(last_page)


def start(url_links):
    r = requests.get(url_links)
    html_content = r.content
    soup = BeautifulSoup(html_content, 'html.parser')
    hotel_links = soup.select('.namelink')
    lst = []
    for link in hotel_links:
        links = "https://www.businesstravelnews.com"+link.get('href')
        lst.append(links)
    return lst


def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email


def get_data(lst):
    email_lst = []
    name_lst = []
    for urls in lst:
        r = requests.get(urls)
        html_content = r.content
        soup = BeautifulSoup(html_content, 'html.parser')
        hotel_name = soup.select(".h1")
        hotel_email = soup.select(".left")
        for email in hotel_email:
            email = cfDecodeEmail(email.a.span['data-cfemail'])
            email_lst.append(email)
        for text in hotel_name:
            hotel_name = text.get_text()
            hotel_name = hotel_name.translate(str.maketrans("\n\t\r", "   "))
            name_lst.append(hotel_name)

    data = pd.DataFrame(list(zip(name_lst,email_lst)), columns=["NAME", "EMAIL"])
    data.to_csv("sample_data.csv")
    print("Data Exported Successfully")



if __name__ == '__main__':
    last_page = urls("https://www.businesstravelnews.com/Hotels/Rome")
    inp = int(input("how many page u want to scrape\n Total Pages: "+str(last_page)+"\n"))
    y = 1
    lst = []
    while y <= inp:
        full_link = "https://www.businesstravelnews.com/Hotels/Rome?pg="+str(y)
        lst.append(full_link)
        y = y + 1
    lst3 = []
    for data in lst:
        lst1 = start(data)
        lst3.extend(lst1)
    get_data(lst3)



