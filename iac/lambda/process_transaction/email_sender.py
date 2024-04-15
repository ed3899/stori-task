from typing import Any

def format_summary_email(summary: dict[str, Any], depth: int = 0) -> str:
    """
    Formats the summary information as an email, accounting for nested dictionaries.

    :param summary: A dictionary with summary information.
    :param depth: The current depth of nesting (default is 0).
    :return: A string containing the formatted email.
    """
    email_content = ""
    for key, value in summary.items():
        if isinstance(value, dict):
            # Add indentation
            email_content += f"{'  ' * depth}{key}:\n"
            # Recurse until you find a value
            email_content += format_summary_email(value, depth + 1)
        else:
            # Normal content with indentation
            email_content += f"{'  ' * depth}{key}: {value}\n"

    return email_content