import simplejson as json
from simplejson.scanner import JSONDecodeError


def string_to_json(string):
    """
    Convert Text field to JSON
    :param string: Django models text field
    :return: JSON structure or None (JSONDecodeError)
    """
    try:
        return json.loads(str(string))
    except JSONDecodeError:
        return None
