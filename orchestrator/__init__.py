import logging
import json
import os
from datetime import datetime
import azure.functions as func
import azure.durable_functions as df
from . import function_mover as fm

def orchestrator_function(context: df.DurableOrchestrationContext):
    
    querystring_list= yield context.call_activity('combine_company_list', "None")
   
    #auto_complete_activity= [ 
        #context.call_activity('auto_complete', querystring) 
            #for querystring in querystring_list if querystring]
    
    #inMemory_data= yield context.task_all(auto_complete_activity)

    return querystring_list #fm.auto_complete_mover_out(inMemory_data)

main = df.Orchestrator.create(orchestrator_function)