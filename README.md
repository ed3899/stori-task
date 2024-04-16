# Stori Task

This is task designed to test Eduardo Alfredo Casanova Lope skills while applying for a Sr. Engineer position at Stori

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

### Picking the right tooling

The first step consisted on picking the right language, either Python or Go.

Python was picked because the problem at hand seemed to be more on the data processing end of things. The problem's pattern seemed to be more high level.

Pandas was picked as the core library for taking on the task. It is a library with a mature ecosystem, production ready features and C bindings that may help us with performance.

Although high performance may be an issue later down the road, assuming all things have been tried already (i.e worker pools, etc), the root of all evil is pre-optimization. We should focus first on getting it right, rather than getting it fast.

Go may be an amazing language with easy to understand and to use concurrency patterns (i.e fan-it, fan-out, pipelines, channels, routines), but it was not initially designed with data processing in mind. It's zen consist on simple control over low-level features. Nonetheless, it has its place once you start needing a bulldozer for heavy data processing where the patterns may already be clear enough.
