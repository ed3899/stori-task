import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

const repository = new awsx.ecr.Repository("ecrRepository", {
  forceDelete: true,
});

const image = new awsx.ecr.Image("ecrImage", {
  repositoryUrl: repository.url,
  context: "./lambdas/process_transaction",
  dockerfile: "./lambdas/process_transaction/Dockerfile",
});

const dynamoDbTable = new aws.dynamodb.Table("dynamoDBTable", {
  name: "my-dynamo-db-table",
  billingMode: "PAY_PER_REQUEST",
  hashKey: "id",
  attributes: [
    {
      name: "id",
      type: "S",
    },
  ],
});

const docsHandlerRole = new aws.iam.Role("docsHandlerRole", {
  assumeRolePolicy: {
    Version: "2012-10-17",
    Statement: [
      {
        Action: "sts:AssumeRole",
        Principal: {
          Service: "lambda.amazonaws.com",
        },
        Effect: "Allow",
      },
    ],
  },
});

new aws.iam.RolePolicyAttachment("zipTpsReportsFuncRoleAttach", {
  role: docsHandlerRole,
  policyArn: aws.iam.ManagedPolicies.AWSLambdaExecute,
});

const lambdaLayer = new aws.lambda.LayerVersion("lambdaLayer", {
  layerName: "myLambdaLayer",
  code: new pulumi.asset.AssetArchive({
    config: new pulumi.asset.FileArchive(
      "./lambdas/process_transaction/process_transaction_lambda_venv/lib"
    ),
  }),
});

const lambdaFn = new aws.lambda.Function("docsHandlerFunc", {
  runtime: "python3.12",
  role: docsHandlerRole.arn,
  handler: "main.handler",
  code: new pulumi.asset.AssetArchive({
    ".": new pulumi.asset.FileArchive("./lambdas/process_transaction"),
  }),
  environment: {
    variables: {
      DYNAMODB_TABLE_NAME: dynamoDbTable.name,
      DYNAMODB_TABLE_ARN: dynamoDbTable.arn,
    },
  },
  layers: [lambdaLayer.arn],
});

const s3Bucket = new aws.s3.Bucket("s3Bucket", {
  bucket: "my-s3-bucket",
});

s3Bucket.onObjectCreated("docsHandler", lambdaFn);

export const repoUrl = repository.url;
export const dynamoDbTableArn = dynamoDbTable.arn
export const bucketDomainName = s3Bucket.bucketDomainName
export const lambdaFnArn = lambdaFn.arn

