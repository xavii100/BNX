from app import validation_request

def test_invalid_email():
    email = "angie@citi.com"
    result = validation_request.is_invalid_email(email)
    assert result == True

def test_invalid_email_false():
    email = "am22783@imcla.lac.nsroot.net"
    result = validation_request.is_invalid_email(email)
    assert result == False

def test_is_null():
    assert True == validation_request.is_null(None)

def test_is_null_false():
    assert False == validation_request.is_null("test")

def test_is_list_empty():
    assert True == validation_request.is_list_empty(list())

def test_is_list_empty_false():
    mail_list = ["am22783@imcla.lac.nsroot.net","cv22783@imcla.lac.nsroot.net"]
    assert False == validation_request.is_list_empty(mail_list)