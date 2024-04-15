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

const transactionTable = new aws.dynamodb.Table(
  `${projectName}-transactionTable`,
  {
    name: `${projectName}-transactionTable`,
    billingMode: "PAY_PER_REQUEST",
    hashKey: "id",
    attributes: [
      {
        name: "id",
        type: "S",
      },
    ],
  }
);

const accountTable = new aws.dynamodb.Table(`${projectName}-accountTable`, {
  name: `${projectName}-accountTable`,
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
      TRANSACTION_TABLE_NAME: transactionTable.name,
      TRANSACTION_TABLE_ARN: transactionTable.arn,
      ACCOUNT_TABLE_NAME: accountTable.name,
      ACCOUNT_TABLE_ARN: accountTable.arn,
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
export const transactionTableArn = transactionTable.arn;
export const accountTableArn = accountTable.arn;
export const bucketDomainName = s3Bucket.bucketDomainName;
export const lambdaFnArn = lambdaFn.arn;
