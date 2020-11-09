# ms-notification-feature
This microservice sends an email to notify, validate email and subject to send an email.

# exist_file
## Description
This api will receive a subject, a valid email, and a message.

```python
send()
```
1. Call the send function to send a notification
2. Return a message to know the message was sended

### Note

### Versioning

* **Version** 1.0.0

- **LOG classes**
	- N/A

*  **Checkstyle** 
	- N/A

* **PMD changes**
	- N/A

* **FindBugs**
	- N/A

* **Others**
	- N/A

#### Last modification date:
10/10/2020 - MJ79567, AM22783 

## Endpoint
>/api/v1/notifications/send (POST) 

### Request data

#### URL: /api/v1/notifications/send - POST

```json
{
  "issuer_mail": "botmail@citi.com",
  "mail_list": [
    "mail@citi.com",
    "mail2@citi.com",
    "mail3@citi.com"
  ],
  "subject": "File validated succesfully",
  "body": "Congrats! your file is validated"
}
```
### Response data
```json
{
  "type": "invalid",
  "code": "string",
  "details": "string"
}
```

-Check the soap-ui projects in doc directory for tests with SOAP UI tool in local and dev environments. 

## Built With
* Flask

### Prerequisites
You need to have installed:
    
- Logged in the citi banamex intranet 
 - Python 3.7.0
 - pipenv

- Install the libraries in the requirements.txt with a virtual environment

## Deployment
```console
  $ python -m venv venv
  $ venv/Scripts/activate.bat
  $ pip install -r requirements.txt
  $ SET FLASK_APP = setup.py
  $ SET_FLASK_ENV = development
  $ flask run
```

### Running JUnit tests

```console
  $ pytest
```

### Running in local mode
- To run app in Windows: py -m flask run
- To run tests in Windows: py -m pytest


### Reporting

#### site

#### Sonar
