from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
import pyttsx3
import webbrowser
import nltk
from datetime import date, datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import json
# from quick_book_v1 import exter_book_quick_play

# Create your views here.
def home(request):
	count = User.objects.count()
	return render(request, 'home.html', {
		'count': count
		})

""" def write_user_data(data_info, f):
	def write_json(data, f):
		with open(f, 'w') as fa:
			json.dump(data, fa, indent=4)
	with open(f) as json_file:
		data = json.load(json_file)
		temp = data['user_data']
		y = {
			'f_name':data_info[0],
			'l_name':data_info[1],
			'gender':data_info[2],
			'email':data_info[3],
			'age': data_info[4],
			'phone_number':data_info[5],
		}
		temp.append(y)
	write_json(data) """
		

def user_form(request):
	if request.method == 'GET':
		username = os.getlogin()
		f = open(f'C:\\Users\\{username}\\Documents\\ user_info.txt', 'w')
		f_name = request.GET.get('f_name')
		f.write(f_name)
		l_name = request.GET.get('l_name')
		f.write('\n'+l_name)
		gender = request.GET.get('gender')
		f.write('\n'+gender)
		email = request.GET.get('email')
		f.write('\n'+email)
		age = request.GET.get('age')
		f.write('\n'+age)
		phone_number = request.GET.get('phone_number')
		f.write('\n'+phone_number)
		f.close()
		#write_user_data(data, 'C:\\Users\\'+username+'\\Documents\\ user_info.json')
		flag = 'Data Stored Successfully!'
	return render(request, 'success.html',{'flag': flag})
	

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = UserCreationForm()
	return render(request, 'registration/signup.html', {
		'form': form
		})

