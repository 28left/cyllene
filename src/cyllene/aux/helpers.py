def diff_dict(dict_1: dict, dict_2: dict):
    """
    Collects those entries from a dictionary whose keys are not present in a second dictionary

    Args:
        dict_1: a Python dictionary
        dict_2: a Python dictionary

    Returns:
        A dict containing all key, value pairs from dict_1 for which key is not a key in dict_2.

        Example: 
        dicta = {"a": 1, "b": 2, "c": 3}
        dictb = {"b": 2}

        diff_dict(dicta, dictb) returns {'a': 1, 'c': 3}

    Raises:
        TypeError: One of the arguments is not a valid dictionary
    """

    if not isinstance(dict_1, dict) or not isinstance(dict_2, dict):

        raise TypeError("Arguments must be dictionaries.")

    return {key: dict_1[key] for key in dict_1.keys() - dict_2.keys()}


def extract_dict(my_dict: dict, keys: list):

    return_dict = {}
    for key in keys:
        if key in my_dict.keys():
            return_dict[key] = my_dict[key]

    return return_dict


def set_attr_dict(my_object, my_dict: dict):
    """
    Set attributes of an object as passed by a dictionary 

    Args:
        my_object: any Python object
        my_dict: any dictionary containing the key, value pairs to be set as attributes

    Raises:
        TypeError: if my_dict is not a dictionary
    """

    if isinstance(my_dict, dict):
        for key in my_dict.keys():
            setattr(my_object, key, my_dict[key])
    else:
        TypeError("Second argument must be a dictionary.")


def get_attr_dict(my_obj, my_keys: list) -> dict:

    if isinstance(my_keys, list):

        return_dict = {}

        for key in my_keys:
            return_dict[key] = getattr(my_obj, key, "")

        return return_dict

    else:
        TypeError("Second argument must be a list")
