#!/usr/bin/env bash

set -e
virtualenv .env
source .env/bin/activate
cdk deploy VdbVpcStack
cdk deploy VdbRdsStack
cdk deploy VdbExecuteEcsStack
cdk deploy VdbHeaderSyncEcsStack
cdk deploy VdbPostgraphileEcsStack