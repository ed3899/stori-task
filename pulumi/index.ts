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

const transactionTableBatchWritePolicy = new aws.iam.Policy(
  `${projectName}-transactionTableBatchWritePolicy`,
  {
    policy: {
      Id: "SomeRandomId123",
      Version: "2012-10-17",
      Statement: [
        {
          Effect: "Allow",
          Action: "dynamodb:BatchWriteItem",
          Resource: transactionTable.arn,
        },
      ],
    },
  },
  {
    dependsOn: [transactionTable],
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

const accountTableWritePolicy = new aws.iam.Policy(
  `${projectName}-accountTableWritePolicy`,
  {
    policy: {
      Id: "SomeRandomIdas12232",
      Version: "2012-10-17",
      Statement: [
        {
          Effect: "Allow",
          Action: "dynamodb:PutItem",
          Resource: accountTable.arn,
        },
      ],
    },
  },
  {
    dependsOn: [accountTable],
  }
);

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

const lambdaRolePolicyAttachmentTransacTable = new aws.iam.RolePolicyAttachment(
  `${projectName}-roleAttachment-transactionsTable`,
  {
    role: docsHandlerRole,
    policyArn: transactionTableBatchWritePolicy.arn,
  }
);

const lambdaRolePolAttachAccountTable = new aws.iam.RolePolicyAttachment(
  `${projectName}-roleAttachment-accountsTable`,
  {
    role: docsHandlerRole,
    policyArn: accountTableWritePolicy.arn,
  }
);

const lambdaRolePolicyAttachmentExecute = new aws.iam.RolePolicyAttachment(
  `${projectName}-roleAttachment-execute`,
  {
    role: docsHandlerRole,
    policyArn: aws.iam.ManagedPolicy.AWSLambdaExecute,
  }
);

const lambdaRolePolicyAttachmentBasicExecute = new aws.iam.RolePolicyAttachment(
  `${projectName}-roleAttachment-basicExecute`,
  {
    role: docsHandlerRole,
    policyArn: aws.iam.ManagedPolicy.AWSLambdaBasicExecutionRole,
  }
);

const s3Bucket = new aws.s3.Bucket(`${projectName}-s3Bucket-18723873787`, {
  forceDestroy: true,
});

const fileObject = new aws.s3.BucketObject(`${projectName}-storiLogo`, {
  bucket: s3Bucket,
  key: "stori_logo.jpg",
  source: new pulumi.asset.FileAsset("./stori_logo.jpg"),
});

const publicAccessBlock = new aws.s3.BucketPublicAccessBlock(
  "public-access-block",
  {
    bucket: s3Bucket.id,
    blockPublicAcls: false,
  }
);

const bucketPolicy = new aws.s3.BucketPolicy(
  `${projectName}-s3BucketPolicy`,
  {
    bucket: s3Bucket.id,
    policy: s3Bucket.arn.apply(s3BucketArn => {
      const _policy = docsHandlerRole.arn.apply(docsHandlerRoleArn =>
        JSON.stringify({
          Id: "ReadObject",
          Version: "2012-10-17",
          Statement: [
            {
              Sid: "AllowGetObject",
              Effect: "Allow",
              Principal: {
                AWS: docsHandlerRoleArn,
              },
              Action: "s3:GetObject",
              Resource: `${s3BucketArn}/*`, // policy refers to bucket name explicitly
            },
          ],
        })
      );

      return _policy;
    }),
  },
  {dependsOn: [docsHandlerRole, lambdaRolePolicyAttachmentExecute, s3Bucket]}
);

const lambdaFn = new aws.lambda.Function(`${projectName}-docsHandlerFunc`, {
  role: docsHandlerRole.arn,
  environment: {
    variables: {
      TRANSACTION_TABLE_NAME: transactionTable.name,
      TRANSACTION_TABLE_ARN: transactionTable.arn,
      ACCOUNT_TABLE_NAME: accountTable.name,
      ACCOUNT_TABLE_ARN: accountTable.arn,
      S3_BUCKET_NAME: s3Bucket.bucket,
    },
  },
  imageUri: image.imageUri,
  packageType: "Image",
  timeout: 20,
});

s3Bucket.onObjectCreated("docsHandler", lambdaFn);

export const repoUrl = repository.url;
export const transactionTableArn = transactionTable.arn;
export const accountTableArn = accountTable.arn;
export const bucketDomainName = s3Bucket.bucketDomainName;
export const lambdaFnArn = lambdaFn.arn;
