import os
from app.exception import BadRequest
from app.log import log

def send(message, subject, receiver, sender):
    try:
        senders_string = ' '.join(sender)
        shell = """echo -e {} | mailx -v -r "{}" -s "{}" {}""".format(message,receiver,subject,senders_string)
        stream = os.popen(shell)
        output = stream.read()
        print(output)
        print("Message was sended")
        return True
    except Exception as ex:
        log.info('%s, %s', ex, "mail_list")
        raise BadRequest("Error trying to send the message", "mail_list")   
