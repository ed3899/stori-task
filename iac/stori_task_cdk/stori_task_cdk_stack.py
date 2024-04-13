import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_s3_notifications as s3Notifications,
    aws_lambda as lambda_,
)


class StoriTaskStack(cdk.Stack):

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

        layer = cdk.aws_lambda.LayerVersion(
            self,
            code=lambda_.Code.from_asset("lambda/python.zip"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_12],
            id="s3FileProcessingLayer"
        )

        s3_file_processing_lambda = lambda_.Function(
            self,
            "s3FileProcessing",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset("lambda"),
            handler="process_transaction.lambda_handler",
            environment={"DYNAMO_DB_TABLE_NAME": dynamodb_table.table_name},
            layers=[layer],
        )

        bucket = s3.Bucket(
            self,
            "MyBucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3Notifications.LambdaDestination(s3_file_processing_lambda),  # type: ignore
        )
