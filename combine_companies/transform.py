# Import libraries
import logging
import requests
import csv
from datapackage import Package

def dict_filter_in(company_dict, interested_keys):
    """
    DESCRIPTION: The purpose of this function is to extract only the interested_keys from all_keys
                 Based on- is in the subset
    INPUT: all_keys, interested_keys
    OUTPUT: Dictionary with interested_keys
    """
    dictList= dict([(i, company_dict[i]) for i in company_dict if i in set(interested_keys)])
    return dictList

def asxlisted_companies():
    """
    DESCRIPTION: The purpose of this function is to extract the list of 
                 ASX listed companies
    INPUT: NONE
    OUTPUT: Dictionary with code, Company name, region
    """
    # Buid the schema to standardise
    interested_keys= ('ASX code', 'Company name')
    insert_dict= {'region': 'AU'}
    
    # CSV URL location
    CSV_URL= 'https://asx.api.markitdigital.com/asx-research/1.0/companies/directory/file?access_token=83ff96335c2d45a094df02a206a39ff4'

    # Hit the CSV API and decode values
    with requests.get(CSV_URL, stream= True) as r:
        lines= (line.decode('utf-8') for line in r.iter_lines())
    
        rows= list()
        for row in csv.reader(lines):
            rows.append(row)

    # Iterate over the rows and append the dictionary to create a list of dictionaries
    company_list= list()
    for i in range(len(rows[1:])):
        company_dict= dict_filter_in(dict(zip(rows[0], rows[1:][i])), interested_keys)
        company_dict['ASX code']= str(company_dict['ASX code']) + '.AX'
        company_dict['code']= company_dict.pop('ASX code')
        company_dict["q"]= company_dict.pop("code")
        company_dict.update(insert_dict)
        company_list.append(company_dict)

    return company_list[:150]

def nasdaqlisted_companies():
    """
    DESCRIPTION: The purpose of this function is to extract the list of 
                 nasdaq listed companies
    INPUT: NONE
    OUTPUT: Dictionary
    """
    package= Package('https://datahub.io/core/nasdaq-listings/datapackage.json')

    # Buid the schema to standardise
    keys_names= ['code', 'Company name']
    insert_dict= {'region': 'US'}
    
    # Iterate over and append all the company names
    company_list= list()
    for company in package.resources:
        if company.descriptor['datahub']['type'] == 'derived/csv':
            company_array= company.read()
            company_list.append(company_array)

    # Iterate over and append list of company dictionaries with 
    # Code, Company name and Region
    company_dict_list= list()
    for i in range(len(company_list[1])):   
        company_dict= dict(zip(keys_names, company_list[1][i]))
        company_dict["q"]= company_dict.pop("code")
        company_dict.update(insert_dict)
        company_dict_list.append(company_dict)
            
    return company_dict_list[:150]

def combine_company_list(company_list:list):
    """
    DESCRIPTION: The purpose of this function is to combine arrays of 
                 listed companies from various stock exchanges
    INPUT: array of company_list
    OUTPUT: combined company list of dictionaries
    """
    newlist= [y for x in company_list for y in x]

    return newlist  
