#!/usr/bin/env bash

set -e
virtualenv .env
source .env/bin/activate
cdk destroy VdbPostgraphileEcsStack
cdk destroy VdbHeaderSyncEcsStack
cdk destroy VdbExecuteEcsStack
cdk destroy VdbRdsStack
cdk destroy VdbVpcStack