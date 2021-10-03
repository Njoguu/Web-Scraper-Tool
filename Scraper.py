from selenium import webdriver
from bs4 import BeautifulSoup as soup
from openpyxl.workbook import *
import pandas as pd
import xlsxwriter


# make use of webdriver
driver = webdriver.Chrome("/USERS/USER/Downloads/chromedriver") # --> Storage path of the chromedriver

# get page metadata
driver.get("https://countrycode.org/") # --> link address for webpage you want to scrape the data from

content = driver.page_source
page_soup = soup(content, "html.parser")


# Getting the data and adding them to a list
# get list of country names
countries = []
country = page_soup.findAll('td', attrs = {'class':'country-col'})
for ctry in country:
    country_name = ctry.a.text
    countries.append(country_name)


codes = []
codes = page_soup.findAll('td', attrs = {'class': 'codes-col'})
for code in codes:
    country_code = code.a.text
    codes.append(country_code)

# Displaying all the data in an Excel Spreadsheet
a = {'Country' : countries ,'Code' : codes}
data = pd.DataFrame.from_dict(a, orient='index')
data = data.transpose()

writer = pd.ExcelWriter('countrycodes.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
data.to_excel(writer, sheet_name='Sheet1', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()

driver.close()