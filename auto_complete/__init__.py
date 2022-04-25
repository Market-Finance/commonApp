# Import libraries
import os
import pandas as pd
import numpy as np
import requests
import json
import time
import random
import sys
from shared.fun_request import *

# Override default settings
sys.setrecursionlimit(10000)

def main(querystring):
    """
    DESCRIPTION: The purpose of this function is to extract the list of company
    symbols from asx and nasdaq. And company symbols are then queried by
    request x_rapid_api to return auto_complete
    INPUT: query string dictionary
    OUTPUT: auto_complete dictionary
    """
    url= "https://apidojo-yahoo-finance-v1.p.rapidapi.com/auto-complete"
    auto_complete_dict= miner(url, querystring)
    return auto_complete_dict