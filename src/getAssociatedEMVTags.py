 
def getAssociatedEMVTags(file_name, tran_num):
    list_of_results = []
    list_of_emv_tags = []
    list_of_final_emv_tags = []
    transactionNumber = tran_num
    search_NVP_criteria_1 = transactionNumber+"'soEMVDATAMASKED1'"
    search_NVP_criteria_2 = transactionNumber+"'toEMVDATAMASKED1'"
    list_of_strings = [search_NVP_criteria_1,search_NVP_criteria_2]

    #"""Get line from the file, which contains any string from the list"""
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains any string from the list of strings
            for string_to_search in list_of_strings:
                if string_to_search in line:
                    # If any string is found in line, then append that line 
                    list_of_results.append((string_to_search, line.rstrip()))
    matched_lines = list_of_results

    # Loop through to get the associated NVP
    for elem in matched_lines:
        list_of_final_emv_tags.append(elem[1])
        
    # Parsing the NVP based on the index to be able to read EMV tags
    list_of_emv_tags.append(list_of_final_emv_tags[-1])
    string_holding_emv_tags=(str(list_of_emv_tags))
    
    startIndex=string_holding_emv_tags.find("(",0,100)
    endIndex=string_holding_emv_tags.find(")",-10,-1)
    list_of_emv_tags=string_holding_emv_tags[startIndex+1:endIndex]
   
    # Spliting the tags by the delimeter and returing the tags (List of tuples)
    # Eg: Format of the tags returned - [('50', '5649534120435245444954'), ('5A', 'XXXXXXXXXXXXXXXX')]
    list_toSplit_byDelimeter=[]
    list_toSplit_byDelimeter=list_of_emv_tags.split("\\x1c")
    list_of_tuples_EMVtags = [tuple(map(str, sub.split('='))) for sub in list_toSplit_byDelimeter]  
    list_of_tuples_EMVtags.pop()
    
    return list_of_tuples_EMVtags
