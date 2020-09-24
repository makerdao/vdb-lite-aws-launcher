# vdb-aws-launcher

AWS CDK based project for launching a VDB lite environment. Resources created:
- VPC
- RDS instance
- ECS cluster with services running vdb header sync, execute and postgraphile (accessible through an application load balancer)

![Deployment diagram](diagram/vdb-lite.png?raw=true "Deployment diagram")

### Prerequisite

For deploying to AWS, this project uses `cdk` and python (see https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html).  
Install AWS CDK running `npm install -g aws-cdk`.

### Installation
Clone repo and switch into its directory then run `./install.sh`

### Configuration
Edit `config/vdb-lite.json` and specify desired values.

| Parameter | Description |
| --- | --- |
| `AWS_REGION` | AWS region to be used for deploying vdb lite |
| `DATABASE_USER` | PostgreSQL database user |
| `DATABASE_PASSWORD` | PostgreSQL database password |
| `DATABASE_NAME` | vdb lite database name |
| `CLIENT_IPCPATH` | RPC URL to be used by vdb lite (tested with geth light node) |
| `VDB_EXECUTE_IMAGE` | Docker image used for vdb lite transformer execute service |
| `VDB_HEADER_SYNC_IMAGE` | Docker image used for vdb lite header sync service |
| `VDB_EXTRACT_DIFFS_IMAGE` | Docker image used for vdb extract diffs service * |
| `VDB_POSTGRAPHILE_IMAGE` | Docker image used for vdb lite postgraphile service |

### Deploy
Use `./deploy.sh` script to deploy vdb-lite in AWS and accept deployment steps.  
To tear down environment run `./destroy.sh`  

### Test deployment

Last deployment step will print out URL to load balancer, e.g.
```
✅  VdbPostgraphileEcsStack

Outputs:
VdbPostgraphileEcsStack.VdbPostgraphileAlbServiceLoadBalancerDNSE1507D40 = VdbPo-VdbPo-170291ZOJZ9Y7-1863118136.eu-west-2.elb.amazonaws.com
VdbPostgraphileEcsStack.VdbPostgraphileAlbServiceServiceURLFC37D1D2 = http://VdbPo-VdbPo-170291ZOJZ9Y7-1863118136.eu-west-2.elb.amazonaws.com
```

Use this query to validate deployment (replace URL with URL to load balancer)
```
curl -s \
-X POST \
-H 'Content-Type: application/json' \
-H 'Accept-Encoding:gzip' \
--data-binary '{"query":"query q { allEventLogs(last: 10) { nodes { headerByHeaderId { blockNumber } } } }"}' \
--compressed \
'http://VdbPo-VdbPo-170291ZOJZ9Y7-1863118136.eu-west-2.elb.amazonaws.com/graphql' |jq
```

### full VDB vs vdb-lite

- VDB lite is a slimmed down version of VulcanizeDB and needs just a regular JSON-RPC endpoint to work (e.g. parity, infura, etc.). It exposes events from the MakerDAO smart contracts
- The full version of VulcanizeDB includes storage diffs processing and requires a patched geth node. See https://github.com/makerdao/go-ethereum. It exposes events + storage slots + tables aggregating data structures that are distributed across several contracts (e.g. urns)
