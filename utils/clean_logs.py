import json


def format_log(log):
    """
    Convert the input log into a dictionary format suitable for use with Python functions.
    :param log:
        The input log that needs to be formatted.
    :return: dict
        A dictionary representing the formatted log.
    """
    items = log.split('|')
    logs_transformed = {}

    for item in items:
        key, value = item.split('=')
        if key == 'site':
            value = json.loads(value.replace("'", "\""))
        logs_transformed[key] = value

    return logs_transformed


def is_expected_format(log):
    """
    Validate whether the given log dictionary adheres to the expected format for table insertion.

    :param log: dict
        A dictionary representing a formatted log entry.
    :return: bool
        Returns True if the log format meets the expected criteria; otherwise, returns False.
    """
    keys = ['id', 'therapeutic_area', 'created_at', 'site']
    sub_keys = ['site_name', 'site_category']
    if (
            len(log) == 4 and
            len(log.get('site', {})) == 2 and
            all(key in log for key in keys) and
            all(sub_key in log.get('site', {}) for sub_key in sub_keys)
    ):
        return True
    return False
