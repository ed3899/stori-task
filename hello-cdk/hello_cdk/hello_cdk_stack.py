import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_s3_notifications as s3Notifications,
)

class HelloCdkStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dynamodb_table = cdk.aws_dynamodb.TableV2(
            self,
            "MyTable",
            partition_key=dynamodb.Attribute(
                name="Id", type=dynamodb.AttributeType.NUMBER
            ),
            billing=dynamodb.Billing.on_demand(),
        )

        hello_world_function = cdk.aws_lambda.Function(
            self,
            "HelloWorldFunction",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_12,
            code=cdk.aws_lambda.Code.from_asset("lambda"),
            handler="hello.lambda_handler",
            environment={"DYNAMO_DB_TABLE_NAME": dynamodb_table.table_name},
        )

        bucket = s3.Bucket(
            self,
            "MyBucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3Notifications.LambdaDestination(hello_world_function),  # type: ignore
        )
