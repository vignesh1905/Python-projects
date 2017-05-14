# Code to scrap a table from a web page using Beautiful Soup

from bs4 import BeautifulSoup
import requests
import pandas as pd

#Setting up python to give request to the website
url = "http://www.elections.in/tamil-nadu/assembly-constituencies/2016-election-results.html"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, "lxml")

#Scarping the table from the website
table = soup.find_all('table')[1] # We need only the second table so we use
                                  # to get only the second table
rows = table.find_all('tr')
header = rows[0].find_all('th')
header_list = []

#Looping through the headers to get the required values
for cols in xrange(0,len(header)):
    col_name = header[cols].get_text()
    header_list.append(col_name)

normal_list = []
for i in xrange(len(header_list)):
    value = header_list[i].encode("utf-8")
    normal_list.append(value)

second_rows = table.find_all('tr')[1:]

#Simple data_frame where the data is stored
new_table = pd.DataFrame(columns=range(0,len(normal_list)), index =[range(0,234)])

#Getting the column headers
row_marker = 0
for row in second_rows:
    column_marker = 0 
    cols = row.find_all('td')
    for column in cols:
        new_table.iat[row_marker,column_marker] = (column.get_text()).encode("utf-8")
        column_marker += 1
    row_marker += 1

new_table.columns = normal_list

#Saving it to csv file
new_table.to_csv('election.csv')
