from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import pyttsx3
import webbrowser
import nltk
from datetime import date
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
# from quick_book_v1 import exter_book_quick_play

# Create your views here.
def home(request):
	count = User.objects.count()
	return render(request, 'home.html', {
		'count': count
		})


def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = UserCreationForm()
	return render(request, 'registration/signup.html', {
		'form': form
		})

def get_cmd(request):
	if request.GET.get('cmd'):
		cmd = request.GET.get('cmd')
		# webbrowser.open("https://www.redbus.in/")
		# result = exter_book_quick_play(cmd)
		# now do your work here and return the result to play.html
		# ------------Default Query is---------------
		# book bus for me from Mumbai to Pune bus type ordinary on 23 next month
		tokenized = nltk.word_tokenize(cmd)
		query = [word for (word, pos) in nltk.pos_tag(tokenized) if(pos[:2] == 'NN' or pos[:2] == 'CD' or pos[:2] == 'JJ')]
		if query[0]+query[1] == 'bookbus': # if this is valid extract all data 
			source_city = query[2]
			des_city = query[3]
			bus_type = query[6]
			try:
				booking_time = query[9]
				time_am_or_pm = query[10]
			except:
				None

			dd = query[7]
			mm = query[8]
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
				mm
			engine = pyttsx3.init()
			engine.say("Your Source City is "+source_city)
			engine.say(" your destination city is "+des_city)
			engine.say(" your bus type is "+bus_type)
			engine.say(" and date is" +dd+" "+mm+ " "+yyyy)
			engine.runAndWait()
			# scrap data from webpages of given url
			driver = webdriver.Chrome("c:\Final Year Project\Chrome Driver\chromedriver.exe")
			driver.maximize_window()
			url = "https://redbus.in/"
			driver.get(url)
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
				None
			# now we need to extract all data from website to suggest some good buses
			# to do this we need to extract current pageand then add this all data to csv file for management 
			# remove all redudent data and filter it to get good results
			content = driver.page_source
			soup = BeautifulSoup(content, 'html.parser')
			info = soup.find_all('div', attrs={'class': 'clearfix row-one'})
			name_ = []
			type_ = []
			price_ = []
			time_ = []

			for a in info:
				n = a.find('div', attrs={'class': 'travels lh-24 f-bold d-color'})
				name_.append(n.text)
				t = a.find('div', attrs={'class': 'bus-type f-12 m-top-16 l-color'}) 
				type_.append(t.text)
				p = a.find('div', attrs={'class': 'seat-fare'})
				p_with_text = p.text
				p_without_text = [int(i) for i in p_with_text.split() if i.isdigit()]
				price_.append(p_without_text[0])
				tm = a.find('div', attrs={'class': 'dp-time f-19 d-color f-bold'})
				time_.append(tm.text)

			df = pd.DataFrame({'Travels Name': name_, 'Bus Type': type_, 'Price': price_, 'Time': time_})
			# data_file_path = os.path.dirname(os.path.realpath('./data/data_handling.csv'))
			df.to_csv('data_handling.csv', index=False, encoding='utf-8')
			driver.close()

			# finding the average price of all buses to give good results 
			csv_data = pd.read_csv('data_handling.csv')
			all_ele = []
			for row in csv_data.index:
				all_ele.append(csv_data['Price'][row])

			average_price =(sum(all_ele)//len(all_ele)) 


		scrap_data = [['Testing Name','Testing','312','12:00'],['dummy','dum','123','1:00']]
		return render(request, 'play.html', {'result':average_price,'scrap_data':scrap_data})

@login_required
def secret_page(request):
	return render(request, 'secret_page.html')

@login_required
def play(request):
	engine = pyttsx3.init()
	engine.say("You Just Started the flow")
	engine.runAndWait()
	return render(request, 'play.html')

def how_work(request):
	return render(request, 'how_work.html')
