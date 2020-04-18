# from selenium import webdriver
import pyttsx3
from datetime import date
from bus_automate import bus_auto


def exter_book_quick_play(_data):
    engine = pyttsx3.init()
    engine.say("Flow Initiated. plase don't stop this")
    engine.runAndWait()

    # book bus for me from Mumbai to Pune bus type ordinary on 23 next month
    if _data.__contains__("book") and _data.__contains__("bus"):
        # filter data (remove unwanted chars )
        bad_stm = ['/', '|', ';', '.', '!', '*', "'", ':', '?', '(', ')', '[', ']', '{', '}', '@', '#', "$", '%',
                    "&",
                    'and', 'is', ]
        for i in bad_stm:
            _data = _data.replace(i, '')
            # separate each word from another

        _data_arr = _data.split()
        print(_data_arr)
        if _data_arr.index('book') == 0 and _data_arr.index('bus') == 1:
            # url = "http://127.0.0.1/SmartRobot_web_UI/bus_book.php"
            # driver = webdriver.Chrome(
            # "C:\All Projects\Python Projects\Final Year Project\Chrome Driver\chromedriver.exe")
            # driver.get(url)
            # Destination data
            frm_idx = _data_arr.index('from')
            des_idx = frm_idx + 1
            des_city = _data_arr[des_idx]
            print(des_city)
            engine.say("Your Source city is " + des_city)
            engine.runAndWait()
            # driver.find_element_by_id('frm').send_keys(des_city)
            # Arrival city data
            to_idx = _data_arr.index('to')
            arr_idx = to_idx + 1
            arr_city = _data_arr[arr_idx]
            print(arr_city)
            engine.say("your Destination city is " + arr_city)
            engine.runAndWait()
            # driver.find_element_by_id('t_o').send_keys(arr_city)
            # Bus type
            bt_idx = _data_arr.index('type')
            b_type_idx = bt_idx + 1
            b_type = _data_arr[b_type_idx]
            print(b_type)
            engine.say("Your bus type is " + b_type)
            engine.runAndWait()
            # driver.find_element_by_id('b_type').send_keys(b_type)
            # get date
            dte_idx = _data_arr.index('on')
            dd_idx = dte_idx + 1
            dd = _data_arr[dd_idx]
            print(dd)
            # driver.find_element_by_id('dd').send_keys(dd)
            # for month
            mm_idx = dte_idx + 2
            mm = _data_arr[mm_idx]
            x = date.today()
            yyyy = x.strftime("%Y")
            # driver.find_element_by_id('yyyy').send_keys(yyyy)
            if mm == "next" or mm == "month":
                try:
                    mm = x.replace(month=x.month + 1).strftime("%B")
                    print(mm)
                except ValueError:
                    if x.month == 12:
                        mm = x.replace(year=x.year + 1, month=1)
                    else:
                        # next month is too short to have "same date"
                        raise
            else:
                mm
            # driver.find_element_by_id('mm').send_keys(mm)
            engine.say("Your traveling date is ")
            engine.say(dd)
            engine.say(mm)
            engine.say(yyyy)
            engine.runAndWait()
            print("Date is {}/{}/{} ".format(dd, mm, yyyy))
            engine.say('You want return ticket?')
            engine.runAndWait()
            _n_data = 'no'
            if _n_data == 'no' or _n_data == 'no no':
                _n_data = 0
                r_dd = 0
                r_mm = 0
                r_yyyy = 0
                # driver.find_element_by_id('noCheck').click()
            elif _n_data == 'yes':
                # driver.find_element_by_id('yesCheck').click()
                # this is for day return date
                print("Return date?")
                print("Day in date dd/mm/yyyy dd?")
                engine.say("On which day you like to book for return?")
                engine.say("Tell me day only!")
                engine.runAndWait()
                r_dd = "12"
                # driver.find_element_by_id('r_dd').send_keys(r_dd)
                # this is for return month
                print("Now tell me month only?")
                engine.say("Now tell me month?")
                engine.say("In which month ?")
                engine.runAndWait()
                r_mm = "in next month"
                if r_mm == "in next month" or r_mm == "Next month" or r_mm == "Next Month" or r_mm == "next Month":
                    try:
                        r_mm_ = x.replace(month=x.month + 1).strftime("%B")
                    except ValueError:
                        if x.month == 12:
                            r_mm_ = x.replace(year=x.year + 1, month=1)
                        else:
                            # next month is too short to have "same date"
                            raise
                else:
                    r_mm_ = x.strftime("%B")
                # driver.find_element_by_id('r_mm').send_keys(r_mm_)

                # this is for return date year
                engine.say("i will pick current year.")
                engine.runAndWait()
                r_yyyy = x.strftime("%Y")
                print("Return date is %d/%d/%d" % (r_dd, r_mm, r_yyyy))
                # driver.find_element_by_id('r_yyyy').send_keys(r_yyyy)

            # driver.find_element_by_id('sub').click()

            engine.say("Okay let me do some work, I have your data")
            engine.say("I will send ticket, to your mail")
            engine.runAndWait()
            var_list = [des_city, arr_city, b_type, dd, mm, yyyy, _n_data, r_dd, r_mm, r_yyyy]
            bus_auto(var_list)
        else:
            print("I can't book bus for you")
            engine.say("I can't book bus for you")
            engine.runAndWait()
    else:
        engine.say("Sorry I can't help you!")
        engine.runAndWait()

    Extract_query()
    # importing bus_auto function from bus_automation file