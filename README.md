# Stori Task

This is task designed to test my skills while applying for a Sr. Engineer position at Stori

## Requirements

- Node >= 20.12.1
- Pulumi >= 3.112.0
- Docker >= 24.0.9-1
- AWS

## Setup

1. Create an account at [pulumi](https://www.pulumi.com/docs/get-started/) and get a [token](https://www.pulumi.com/docs/pulumi-cloud/access-management/access-tokens/#personal-access-tokens).
2. Create an [environment](https://www.pulumi.com/docs/esc/). This is the environment where AWS credentials are stored instead of locally.
3. Connect your environment with [aws](https://www.pulumi.com/docs/esc/environments/#using-secrets-providers-and-oidc)
4. At `pulumi/` run `pulumi up -y`

## Try

1. Upload the `transactions.csv` to the created S3 bucket
2. Go to your lambdas at the aws console and then look for the cloudwatch group of that lambda
3. You should see the result output

## System Design

