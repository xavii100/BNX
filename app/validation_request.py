# Define a function for validating an Email 
def is_invalid_email(email):   
    email = str(email)
    return False if email.endswith("@imcla.lac.nsroot.net") else True

# To validate null - Nones values
def is_null(field):         
    return True if field is None else False

# To validate list - Nones values
def is_list_empty(listdata):  
    return True if listdata is None or len(listdata) == 0 else False


def is_invalid_any_email(list_email):
    for email in list_email:
        if is_invalid_email(email):
            return True
    return False
