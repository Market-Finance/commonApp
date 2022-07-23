from shared import mover as mo

def auto_complete_mover_out(inMemory_data):
    """
    DESCRIPTION: The purpose of this function is to move mined auto complete
                 to this desired blob storage and data lake location 
    INPUT: None
    OUTPUT: status string
    """
    # Blob file path and file_name destination
    blob_file_path= 'MarketFinance/common/auto_complete_new'
    blob_file_name= 'auto_complete.json'

     # Data Lake path and file_name destination
    data_lake_file_path= 'common/auto_complete'
    data_lake_file_name= 'auto_complete'

    mo.blob_storage_upload(inMemory_data, blob_file_path, blob_file_name)
    mo.data_lake_storage_upload(inMemory_data, data_lake_file_path, data_lake_file_name)
    return "Success"