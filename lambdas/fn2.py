import json
import os
from pprint import pprint

import boto3


def handler(event, context):
    """lambdaを同期呼び出しするlambda"""

    # 同期呼び出し
    client = boto3.client("lambda")
    response = client.invoke(FunctionName=os.getenv("FUNCTION_NAME"))

    # こんなレスポンスが返ってくる。Lambdaで例外が発生してもLambdaとしては正常終了してるので例外はでない。
    pprint(response)
    # {'ExecutedVersion': '$LATEST',
    # 'FunctionError': 'Unhandled',
    # 'Payload': <botocore.response.StreamingBody object at 0x7fc86c9de310>,
    # 'ResponseMetadata': {'HTTPHeaders': {'connection': 'keep-alive',
    # 'content-length': '263',
    # 'content-type': 'application/json',
    # 'date': 'XXX, 00 XXX 0000 00:00:00 XXX',
    # 'x-amz-executed-version': '$LATEST',
    # 'x-amz-function-error': 'Unhandled',
    # 'x-amzn-remapped-content-length': '0',
    # 'x-amzn-requestid': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    # 'x-amzn-trace-id': 'root=1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;sampled=0'},
    # 'HTTPStatusCode': 200,
    # 'RequestId': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    # 'RetryAttempts': 0},
    # 'StatusCode': 200}

    # エラー発生の有無は`FunctionError`の有無判断する
    if response.get("FunctionError"):
        print("同期呼び出ししたLambdaは例外を吐いたよ！！")

        # errorの中身はここで確認できる
        payload = response["Payload"].read().decode("utf8")
        payload_dict = json.loads(payload)
        pprint(payload_dict)
        # {'errorMessage': 'HHHHHHHHOOOOOOOOOOGGGGGGGGEEEEEEEE',
        # 'errorType': 'HogehogeException',
        # 'requestId': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        # 'stackTrace': ['  File "/var/task/fn1.py", line 3, in handler\n'
        # '    raise HogehogeException("HHHHHHHHOOOOOOOOOOGGGGGGGGEEEEEEEE")\n']}

        print(payload_dict.get("errorMessage"))
        # HHHHHHHHOOOOOOOOOOGGGGGGGGEEEEEEEE

        print(payload_dict.get("errorType"))
        # HogehogeException

    return
