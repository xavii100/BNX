from flask import Blueprint,Response,request,current_app
from flask_mail import Message
from app import emailfunction, request_validator
import os

notifications = Blueprint('notifications',__name__, url_prefix='/api/v1/')

'''
    Function to send a message
'''
@notifications.route('/notification/send', methods=['POST'])
def send():
    request_validator.validate_header(request.headers)
    request_validator.validate_request_body(request.json)
    req = request.get_json()
    subject = req['subject']
    body = req['body']
    mail_list = req['mail_list']
    # issuer_mail = req['issuer_mail']
    base_route = os.environ.get("BASE_ROUTE")
    if base_route is None:
        base_route = "test"
    issuer_mail = "trr_dply@{}".format(base_route)
    resp = emailfunction.send(body,subject,issuer_mail,mail_list)
    print(resp)
    return Response(status=200)

'''
    Function to send a message
'''
@notifications.route('/notification/test', methods=['POST'])
def send_test():
    base_route = os.environ.get("BASE_ROUTE")
    if base_route is None:
        base_route = "test"
    issuer_mail = "trr_dply@{}".format(base_route)
    body = "Hola mi nombre es:\nAngie"
    subject = "Test"
    mail_list = ["am22783@imcla.lac.nsroot.net", "cs71471@imcla.lac.nsroot.net"]
    resp = emailfunction.send(body,subject,issuer_mail,mail_list)
    print(resp)
    return Response(status=200)

'''
    Api health.
'''
@notifications.route('/swagger', methods=['GET'])
def swagger():
    return Response(response = '{}', mimetype = 'application/json')