import requests
from bs4 import BeautifulSoup
import csv
import time

def GDP_Average(IMF, WB, UN):
    IMF_int = int(IMF)
    WB_int = int(WB)
    UN_int = int(UN)
    average = round((IMF_int + WB_int + UN_int) / 3)
    return str(average)
    
start_time_global = time.time()

# URL of the Wikipedia pages
start_time = time.time()
url_fertility = "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependencies_by_total_fertility_rate"
url_education_index = "https://rankedex.com/society-rankings/education-index"
url_GDP = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita"
url_population = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
url_working_age_population = "https://en.wikipedia.org/wiki/List_of_countries_by_age_structure"
url_sex_ratio = "https://en.wikipedia.org/wiki/List_of_sovereign_states_by_sex_ratio"
url_emergency_contraception = "https://en.wikipedia.org/wiki/Emergency_contraceptive_availability_by_country"
url_time = time.time() - start_time
print("URL time : ", url_time)

# Send a GET request to the URLs and get the responses
start_time = time.time()
response_fertility = requests.get(url_fertility)
response_education_index = requests.get(url_education_index)
response_GDP = requests.get(url_GDP)
response_population = requests.get(url_population)
response_working_age_population = requests.get(url_working_age_population)
response_sex_ratio = requests.get(url_sex_ratio)
response_emergency_contraception = requests.get(url_emergency_contraception)
response_time = time.time() - start_time
print("RESPONSE time : ", response_time)

# Retrieve the contents
start_time = time.time()
content_fertility = response_fertility.content
content_education_index = response_education_index.content
content_GDP = response_GDP.content
content_population = response_population.content
content_working_age_population = response_working_age_population.content
content_sex_ratio = response_sex_ratio.content
content_emergency_contraception = response_emergency_contraception.content
content_time = time.time() - start_time
print("CONTENT time : ", content_time)

# Parse the HTML contents using BeautifulSoup
start_time = time.time()
soup_fertility = BeautifulSoup(content_fertility, 'html.parser')
soup_education_index = BeautifulSoup(content_education_index, 'html.parser')
soup_GDP = BeautifulSoup(content_GDP, 'html.parser')
soup_population = BeautifulSoup(content_population, 'html.parser')
soup_working_age_population = BeautifulSoup(content_working_age_population, 'html.parser')
soup_sex_ratio = BeautifulSoup(content_sex_ratio, 'html.parser')
soup_emergency_contraception = BeautifulSoup(content_emergency_contraception, 'html.parser')
soup_time = time.time() - start_time
print("SOUP time : ", soup_time)

# Find the tables with class containing the data
start_time = time.time()
table_fertility = soup_fertility.find('table', {'class': 'wikitable sortable'}) 
table_education_index = soup_education_index.find('table')
table_population = soup_population.find_all('tr', {'class': ''})
table_GDP = soup_GDP.find_all('tr', {'class': ''})
table_working_age_population = soup_working_age_population.find_all('tr', {'class': ''})
table_sex_ratio = soup_sex_ratio.find_all('tr', {'class': ''})
table_emergency_contraception = soup_emergency_contraception.find_all('tr', {'class': ''})
table_time = time.time() - start_time
print("TABLE time : ", table_time)

# Extract the data from the table rows
start_time = time.time()
# # For Fertility
rows_fertility = table_fertility.find_all('tr')
country_fertility_list = []

# # Loop through the rows and extract country name and fertility rate
for row in rows_fertility[1:]:
    cells = row.find_all('td')
    if len(cells) >= 2:
        country = cells[1].text.strip()
        fertility_rate = cells[2].text.strip()
        if (fertility_rate != "-") and (fertility_rate != ""):
        	country_fertility_list.append([country, fertility_rate])
        	
# # For Education Index
country_education_index_list = []
rows_education_index = table_education_index.find_all('tr')
for row in rows_education_index:
    columns = row.find_all('td')
    if len(columns) >= 2:
        country_name = columns[0].text.strip()
        education_index = columns[2].text.strip()
        country_education_index_list.append([country_name, education_index])

