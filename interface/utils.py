import simplejson as json


def string_to_json(string):
    """
    Convert Text field to JSON
    :param string: Django models text field
    :return: JSON structure
    """
    return json.loads(str(string))
