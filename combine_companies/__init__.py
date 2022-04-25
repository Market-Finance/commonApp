# Import libraries
from . import transform as tr

def main(name:str):
    """
    DESCRIPTION: The purpose of this function is to extract and combine list
                 of ASX and NASDAQ listed companies and combine
    INPUT: None
    OUTPUT: list of combined companies
    """
    # AutoComplete Data Transformation
    combine_list= [tr.asxlisted_companies(), tr.nasdaqlisted_companies()]

    combine_companies= tr.combine_company_list(combine_list)
    return combine_companies[:5]
