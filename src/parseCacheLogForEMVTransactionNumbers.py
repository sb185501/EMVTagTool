 
def search_multiple_strings_in_file(file_name):
    """Get line from the file, which contains any string from the list"""
    list_of_results = []
    list_of_strings = ['toEMVDATAMASKED1', 'soEMVDATAMASKED1']
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file
        for line in read_obj:
            # For each line, check if line contains any string from the list of strings
            for string_to_search in list_of_strings:
                if string_to_search in line:
                    # If any string is found in line, then append that line in list
                    list_of_results.append((string_to_search, line.rstrip()))

    # List of tuples containing transaction numbers
    list_of_trans = unique_emv_transactions_from_cacheLog(list_of_results)
    return list_of_trans
 
def unique_emv_transactions_from_cacheLog(matched_lines):
    list_of_each_tran=[]
    list_of_all_trans=[]
 
    # Searching for EMV transaction numbers
    for elem in matched_lines:
        log_as_string=elem[1]
        list_of_each_tran=log_as_string[50:60]
        list_of_all_trans.append(list_of_each_tran)
    
    # Giving list of unique transaction numbers
    unique_trans=set(list_of_all_trans)
    list_of_unique_trans=list(unique_trans)
    return list_of_unique_trans


