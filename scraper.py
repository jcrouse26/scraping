from bs4 import BeautifulSoup
import requests
import csv

# with open('file:///Users/jasoncrouse/Downloads/view-source_juniorgolfscoreboard.com_TournySearch.asp.html') as html_file:
with open('tournaments_2019.html') as html_file:
	soup = BeautifulSoup(html_file, 'lxml')

table = soup.find('table')

search_results= table.find_all('tr')

csv_file = open('jgs_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)

csv_writer.writerow(['name', 'course', 'city', 'state', 'province', 'country', 'date', 'entry_fee', 'entry_deadline', 'b/g', 'age min', 'age_max', 'size', 'selection_criteria', 'contact info', 'website'])

course = ''
city = ''
state = ''
country = ''
province = ''
date = ''
entry_fee = ''
entry_deadline = ''
gender = ''
age = ''
age_min = ''
age_max = ''
size = ''
selection_criteria = ''
contact_info = ''
website = ''


i = 0

for item in search_results:
	# i = i + 1
	# if i > 6:
	# 	break
	obj = item.find_all('td')[0]
	
	try:
		TID = obj.find('input')['value']
		tourney_more_info_link = 'http://juniorgolfscoreboard.com/TournyInfo.asp?TID=' + TID
		source = requests.get(tourney_more_info_link).text
		soup = BeautifulSoup(source, 'lxml')

		info_table = soup.find('table')
		tourney_name = info_table.find('h3').text
		info_table = info_table.find_all('tr')

		print TID

		if "Province" in info_table[4].text:
			course = info_table[2].text.split("\n")[2]
			city_state = info_table[3].text.split("\n")[2]
			city = city_state.split(',')[0]
			state = city_state.split(',')[1]
			province = info_table[4].text.split("\n")[2].strip()
			country = info_table[5].text.split("\n")[3].strip()
			date = info_table[6].text.split("\n")[3].strip()
			entry_fee = info_table[7].text.split("\n")[4].strip()
			entry_deadline = info_table[8].text.split("\n")[2]
			if "B/G" in info_table[9].text:
				gender = info_table[9].text.split('\n')[4].strip()
				age = info_table[9].text.split('\n')[6].split('Size:')[0].strip()
				size = info_table[9].text.split('\n')[6].split('Size:')[1]
			else:
				gender = info_table[9].text.split('\n')[3].strip().split(' ')[0]
				age = info_table[9].text.split(":")[2].split('Size')[0].strip()
				size = info_table[9].text.split(':')[3].strip()
			age_min = age.split('-')[0]
			age_max = age.split('-')[1]
			size = info_table[9].text.split("\n")[6].split('Size:')[1].strip()
			selection_criteria = info_table[10].text.split("\n")[2]

			rows = [tourney_name, course, city, state, province, country, date, entry_fee, entry_deadline, gender, age_min, age_max, size, selection_criteria]
			print rows
			csv_writer.writerow(rows)
		else:
			print "Does not have Province"
			course = info_table[2].text.split("\n")[2]
			city_state = info_table[3].text.split("\n")[2]
			city = city_state.split(',')[0]
			state = city_state.split(',')[1]
			country = info_table[4].text.split('\n')[3].strip()
			date = info_table[5].text.split("\n")[3].strip()
			entry_fee = info_table[6].text.split('\n')[4].strip()
			entry_deadline = info_table[7].text.split("\n")[2]

			if "B/G" in info_table[8].text:
				gender = info_table[8].text.split('\n')[4].strip()
				age = info_table[8].text.split('\n')[6].split('Size:')[0].strip()
				size = info_table[8].text.split('\n')[6].split('Size:')[1]
			else:
				gender = info_table[8].text.split('\n')[3].strip().split(' ')[0]
				age = info_table[8].text.split(":")[2].split('Size')[0].strip()
				size = info_table[8].text.split(':')[3].strip()

			age_min = age.split('-')[0]
			age_max = age.split('-')[1]

			selection_criteria = info_table[9].text.split("\n")[2]
			contact_info = info_table[10].text.split('\n')[2]
			website = info_table[11].find('a')['href']

			rows = [tourney_name, course, city, state, '', country, date, entry_fee, entry_deadline, gender, age_min, age_max, size, selection_criteria, contact_info, website]
			print rows
			csv_writer.writerow(rows)
	except:
		print "error"
		pass

csv_file.close()