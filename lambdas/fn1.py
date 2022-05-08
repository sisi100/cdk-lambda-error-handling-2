from time import sleep


def handler(event, context):
    """一生眠るLambda"""
    sleep(15 * 60)
