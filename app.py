#!/usr/bin/env python3
import json

from aws_cdk.core import Construct, App

from aws_launcher.rds_stack import VdbRdsStack
from aws_launcher.ecs_stack import VdbExecuteEcsStack, VdbHeaderSyncEcsStack, VdbPostgraphileEcsStack
from aws_launcher.vpc_stack import VdbVpcStack


class VdbLiteService(Construct):

    def __init__(self, scope: Construct, id: str):

        super().__init__(scope, id)

        env_setup = {'region': 'us-east-1'}

        with open(f'config/vdb-lite.json', 'r') as file:
            config = json.load(file)

        vpc_stack = VdbVpcStack(app, "VdbVpcStack", env=env_setup)
        rds_stack = VdbRdsStack(app, "VdbRdsStack", vpc_stack.vpc, vpc_stack.vdb_security_group,
                                config=config, env=env_setup)
        execute_rds_stack = VdbExecuteEcsStack(app, "VdbExecuteEcsStack",
                                               vpc=vpc_stack.vpc,
                                               security_group=vpc_stack.vdb_security_group,
                                               rds=rds_stack.vdb_rds,
                                               config=config,
                                               env=env_setup)
        headersync_rds_stack = VdbHeaderSyncEcsStack(app, "VdbHeaderSyncEcsStack",
                                                     cluster=execute_rds_stack.cluster,
                                                     security_group=vpc_stack.vdb_security_group,
                                                     rds=rds_stack.vdb_rds,
                                                     config=config,
                                                     env=env_setup)
        postgraphile_stack = VdbPostgraphileEcsStack(app, "VdbPostgraphileEcsStack",
                                                     cluster=execute_rds_stack.cluster,
                                                     rds=rds_stack.vdb_rds,
                                                     config=config,
                                                     env=env_setup)


app = App()
VdbLiteService(app, "vdb")

app.synth()