# # For GDP
country_GDP_list = []
for row in table_GDP:
    cells = row.find_all('td')
    if len(cells) > 0:
        country_name = cells[0].text.strip()
        if len(cells) > 7:
            GDP_IMF = cells[2].text.strip().replace(',','')
            GDP_WB = cells[4].text.strip().replace(',','')
            GDP_UN = cells[6].text.strip().replace(',','')
            Avg = GDP_Average(GDP_IMF, GDP_WB, GDP_UN)
            country_GDP_list.append([country_name, GDP_IMF, GDP_WB, GDP_UN, Avg])
            
# # For Population by country
country_population_list = []
for row in table_population:
    cells = row.find_all('td')
    if len(cells) > 2:
        country_name = cells[0].text.strip()
        population = cells[1].text.strip().replace(',','')
        country_population_list.append([country_name, population])

# # For Working Age Population
working_age_population_list = []
for row in table_working_age_population:
    cells = row.find_all('td')
    if len(cells) > 2:
        country_name = cells[0].text.strip()
        working_age_population = cells[2].text.strip().replace("%", "")
        working_age_population_list.append([country_name, working_age_population])
        

# # For Sex Ratio
sex_ratio_list = []
for row in table_sex_ratio:
    cells = row.find_all('td')
    if len(cells) > 4:
        country_name = cells[0].text.strip().split(",")[0]
        sex_ratio_15to24 = cells[3].text.strip()
        sex_ratio_25to54 = cells[4].text.strip()
        if sex_ratio_15to24 != '--' or sex_ratio_25to54 != '--':
            sex_ratio_list.append([country_name, sex_ratio_15to24, sex_ratio_25to54])
            
# # For Emergency Contraception availibility (OTC):
emegency_contraception_OTC_list = []
for row in table_emergency_contraception:
    cells = row.find_all('td')
    if len(cells) > 4:
        country_name = cells[0].text.strip()
        if country_name == 'United States of America':
            country_name = 'United States'
        available = cells[4].text.strip()	
        if available != '':
            emegency_contraception_OTC_list.append([country_name, available[0]])
            if country_name == 'Zambia':
                break
            
# Convert General Lists to Dictionnaries
country_fertility_dict = {item[0]: item[1] for item in country_fertility_list}
country_education_index_dict = {item[0]: item[1] for item in country_education_index_list}
country_GDP_dict = {item[0]: item[1:] for item in country_GDP_list}
country_working_age_dict = {item[0]: item[1] for item in working_age_population_list}
country_sex_ratio_dict = {item[0]: item[1:] for item in sex_ratio_list}
country_OTC_contraception_dict = {item[0]: item[1] for item in emegency_contraception_OTC_list}
country_population_dict = {item[0]: item[1] for item in country_population_list}

# Combine lists: Fertility & GDP & Working Age Population
final_data = []

for country_name in country_fertility_dict.keys():
    if (country_name in country_GDP_dict) and (country_name in country_working_age_dict) and (country_name in country_sex_ratio_dict) and (country_name in country_OTC_contraception_dict) and (country_name in country_population_dict) and (country_name in country_education_index_dict):
        fertility_rate = country_fertility_dict[country_name]
        education_index = country_education_index_dict[country_name]
        GDP_IMF, GDP_WB, GDP_UN, Avg = country_GDP_dict[country_name]
        population = country_population_dict[country_name]
        working_age_population = country_working_age_dict[country_name]
        sex_ratio_15to24, sex_ratio_25to54 = country_sex_ratio_dict[country_name]
        available = country_OTC_contraception_dict[country_name]
        
        final_data.append([country_name, fertility_rate, education_index, GDP_IMF, GDP_WB, GDP_UN, Avg, population, working_age_population, sex_ratio_15to24, sex_ratio_25to54, available])
    else:
        print(country_name)

extracting_time = time.time() - start_time
print("EXTRACTING time : ", extracting_time)
        
# Write the country name and fertility rate data to a CSV file
with open('Country_General_Data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Country', 'Fertility Rate (2022)', 'Education Index', 'GDP IMF', 'GDP World Bank', 'GDP United Nations', 'Average GDP', 'Population', 'Working Age Population [15-64] (%)', 'M/F Ratio [15-24]', 'M/F Ratio [25-54]', 'Emergency Contraception [OTC]'])
    writer.writerows(final_data[0:len(final_data)])

print("Data has been written to country_fertility_data.csv file.")


global_time = time.time() - start_time_global
print("Global time : ", global_time)