def get_cmd(request):
	if request.GET.get('cmd'):
		cmd = request.GET.get('cmd')
		if len(cmd) <= 0:
			error_msg = "Command is empty!"
			return render(request, "error.html", {'error_msg': error_msg})
		# webbrowser.open("https://www.redbus.in/")
		# result = exter_book_quick_play(cmd)
		# now do your work here and return the result to play.html
		# ------------Default Query is---------------
		# book bus for me from Mumbai to Pune on 23 next month at 13
		# ----------------------------------------------------S
		engine = pyttsx3.init()    # voice status updator
		tokenized = nltk.word_tokenize(cmd)
		if len(tokenized) < 6 :
			engine.say("Please check your command")
			engine.runAndWait()
			error_msg = cmd
			return render(request, 'play.html', {'error_msg': error_msg})
		query = [word for (word, pos) in nltk.pos_tag(tokenized) if(pos[:2] == 'NN' or pos[:2] == 'CD' or pos[:2] == 'JJ')]
		if query[0]+query[1] == 'bookbus': # if this is valid extract all data 
			source_city = query[2]
			des_city = query[3]
			# manage time 
			if query[5] != 'next':
				try:
					if len(query[6]) > 2:
						booking_time = query[6]
					else:
						booking_time = str(query[6] + ":00")
						engine.say("your booking time is "+ str(booking_time))
				except:
					engine.say('Booking time not recognized.')
					engine.say('This may encounter some errors')
					engine.runAndWait()
					booking_time = 0
			else:
				try:
					if len(query[7]) > 2:
						booking_time = query[7]
					else:
						booking_time = str(query[7]) + ":00"
						engine.say("your booking time is "+ str(booking_time))
				except:
					engine.say('Booking time not recognized')
					engine.say('This may encounter some errors')
					engine.runAndWait()
					booking_time = 0
			# time extraction successful
			dd = query[4]
			mm = query[5]
			x = date.today()
			yyyy = x.strftime("%Y")
			if mm == 'next':
				try:
					mm = x.replace(month=x.month + 1).strftime("%B")
				except:
					if x.month == 12:
						mm = x.replace(year=x.year + 1, month = 1)
						yyyy = x.replace(year=x.year + 1).strftime("%Y")
			else:
				None
			engine.say("Your Source City is "+source_city)
			engine.say(" your destination city is "+des_city)
			engine.say(" and date is" +dd+" "+mm+ " "+yyyy)
			engine.say("Relax and do your work.")
			engine.runAndWait()
			# extraction of data successful.
			# scrap data from webpages of given url
			driver = webdriver.Chrome("c:\Final Year Project\Chrome Driver\chromedriver.exe") # 83 version
			url = "https://redbus.in/"
			driver.get(url)
			driver.maximize_window()
			time.sleep(1)
			# place source city
			driver.find_element_by_id('src').send_keys(source_city)
			time.sleep(3)
			# place destination city
			driver.find_element_by_id('dest').send_keys(des_city)
			time.sleep(3)
			# select date on calender first you need to open cal so we just pass dummy value
			driver.find_element_by_id('onward_cal').send_keys('0')
			# define function which convert month to numeric value for next process
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
					return m[s]
				except:
					raise ValueError("Not a Month")
			c_mm = x.strftime("%B")
			# this is to define how many time robot need to click in next month button
			flag = month_to_number(mm) - month_to_number(c_mm)
			while flag > 0:
				try:
					driver.find_element_by_xpath("//div[@id='rb-calendar_onward_cal']/table/tbody/tr/td[@class='next']").click()
					flag -= 1
				except:
					raise "Please Provide valid month"
			# select date on calender
			driver.find_element_by_xpath("//div[@id='rb-calendar_onward_cal']/table/tbody/tr/td[text()=" + dd + "]").click()
			# now click on search button
			driver.find_element_by_xpath("//button[@id='search_btn']").click()
			time.sleep(10)
			try:
				driver.find_element_by_xpath("//div[text()='View Buses']").click()
			except:
				engine.say("their are no government buses available at the moment")
				engine.say("I will search for private buses")
				engine.runAndWait()
			# first we need to validate existance of buses if there is no bus available
			# redirect to error page
			try:
				val_err1 = driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div/h3")
				engine.say(val_err1.text)
				engine.runAndWait()
				error_msg = "No buses found! Please try to search for new Date or Time."
				return render(request, 'error.html', {'error_msg': error_msg})
			except:
				None
			# now we need to extract all data from website to suggest some good buses
			# to do this we need to extract current pageand then add this all data to csv file for management 
			# remove all redudent data and filter it to get good results
			content = driver.page_source
			soup = BeautifulSoup(content, 'html.parser')
			# use same info var for finding minimum at given time and for next process
			info = soup.find_all('div', attrs={'class': 'clearfix row-one'})
			name_ = []
			type_ = []
			price_ = []
			time_ = []

			for a in info:
				n = a.find('div', attrs={'class': 'travels lh-24 f-bold d-color'})
				name_.append(n.text)
				t = a.find('div', attrs={'class': 'bus-type f-12 m-top-16 l-color'})
				type_.append(t.text.lower())
				p = a.find('div', attrs={'class': 'seat-fare'})
				p_with_text = p.text
				p_without_text = [int(i) for i in p_with_text.split() if i.isdigit()]
				price_.append(p_without_text[0])
				tm = a.find('div', attrs={'class': 'dp-time f-19 d-color f-bold'})
				time_.append(tm.text)

			df = pd.DataFrame({'Travels Name': name_, 'Bus Type': type_, 'Price': price_, 'Time': time_})
			# data_file_path = os.path.dirname(os.path.realpath('./data/data_handling.csv'))
			df.to_csv('data_handling.csv', index=False, encoding='utf-8')
			# do not close browser use same for next process

			# making data frame from file
			data = pd.read_csv('data_handling.csv', delimiter=',')
			
			# replaceing black sapces with underscore sign '_'
			data.columns = [column.replace(" ", "_") for column in data.columns]

			# filter out all buses at given time and suggest a bus having lowest price
			bus_at_time = data[data['Time'] == booking_time]
			min_bus_at_time = bus_at_time[bus_at_time['Price'] == bus_at_time['Price'].min()]
			# filter out data according to time and bus type and price at once 
			# if bus is not present at given time then consider bus according to time
			# find the bus type at user time
			# given_bus_type_at_time = data[data['Bus_Type'].dropna().str.contains(b_type.lower())]
			# if len(given_bus_type_at_time) == 0:
			# 	engine.say("Bus type not found at given time")
			# 	engine.say("I will pick your bus by Time.")
			# 	engine.runAndWait()
			# 	result = min_bus_at_time
			# else:
			# 	min_given_bus_type_at_time = given_bus_type_at_time[given_bus_type_at_time["Price"] == given_bus_type_at_time["Price"].min()]
			# 	engine.say("Bus found at minimum cost")
			# 	engine.say("Now its time to book")
			# 	result = min_given_bus_type_at_time
			# consider minimum cost bus at given time
			if len(min_bus_at_time) == 0:
				engine.say("Bus not found now you have to do it by yourself")
				engine.say("You can give me new information for booking")
				engine.runAndWait()
				result = "Bus Not Found! Please try to search for new Date or Time."
				return render(request, 'error.html', {'error_msg': result})
			else:
				engine.say("Bus found at your time")
				engine.runAndWait()
				result = min_bus_at_time

			res = []
			for index, row in result.iterrows():
				res.append(row[0])
				res.append(row[1])
				res.append(row[2])
				res.append(row[3])
			engine.say("bus name is "+ res[0])
			engine.runAndWait()

			new_res = []
			for i in res:
				new_res.append(str(i).replace(" ",""))
			# now match our extracted information on website and do further process
			new_info = soup.find_all('div', attrs={'class': 'clearfix bus-item'})
			# make counter to select bus on web browser
			count = 0
			for a in new_info:
				count += 1
				n = a.find('div', attrs={'class': 'travels lh-24 f-bold d-color'})
				tm = a.find('div', attrs={'class': 'dp-time f-19 d-color f-bold'})
				if n.text.replace(" ","") == new_res[0] and tm.text == new_res[3]:
					break
			v = "/html/body/section/div[2]/div[1]/div/div[2]/div[2]/div[2]/ul/div["+ str(count) +"]/li/div/div[2]/div[1]"
			ele = driver.find_element_by_xpath(v)
			driver.execute_script("arguments[0].click();", ele) # help from stackoverflow
			time.sleep(3)
			engine.say("Please Select your seat you have 30 seconds.")
			engine.runAndWait()
			time.sleep(30)
			# their is only one way to verify and click on seats using Action Chain
			# which works with screen co-ordinates and that can be differ
			# if you dont have solution then use manual interface to select seat in 30 sec sleep all processes for 30 sec so user can select seat
			username = os.getlogin()
			openfile = open(f'C:\\Users\\{username}\\Documents\\ user_info.txt') # open file locally
			con = openfile.read()
			openfile.close()
			if len(con) != 0:   # check for content
				h_map = con.split('\n')
			else:
				engine.say("Please add profile Data")
				engine.runAndWait()
				error_msg = "Please add your Profile Data. Click on Your Name (Top Right Side) >> Add Profile Data."
				return render(request, 'error.html', {'error_msg': error_msg})
				
			# this will select boarding and destination automatically
			boarding_point = "//*[@class='modal-body oa-y']/ul/li/div[3]/span"
			driver.find_element_by_xpath(boarding_point).click()
			time.sleep(3)
			destination_point = "//*[@class='modal-body oa-y']/ul/li/div[3]/span"
			driver.find_element_by_xpath(destination_point).click()
			time.sleep(3)
			pro_book_btn = "//*[text()='Proceed to book']"
			driver.find_element_by_xpath(pro_book_btn).click()
			time.sleep(5)
			# now start filling out form
			name_add = "//*[@class='custinfo_label']/input[@placeholder='Name']"
			driver.find_element_by_xpath(name_add).send_keys(h_map[0]+ " " + h_map[1])
			age_add = "//*[@class='custinfo_label']/input[@placeholder='Age']"				
			driver.find_element_by_xpath(age_add).send_keys(h_map[4])
			male_add = "//*[@id='div_22_0']"
			female_add = "//*[@id='div_23_0']"
			if h_map[2] == "Male":
				driver.find_element_by_xpath(male_add).click()
			else:
				driver.find_element_by_xpath(female_add).click()
			email_add = "//*[@class='custinfo_label']/input[@placeholder='Email ID']"
			driver.find_element_by_xpath(email_add).send_keys(h_map[3])
			phone_add = "//*[@class='custinfo_label']/input[@placeholder='Phone']"
			driver.find_element_by_xpath(phone_add).send_keys(h_map[5])
			# end form now click on pay button
			pay_btn_add = "//*[@value='Proceed to pay']"
			driver.find_element_by_xpath(pay_btn_add).click()
			engine.say("Make payment Manually. You will get your ticket to your Mail and Whatsapp")
			engine.runAndWait()
		else:
			engine.say("Please check your command!")
			engine.runAndWait()
			error_msg = cmd
			return render(request, 'play.html', {'error_msg': error_msg})
		#scrap_data = [['Testing Name','Testing','312','12:00'],['dummy','dum','123','1:00']] ##### test case 1
		return render(request, 'play.html', {'res_name':res[0], 'res_type':res[1],'res_price': res[2],'res_time':res[3]})


@login_required
def secret_page(request):
	return render(request, 'secret_page.html')

@login_required
def user_data(request):
	return render(request, 'user_form.html')

@login_required
def play(request):
	return render(request, 'play.html')

def how_work(request):
	return render(request, 'how_work.html')

