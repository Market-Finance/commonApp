# Market Finance- Common Application
The purpose of the Market Finance common application is to extract the starting point for the analytical engine. The starting point, meaning the stock symbol, region, company names and symbol's news clippings id for the query search. The starting point is extracted by using open source NASDAQ and ASX listing API. Then the list is appended and passed through the Yahoo Finance API to pull the standardised API's query string for other endpoint requests, as the schema's requirements are slightly different. As a result, the success of API calls is increased, and this approach improves the data quality by fixing the data upstream.

## Table of Contents  
- [Local System Setup](#1-local-system-setup)
- [Establish Global variables for Azure CLI](#2-establish-global-variables-for-azure-cli)
- [Create a new repository in Github](#3-create-a-new-repository-in-github)
- [Create a Azure function app](#4-create-a-azure-function-app)
- [Configure host.json file](#5-configure-hostjson-file)
- [Configure the local.settings.json file](#6-configure-the-localsettingsjson-file)
- [Create Azure function App on Azure portal](#7-create-azure-function-app-on-azure-portal)
- [Setup and Configure variables for Azure function environment](#8-setup-and-configure-variables-for-azure-function-environment)
- [Azure functions App role assigments for all the service such as blob storage, DataLake and keyvault](#9-azure-functions-app-role-assigments-for-all-the-service-such-as-blob-storage-datalake-and-keyvault)
- [Setup CI/CD for Azure function application](#10-setup-cicd-for-azure-function-application)
- [Check the configuration of the Azure function Application](#11-check-the-configuration-of-the-azure-function-application)
- [Stock Application Implementation Overview](#12-stock-application-implementation-overview)
    - [Durable Functions](#121-durable-functions)
    - [Activities](#122-activities)
        - [Combine companies](#combine-companies)
        - [Auto complete](#auto-complete)
    - [DurableFunction Http](#123-durablefunction-http)
    - [Orchestrator](#124-orchestrator)
    - [Shared](#125-shared)
        - [Function Requests](#1251-function-requests)
        - [Mover](#1252-mover)
- [Git push and Deploy](#13-git-push-and-deploy)

<a name="1-local-system-setup"/>
<a name="2-establish-global-variables-for-azure-cli"/>
<a name="3-create-a-new-repository-in-github"/>
<a name="4-create-a-azure-function-app"/>
<a name="5-configure-hostjson-file"/>
<a name="#6-configure-the-localsettingsjson-file"/>
<a name="#7-create-azure-function-app-on-azure-portal"/>
<a name="#8-setup-and-configure-variables-for-azure-function-environment"/>
<a name="#9-azure-functions-app-role-assigments-for-all-the-service-such-as-blob-storage-datalake-and-keyvault"/>
<a name="#10-setup-cicd-for-azure-function-application"/>
<a name="#11-check-the-configuration-of-the-azure-function-application"/>
<a name="#12-stock-application-implementation-overview"/>
<a name="#121-durable-functions"/>
<a name="#122-activities"/>
<a name="#combine-companies"/>
<a name="#auto-complete"/>
<a name="#123-durablefunction-http"/>
<a name="#124-orchestrator"/>
<a name="#125-shared"/>
<a name="#1251function-request"/>
<a name="#1252mover"/>
<a name="#13-git-push-and-deploy"/>

The following details the implementation of the Common Application (end-to-end)
## 1. Local System Setup
```
# Check for python version 3.7 or greater
python --version

# Make sure Azure CLI is installed
az --version

# Make sure visual studio code is installed
code --version

# Make sure Azure Function Core Tools are installed
func --version

# Run az login to sign into Azure 
az login

# Turn on the param-persit option, so the varibles are automatically stored
az config param-persit on
```

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

## 2. Establish Global variables for Azure CLI
```
# Define the region for Application services
$service_location= <define your server location>

# Define the resource group used
$resource_group_name = <define your resource group name>

# Define the email user name for admin access 
$user_email= <define your user email address>

# Define the Blob's production container name
$abs_container_name= <define your blob storage production container name> 

# Define the Blob's archive container name
$abs_archive_container_name= <define your blob storage archive container name>

# Extract the blob storage account Id through Azure CLI
$storage_acct_id=$(az storage account show --name $storage_acct_name --resource-group $resource_group_name --query 'id' --output tsv)

# Extract the blob storage account key through Azure CLI
$storage_acct_key1=$(az storage account keys list --resource-group 
$resource_group_name --account-name $storage_acct_name --query [0].value --output tsv)

# Define the production Data Lake 
$adls_acct_name= <define your datalake account name> 
$fsys_name= <define your file root name>
$dir_name= <sub directory>

# Extract the datalake storage account key through Azure CLI
$adls_acct_key1=$(az storage account keys list --resource-group $resource_group_name --account-name $adls_acct_name --query [0].value --output tsv)

# Define the key vault name
$key_vault_name= <define your key vault name>

# Define the blob secret name
$abs_secret_name= <define your blob storage secrets name>

# Define the Data Lake secret name
$adls_secret_name= <define your data lake storage secrets name>

# Define the function application name
$funcapp_name= commonApp
```

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

## 3. Create a new repository in Github
```
# git clone to the project root
git clone <url>
```

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

## 4. Create a Azure function app
```
# Create a function project in the desired folder
# Make sure your are in the right folder directory
func init commonApp --python

# Create Python virual environment
python -m venv .venv 

# Activate Python virtual environment
...venv\Scripts\activate

# Install the requried packages
pip install -r requirements.txt
````

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

## 5. Configure host.json file
```
# Open the host.json file and add function Time out limit
## Set to 3 hours
{
    "functionTimeout": "03:00:00"
}
```

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

## 6. Configure the local.settings.json file
```
# Open the local.settings file and define the following
{
    "ABS_SECRET_NAME": "abs-access-key1" <define your blob secret name stored in the secret valult>,
    "ADLS_SECRET_NAME": "adls-access-key1" <define your data lake secret name stored in the secret vault> ,
    "KEY_VAULT_NAME": "kvmarketfinance" <define your key vault name>,
    "X_RAPIDAPI_HOST": "x-rapidapi-host" <define your X_RAPIDAPI_HOST name>,
    "X_RAPIDAPI_KEY": "x-rapidapi-key <define your X_RAPIDAPI_KEY>"
}
```

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

## 7. Create Azure function App on Azure portal
```
# Create Function app
## Basic
subscription= <define your Azure subscription>
resouces_group= <define your resource group>
function_app_name= <define your function app name>
publish= 'code'
Runtime_stack= python
region= 'australiaEast'

## Hosting
storage_account_name= <define your blob storage account name>
operating_system= 'linux'
plan_type= 'App service plan'
linux_plan= <define your app service plan name>
sku_and_size= <select based on the app service plan>

# follow default settings for other sections
## Create
```
[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

## 8. Setup and Configure variables for Azure function environment
```
az functionapp config appsettings set --name $funcapp_name --resource-group $resource_group_name --settings "KEY_VAULT_NAME=kvmarketfinance"
az functionapp config appsettings set --name $funcapp_name --resource-group $resource_group_name --settings "ABS_SECRET_NAME=abs-access-key1"
az functionapp config appsettings set --name $funcapp_name --resource-group $resource_group_name --settings "ADLS_SECRET_NAME=adls-access-key1"
az functionapp config appsettings set --name $funcapp_name --resource-group $resource_group_name --settings "X_RAPIDAPI_HOST= x-rapidapi-host"
az functionapp config appsettings set --name $funcapp_name --resource-group $resource_group_name --settings "X_RAPIDAPI_KEY= x-rapidapi-key"
```

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

## 9. Azure functions App role assigments for all the service such as blob storage, DataLake and keyvault
```
az functionapp identity assign --resource-group $resource_group_name --name $funcapp_name
$func_principal_id=$(az resource list --name $funcapp_name --query [*].identity.principalId --output tsv)
$kv_scope=$(az resource list --name $key_vault_name --query [*].id --output tsv)
az keyvault set-policy --name $key_vault_name --resource-group $resource_group_name --object-id $func_principal_id --secret-permission get list set
az role assignment create --assignee $func_principal_id --role 'Key Vault Contributor' --scope $kv_scope
az role assignment create --assignee $func_principal_id --role 'Storage Blob Data Contributor' --resource-group  $resource_group_name
az role assignment create --assignee $func_principal_id --role 'Storage Queue Data Contributor' --resource-group  $resource_group_name
```

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

## 10. Setup CI/CD for Azure function application
```
# Deployment center for commonApp
source= 'Github'
sign_in= <define your github username and password>
organisation= <define your organisation name>
repository= <define your repository>
branch= main
build_povider= 'GitHub Actions'
Runtime_stack= python
Version= Python 3.8
```

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

## 11. Check the configuration of the Azure function Application
```
# CommonApp configuration
# Application settings 
# Name value and source of 
# ABS_SECRET_NAME, ADLS_SECRET_NAME, X_RAPIDAPI_HOST, X_RAPID_API_KEY are
# referencing the key vault, if not add it manually
click edit, change and save
for value
@Microsoft.KeyVault(SecretUri=https://<key_vault_name>.vault.azure.net/secrets/<secret_name>/<version>)
```

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

## 12. Common Application Implementation Overview
```mermaid
    flowchart TD
    subgraph Flow diagram details the overview of Common App Engine Implementation
            A[Auto Complete]
            BA[ASX listed companies]
            BB[NASDAQ listed companies]
            B[Combine List companies]
            D[Orchestrator]
            F[Blob Storage]
            G[Data Lake]

            subgraph Common Application Durable Functions HTTP Start
                BA --> B
                BB --> B
                D -- FAN IN, and Upload --> G 
                D -- FAN IN, and Upload --> F
                B -- FAN OUT to list of companies --> D 
                A --> D
                end
            end    
```
### 12.1 Durable function
The durable function is an extension of Azure functions that utilises stateful operations in a serverless environment. The extension manages state, checkpoints, and restarts based on the demand. Durable parts have several features that make it easy to incorporate durable orchestrations and entities into HTTP workflow.

    1. Express your workflows in code
    2. Retry activities
    3. Run activities in parallel
    4. Timeout workflows
    5. State management for free
    6. Check on workflow progress with REST API
    7. Cancel workflow
    8. Serverless pricing model
    9. Versioning made easier 
    10. Develop and test locally distributed

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

### 12.2 Activities
The Azure function activity allows running Azure functions in an Azure Data Factory pipeline. By creating a linked services connection, we can run Azure functions. The linked services can control the execution plan for an Azure function.

#### Combine Companies 
Combining companies' activities is used to extract the list of targeted companies. A combined companies list script was written to scale and merge multiple sources of the company list. Given the current requirements of the market scanner, only NASDAQ and ASX listed companies are used in the list consolidation. Future updates will include NZX, etc., and the necessary framework is established to accommodate the updates.

#### Auto Complete
Once the combined companies list is extracted from various open data sources, the list of companies is passed through the auto-complete Rapid API to standardise the stock symbols. This auto-complete is an API that takes in query text string (could be partial name or symbol), conducts a search, finds the closest match, and spits out the standardised symbol for a given stock. This is ideal as it mitigates any risk of running incorrect queries for other API Calls with takes in the parameters from Auto-Complete response JSON. 

The query string list runs through the Fan-out/ Fan in Durable function pattern. This executes multiple functions in parallel and then wait for all function to finish. In our case, during the fan in the JSON response is appended together. 

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

### 12.3 DurableFunction Http 
This feature simplifies calling HTTP APIs from your orchestrator functions. As you may know, in an orchestrator function, you're not allowed to perform any non-deterministic operations, so to call an HTTP API, you would need to call an activity function and make the HTTP request there. The Durable HTTP feature removes the need to create an additional activity function.

Durable functions have several features that make it easy to incorporate durable orchestrations and entities into HTTP workflows—and utilising async operations tracking, with this approach, if the calling API's long-running operations, it would simply return 202 and the running status. We could call the API again to find the status of the running session until the underlying activities are completed. 

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

### 12.4 Orchestrator
The orchestrator function is used to orchestrate the execution of other Durable functions within a function app (CommonApp). The following are some of the characteristics of the orchestrator function. 
    
    - Orchestrator functions define function workflows using procedural code. No declarative schemas or designers are needed. 
    - Orchestrator functions can call other durable functions synchronously and asynchronosuly. Output from called functions can be reliably saved to local variables. 
    - Orchestrator functions are durable and reliable. Execution progress is automatically checkpointed when the function "yield". Local state is never lost when the process recycles or the VM reboots. 
    - Orchestrator functions can be long-running. The total lifespan of an orchestration instance can be seconds, days, months, or never-ending. 

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

### 12.5 Shared
#### 12.5.1 Function Requests
Function Request is a generalised function named miner that takes in the API endpoint URL and its respective query string. It checks for the error message and tries to execute the call again (if it exceeds the rate limit) by adding a sleep statement for a few seconds. This returns a JSON response and gets appended while the miner function gets used in an activity function.

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

#### 12.5.2 Mover
Mover file is a compilation of various code snips such as,  blob_container_service_client, datalake_service_client, return_blob_files, blob_storage_download, blob_storage_upload, and blob_storage_upload, data_lake_storage_upload, and blob_storage_delete. The file represents all the data mover in and out of the function's Local Memeory/ storage (blob and datalake). 

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)

## 13. Git push and Deploy
```
# commit the changes and push
git push
```

[Back to Table of Contents](https://github.com/Market-Finance/commonApp#table-of-contents)