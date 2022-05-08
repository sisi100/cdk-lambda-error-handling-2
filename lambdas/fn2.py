import json
import os
from pprint import pprint

import boto3


def handler(event, context):
    """lambdaを同期呼び出しするlambda"""

    # 同期呼び出し
    client = boto3.client("lambda")
    response = client.invoke(FunctionName=os.getenv("FUNCTION_NAME"))

    # こんなレスポンスが返ってくる。Lambdaで例外を出したときとレスポンスは変わらない
    pprint(response)
    # {'ExecutedVersion': '$LATEST',
    # 'FunctionError': 'Unhandled',
    # 'Payload': <botocore.response.StreamingBody object at 0x7ff63f9e3790>,
    # 'ResponseMetadata': {'HTTPHeaders': {'connection': 'keep-alive',
    # 'content-length': '114',
    # 'content-type': 'application/json',
    # 'date': 'Sun, 08 May 2022 06:08:58 GMT',
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
        print(payload_dict)
        # {'errorMessage': '2022-05-08T06:11:32.690Z xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx Task timed out after 1.00 seconds'}

        print(payload_dict.get("errorMessage"))
        # 2022-05-08T06:08:58.507Z 2xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx Task timed out after 1.00 seconds

        print(payload_dict.get("errorType"))
        # None

    return
