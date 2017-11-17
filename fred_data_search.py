#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 21:57:25 2017
@title: FRED Search Tool for JPMC
@author: apoorv purwar
@email:  ap3644@columbia.edu
"""
 
import requests

# ********* Global Variables: Start *********
api_key = 'b94ef970b1bbd7a16e64e58809cfd252'
file_type = 'json'
search_limit = '10'
fred_api_domain = 'https://api.stlouisfed.org/fred/'

fred_series_url = fred_api_domain + 'series/'
url_payload = '&api_key=' + api_key + '&file_type=' + file_type
error = 'error_code'
# ********** Global Variables: End **********

# Prints the first welcome message for the user.
# @params - None
# @return value - None

def welcome_message():
    print('************************************')
    print('* Welcome to JPMC FRED Search Tool *')
    print('*      Author - Apoorv Purwar      *')
    print('************************************')

# Checks if the attribute to be displayed is returned or not
# @params - Attribute to be checked
# @return value - Attribute if valid, else N/A

def check_validity(param):
    if param is None:
        return 'N/A'
    else:
        return param

# Fetches the release_id of a particular series
# @params - Series Code
# @return value - Release ID for the series

def get_releaseID(series_code):
    
    releaseURL = fred_series_url + 'release?series_id=' + series_code + url_payload
    release_response = (requests.get(releaseURL)).json()
    
    if error in release_response:
        print(release_response["error_message"], "Try Again Later!")
    else:
        return release_response["releases"][0]["id"]            # Assuming there will always be 1 Release ID
    
# Fetches the source of a particular series
# @params - Series Code
# @return value - Source Name for the series
   
def get_source(series_code):
    
    release_id = get_releaseID(series_code)
    fred_release_url = fred_api_domain + 'release/sources?release_id=' + str(release_id) + url_payload
    source_response = requests.get(fred_release_url).json()
    if error in source_response:
        print(source_response["error_message"], "Try Again Later!")
    else:
        return source_response["sources"][0]["name"]            # Assuming the first data source is valid 

# Prints the search result for the received response
# @params - JSON Response
# return value - None
def print_search_results(response):
    print('\n Upto 10, Top Query Results:')
    print(' --------------------')
    
    for i in range(0,len(response['seriess'])):
        fred_code = check_validity(response['seriess'][i]['id'])
        source = check_validity(get_source(fred_code))
        title = check_validity(response['seriess'][i]['title'])
        observation_start = check_validity(response['seriess'][i]['observation_start'])
        observation_end = check_validity(response['seriess'][i]['observation_end'])
        frequency = check_validity(response['seriess'][i]['frequency'])
        
        print('\n {}) {} (FRED Code: {}) from {}'.format(i+1, title, fred_code, source))
        print('Observation - Start Date: {}, End Date: {}'.format(observation_start, observation_end))
        print('Frequency - {}'.format(frequency))
        print('_______________________')
        

# Search the FRED database to retrieve databases matching given search term
# @params - None
# return value - Search Result Response JSON      
def search_fred():
    
    # Get the keywords to look up the database user wants to search for
    keywords = input('Please Enter Search Term: ')

    # Fetch only the top 10 results, with search_limit
    url = fred_series_url + 'search?search_text=' + keywords + url_payload + '&limit=' + search_limit
    response = (requests.get(url)).json()
    # If response received, display the results, with the top parameters
    if error in response:
        print(response["error_message"], "Try Again Later!")
    # If search text returns no results
    elif not response["seriess"]:
        print("No results found for the search text, try again later!")
        return "invalid"
    else:
        print_search_results(response)
    
    return response    

# Get the observation values after selecting a databse
# @params - Search Response JSON
# return value - None 
def get_observations(response):
    
    db_id = input('Please select a Database from above list (Input Number: 1 - {}): '.format(len(response['seriess'])))
    db_id = int(db_id)
    if db_id > len(response['seriess']):
        print('Invalid database index entered, try again later!')
    else:    
        selected_db_title = response['seriess'][db_id-1]['title']
        selected_db_id = response['seriess'][db_id-1]['id']
        
        print('\n You selected {} (FRED Code: {}).'.format(selected_db_title, selected_db_id))
        
        start_date = input('Enter Observation Time Start Date (Format: YYYY-MM-DD): ')
        end_date = input('Enter Observation Time End Date (Format: YYYY-MM-DD): ')
        
        print('\n Frequency Legend:')
        print(' -----------------')
        
        print('d = Daily \n w = Weekly \n bw = Biweekly \n m = Monthly \n q = Quarterly \n sa = Semiannual \n a = Annual')
        
        frequency = input('Enter Frequency(d/w/bw/m/q/sa/a):')
        
        observation_url = fred_series_url + 'observations?series_id=' + selected_db_id + '&observation_start=' + start_date + '&observation_end =' + end_date + '&frequency=' + frequency + url_payload
        observation_response = (requests.get(observation_url)).json()
        
        if error in observation_response:
                print(observation_response["error_message"], "Try Again Later!")
        else:
                for i in range(0, len(observation_response["observations"])):
                    print('Date - {}; Value - {}'.format(check_validity(observation_response["observations"][i]["date"]), check_validity(observation_response["observations"][i]["value"])))

    
# Driver Function
if __name__ == "__main__": 
    
    # Welcome Greeting of the Tool
    welcome_message()
    # Search the FRED database
    response = search_fred()
    if response == "invalid":
        print('Terminating!')
    else:
        # Get Observations for the response
        get_observations(response)

