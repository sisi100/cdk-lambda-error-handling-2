import aws_cdk as cdk
from aws_cdk import aws_lambda

app = cdk.App()
stack = cdk.Stack(app, "test")

# タイムアウトするlambda
fn1 = aws_lambda.Function(
    stack,
    "TimeoutFunction",
    code=aws_lambda.Code.from_asset("lambdas"),
    handler="fn1.handler",
    runtime=aws_lambda.Runtime.PYTHON_3_9,
    timeout=cdk.Duration.seconds(1),
)

# fn1を同期呼び出しするlambda
fn2 = aws_lambda.Function(
    stack,
    "ExceptionHandlingFunction",
    code=aws_lambda.Code.from_asset("lambdas"),
    handler="fn2.handler",
    runtime=aws_lambda.Runtime.PYTHON_3_9,
    environment={"FUNCTION_NAME": fn1.function_name},
)
fn1.grant_invoke(fn2)

app.synth()
