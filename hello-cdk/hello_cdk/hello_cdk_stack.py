import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_s3 as s3


class HelloCdkStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hello_world_function = cdk.aws_lambda.Function(
            self,
            "HelloWorldFunction",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_12,
            code=cdk.aws_lambda.Code.from_asset("lambda"),
            handler="hello.lambda_handler",
        )

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "HelloCdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
