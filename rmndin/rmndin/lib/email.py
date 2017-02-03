import requests


def send_email(subject, recipients, from_address, apikey,
			   base_url, text=None, html=None):
    url = base_url + '/messages'
    auth = ("api", apikey)
    data = {
        "from": "Rmndin <%s>" % from_address,
        "to": recipients,
        "subject": subject,
        "text": text,
        "html": html
    }
    return requests.post(url, auth=auth, data=data)
