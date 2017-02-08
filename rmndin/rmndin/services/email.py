from flask import render_template
from jinja2.exceptions import TemplateNotFound

from rmndin import app
from rmndin.lib import email


def send_email(recipients, subject, from_address, text=None, html=None):
    """
    Send an email given four required parameters.

    :param recipients: <list> of valid email addresses
    :param subject: <str> for subject line
    :param from_address: <str> Email you will appear as to recipient.
    :param text: <str> for body text

    :return: Response
    """
    apikey = app.config.get('MAILGUN_API_KEY')
    base_url = app.config.get('MAILGUN_BASE_URL')
    return email.send_email(recipients=recipients, subject=subject,
                            from_address=from_address, apikey=apikey,
                            base_url=base_url, text=text, html=html)


def send_template_email(recipients, subject,
                        from_address, variables, template):
    """
    Send an email using templates and variables.

    :param recipients: <list> of valid email addresses
    :param subject: <str> for subject line
    :param from_address: <str> Email you will appear as to recipient
    :param variables: <dict> containing key/val arguments for the template
    :param template: <str> designating the template path without extension.

    :return: Response
    """
    with app.app_context():
        try:
            html = render_template("%s.html" % template, **variables)
        except TemplateNotFound:
            html = None

        try:
            text = render_template("%s.txt" % template, **variables)
        except TemplateNotFound:
            text = None

    if not (text or html):
        raise TemplateNotFound("No template found with base path '%s'." %
                               template)
    return send_email(recipients=recipients, subject=subject,
                      from_address=from_address, html=html, text=text)
