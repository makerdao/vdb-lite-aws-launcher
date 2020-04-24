#!/usr/bin/env python3
# app.py
# Copyright (C) 2020 Maker Ecosystem Growth Holdings, INC.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import json

from aws_cdk.core import Construct, App

from aws_launcher.rds_stack import VdbRdsStack
from aws_launcher.ecs_stack import VdbExecuteEcsStack, VdbHeaderSyncEcsStack, VdbPostgraphileEcsStack
from aws_launcher.vpc_stack import VdbVpcStack


class VdbLiteService(Construct):

    def __init__(self, scope: Construct, id: str):

        super().__init__(scope, id)

        with open(f'config/vdb-lite.json', 'r') as file:
            config = json.load(file)

        env_setup = {'region': config['AWS_REGION']}

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

