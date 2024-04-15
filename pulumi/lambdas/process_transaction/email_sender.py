from typing import Any
from email.message import EmailMessage
import tabulate
import base64


def format_summary_email(summary: dict[str, Any]):
    """
    Formats the summary information as an email, accounting for nested dictionaries.

    :param summary: A dictionary with summary information.
    :param depth: The current depth of nesting (default is 0).
    :return: A string containing the formatted email.
    """
    # Convert the image to base64 for embedding in HTML
    with open("./stori_logo.jpg", "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode()

    # Convert the dictionary to a formatted table
    table = tabulate.tabulate(summary.items(), tablefmt="html")

    # Create an email message with HTML content
    msg = EmailMessage()
    msg.set_content(
        f"""
        <html>
            <body>
                <h2>Transaction Details:</h2>
                <img src="data:image/jpeg;base64,{image_data}" alt="Logo">
                {table}
            </body>
        </html>
        """,
        subtype="html",
    )
    msg["Subject"] = "Transaction Summary"
    msg["From"] = "sender@example.com"
    msg["To"] = "recipient@example.com"

    return msg
