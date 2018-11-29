def xmltodict(xml):
    import xmltodict
    obj = xmltodict.parse(xml)
    return obj

def dicttoxml(dict_obj):
    return _dicttoxml(dict_obj)

def _dicttoxml(dict_obj, root=False, attr_type=False, cdata=True):
    import dicttoxml
    return dicttoxml.dicttoxml(dict_obj, root=False, attr_type=False, cdata=True)

def make_qrcode_image(data, **kwargs):
    """Creates a QRCode image from given data."""
    from qrcode import QRCode
    qrcode = QRCode(**kwargs)
    qrcode.add_data(data)
    return qrcode.make_image()

def get_now_ts_sec():
    import time
    return int(time.time())
