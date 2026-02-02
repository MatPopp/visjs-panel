import base64

def data_url_to_bytes(data_url):
    """
    Convert a data URL to bytes.

    Args:
        data_url (str): The data URL to convert.

    Returns:
        bytes: The decoded bytes from the data URL.
    """
    header, encoded = data_url.split(",", 1)
    data = base64.b64decode(encoded)
    return data