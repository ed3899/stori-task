import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

const projectName = "storiTaskByEdca3899";

const repository = new awsx.ecr.Repository(`${projectName}-ecrRepo`, {
  forceDelete: true,
});

const image = new awsx.ecr.Image(`${projectName}-ecrImage`, {
  repositoryUrl: repository.url,
  context: "./lambdas/process_transaction",
  dockerfile: "./lambdas/process_transaction/Dockerfile",
});

const dynamoDbTable = new aws.dynamodb.Table(`${projectName}-dynamoDbTable`, {
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

const docsHandlerRole = new aws.iam.Role(`${projectName}-docsHandlerRole`, {
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

new aws.iam.RolePolicyAttachment(`${projectName}-roleAttachment`, {
  role: docsHandlerRole,
  policyArn: aws.iam.ManagedPolicies.AWSLambdaExecute,
});

const lambdaFn = new aws.lambda.Function(`${projectName}-docsHandlerFunc`, {
  role: docsHandlerRole.arn,
  environment: {
    variables: {
      DYNAMODB_TABLE_NAME: dynamoDbTable.name,
      DYNAMODB_TABLE_ARN: dynamoDbTable.arn,
    },
  },
  imageUri: image.imageUri,
  packageType: "Image",
});

const s3Bucket = new aws.s3.Bucket(`${projectName}-s3Bucket-18723873787`, {
  forceDestroy: true,
});

s3Bucket.onObjectCreated("docsHandler", lambdaFn);

export const repoUrl = repository.url;
export const dynamoDbTableArn = dynamoDbTable.arn;
export const bucketDomainName = s3Bucket.bucketDomainName;
export const lambdaFnArn = lambdaFn.arn;
