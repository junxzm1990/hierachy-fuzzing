import sys

def RepresentsInt(s) :
    try : 
        int(s)
        return True
    except ValueError :
        return False

def RepresentsFloat(s) :
    try :
        float(s)
        return True
    except ValueError :
        return False
def RepresentsStr(s) : 
    try :
        str(s)
        return True
    except ValueError : 
        return False

def token_classifer (raw_token_dict) :
    class_token_dict = dict()
    # print (raw_token_dict)
    # CLASSIFYING OBJECTS ENTRIES depending on each token's content type
    for i in raw_token_dict : 
        # Class 1 : read-in objects. eg : 3 0 R
        if "R" in raw_token_dict[i] and "0" in raw_token_dict[i] :
            if "rd_in_obj_token" not in class_token_dict :
                class_token_dict["rd_in_obj_token"] = {i : raw_token_dict[i]}
            else :
                class_token_dict["rd_in_obj_token"].update({i : raw_token_dict[i]}) 
        # Class 2 : read-in type is matrix : eg /Matrix
        elif '[' in raw_token_dict[i] and ']' in raw_token_dict[i] :
            if "rd_in_mtrx_token" not in class_token_dict : 
                class_token_dict["rd_in_mtrx_token"] = {i : raw_token_dict[i]}
            else :
                class_token_dict["rd_in_mtrx_token"].update({i : raw_token_dict[i]})
        # Class 3 :  read-in type is int : eg /Ff
        elif RepresentsInt(raw_token_dict[i][0]) and RepresentsFloat(raw_token_dict[i][0]) :
            if "rd_in_digit_token" not in class_token_dict :
                class_token_dict["rd_in_digit_token"] = {i : raw_token_dict[i]}
            else :
                class_token_dict["rd_in_digit_token"].update({i : raw_token_dict[i]})
        # Class 4 : read-in type is string : 
        elif RepresentsStr(raw_token_dict[i][0]) :
            if 'rd_in_str_token' not in class_token_dict : 
                class_token_dict['rd_in_str_token'] = {i : raw_token_dict[i]}
            else :
                class_token_dict['rd_in_str_token'].update({i : raw_token_dict[i]})
        else :
            if 'others' not in class_token_dict :
                class_token_dict['others'] = {i : raw_token_dict[i]}
            else :
                class_token_dict['others'].update({i : raw_token_dict[i]})
    #print (class_token_dict['rd_in_str_token'])     
    return class_token_dict
    
#def mutation_strategy ()
#    # mutation on Class 1 (read-in objects) : pick an other object


#def main(argv) :
#    raw_diff_path = argv
#    raw_token_dict = token_dict.main(raw_diff_path)
#    token_classifer(raw_token_dict)
#
