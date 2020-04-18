from queue import Empty
from selenium import webdriver
from datetime import date
from bs4 import BeautifulSoup
import pandas as pd
import pyttsx3


def bus_auto(x_var):
    engine = pyttsx3.init()
    import time
    driver = webdriver.Chrome("C:\Final Year Project\Chrome Driver\chromedriver.exe")
    driver.maximize_window()
    url = "https://www.redbus.in/"
    driver.get(url)
    time.sleep(1)
    # retrieve data from user data file
    driver.find_element_by_id('src').send_keys(x_var[0])
    time.sleep(3)
    driver.find_element_by_id('dest').send_keys(x_var[1])
    time.sleep(3)
    driver.find_element_by_id('onward_cal').send_keys('0')

    def month_to_number(string):
        m = {
            'jan': 1,
            'feb': 2,
            'mar': 3,
            'apr': 4,
            'may': 5,
            'jun': 6,
            'jul': 7,
            'aug': 8,
            'sep': 9,
            'oct': 10,
            'nov': 11,
            'dec': 12
        }
        s = string.strip()[:3].lower()

        try:
            out = m[s]
            return out
        except:
            raise ValueError('Not a month')

    x = date.today()
    u_mm = x_var[4]
    mm = x.strftime("%B")
    _u_mm = month_to_number(u_mm)
    _mm = month_to_number(mm)
    dd = x_var[3]
    flag = _u_mm - _mm
    r_dd = x_var[7]
    r_mm = x_var[8]
    r_yyyy = x_var[9]

    while flag > 0:
        try:
            d = driver.find_element_by_xpath(
                "//div[@id='rb-calendar_onward_cal']/table/tbody/tr/td[@class='next']").click()
            flag -= 1
        except:
            raise Empty("Please provide valid month")

    driver.find_element_by_xpath("//div[@id='rb-calendar_onward_cal']/table/tbody/tr/td[text()=" + dd + "]").click()
    driver.find_element_by_xpath("//button[@id='search_btn']").click()
    time.sleep(10)
    p = driver.find_element_by_xpath("//div[text()='View Buses']")
    if p:
        p.click()
    else:
        p = 0

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    info = soup.find_all('div', attrs={'class': 'clearfix row-one'})
    print(len(info))
    name_ = []
    tpe_ = []
    price_ = []
    time_ = []
    for a in info:
        name = a.find('div', attrs={'class': 'travels lh-24 f-bold d-color'})
        name_.append(name.text)
        tpe = a.find('div', attrs={'class': 'bus-type f-12 m-top-16 l-color'})
        tpe_.append(tpe.text)
        price = a.find('div', attrs={'class': 'seat-fare'})
        price_with_text = price.text
        price_without_text = res = [int(i) for i in price_with_text.split() if i.isdigit()]
        price_.append(price_without_text[0])
        time = a.find('div', attrs={'class': 'dp-time f-19 d-color f-bold'})
        time_.append(time.text)

    df = pd.DataFrame({'Travels Name': name_, 'Bus Type': tpe_, 'Price': price_, 'Time': time_})
    df.to_csv('products.csv', index=False, encoding='utf-8')

    driver.close()

    csv_data = pd.read_csv('products.csv')
    all_ele = []
    for row in csv_data.index:
        all_ele.append(csv_data['Price'][row])

    all_ele_len = len(all_ele)
    average_price = sum(all_ele) / all_ele_len
    print(average_price)

    engine.say("Now tell me, Which type of Bus you like to book?")
    engine.say("We have some types, and these are: R T C means Government buses, Shivshahi buses, Shivneri buses, "
               "Private buses, or you can book sleeper bus ")
    engine.runAndWait()
    b_type = "shivshahi"
    engine.say("at what time you like to book")
    engine.runAndWait()
    booking_time = Recognize_voice() # this is not valid 
    bad_stm = ['at', 'on', 'in']
    for i in bad_stm:
        booking_time = booking_time.replace(i, '')

    # making data frame from csv file
    data = pd.read_csv("products.csv", delimiter=',')

    # replacing blank spaces with '_'
    data.columns = [column.replace(" ", "_") for column in data.columns]

    def closest(lst, K):
        return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]

    # time filter

    # find actual price from average price
    K = average_price
    actual_price_close_to_avg_price = closest(all_ele, K)
    print(actual_price_close_to_avg_price)

    if 'shivshahi bus' in b_type or 'shivshahi buses' in b_type or 'shivshahi' in b_type:
        # filtering with query method for Shivshahi buses
        # data.query('Bus_Type == "SHIVSHAHI"', inplace=True)

        ele_having_shivshahi = data[data.Bus_Type == 'SHIVSHAHI']
        minValue = ele_having_shivshahi['Price'].min()
        time_of_that_bus = ele_having_shivshahi.loc[ele_having_shivshahi['Price'] == minValue, 'Time'].iloc[0]
        print(ele_having_shivshahi)
        print(minValue)
        print(time_of_that_bus)
        engine.say("I found one bus for you at lowest price, at " + str(minValue))
        engine.say("and Bus time is " + str(time_of_that_bus))
        engine.runAndWait()
        bus_name_at_user_time = ele_having_shivshahi.loc[ele_having_shivshahi['Time'] == booking_time, 'Travels_Name'].iloc[0]
        print(bus_name_at_user_time)