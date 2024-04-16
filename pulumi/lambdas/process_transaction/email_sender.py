from typing import Any
import tabulate
from jinja2 import Environment, FileSystemLoader
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def format_summary_email(summary: dict[str, Any], logo_url: str):
    """
    Formats the summary information as an email, accounting for nested dictionaries.

    :param summary: A dictionary with summary information.
    :param depth: The current depth of nesting (default is 0).
    :return: A string containing the formatted email.
    """

    # Convert the dictionary to a formatted table
    table = tabulate.tabulate(summary.items(), tablefmt="html")

    # Set up the Jinja2 template
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template("email_template.html")

    # Render the template with the table and logo_url variables
    html_content = template.render(table=table, logo_url=logo_url)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Transaction Summary"
    msg["From"] = "sender@example.com"
    msg["To"] = "recipient@example.com"

    # Turn into html MIMEText objects
    part1 = MIMEText(html_content, "html")

    # Add HTML parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)

    return msg
