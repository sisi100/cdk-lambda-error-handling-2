class HogehogeException(Exception):
    pass


def handler(event, context):
    """例外を投げるlambda"""
    raise HogehogeException("HHHHHHHHOOOOOOOOOOGGGGGGGGEEEEEEEE")
