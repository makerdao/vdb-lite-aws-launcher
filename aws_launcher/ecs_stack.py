# ecs_stack.py
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
from aws_cdk import (
    core,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_ecs_patterns as ecs_patterns
)


class VdbExecuteEcsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, security_group: ec2.SecurityGroup, rds: rds.DatabaseInstance,
                 config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.cluster = ecs.Cluster(
            self,
            "VdbEcsStackCluster",
            cluster_name="VdbCluster",
            vpc=vpc
        )

        self.cluster.add_capacity("DefaultAutoScalingGroup",
                                  instance_type=ec2.InstanceType("t2.xlarge"),
                                  vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
                                  max_capacity=1)

        execute_task_definition = ecs.FargateTaskDefinition(
            self,
            "ExecuteTaskDef",
            cpu=1024,
            memory_limit_mib=2048
        )

        execute_container = execute_task_definition.add_container(
            "execute",
            image=ecs.ContainerImage.from_registry(name=config['VDB_EXECUTE_IMAGE']),
            entry_point=[
                "sh",
                "-c"
            ],
            command=[
                "./startup_script.sh"
            ],
            logging=ecs.LogDrivers.aws_logs(stream_prefix="VdbExecuteLogs"),
            environment={
                "DATABASE_USER": config['DATABASE_USER'],
                "DATABASE_PASSWORD": config['DATABASE_PASSWORD'],
                "DATABASE_NAME": config['DATABASE_NAME'],
                "DATABASE_PORT": rds.db_instance_endpoint_port,
                "DATABASE_HOSTNAME": rds.db_instance_endpoint_address,
                "STORAGEDIFFS_SOURCE": "geth",
                "CLIENT_IPCPATH": config['CLIENT_IPCPATH']
            }
        )

        ecs.FargateService(
            self, "VdbExecuteService",
            cluster=self.cluster,
            task_definition=execute_task_definition,
            service_name="VdbExecuteService",
            security_group=security_group
        )


class VdbHeaderSyncEcsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, cluster: ecs.Cluster, security_group: ec2.SecurityGroup,
                 rds: rds.DatabaseInstance, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        header_sync_task_definition = ecs.FargateTaskDefinition(
            self,
            "HeaderSyncTaskDef",
            cpu=1024,
            memory_limit_mib=2048
        )

        header_sync_container = header_sync_task_definition.add_container(
            "header-sync",
            image=ecs.ContainerImage.from_registry(name=config['VDB_HEADER_SYNC_IMAGE']),
            entry_point=[
                "sh",
                "-c"
            ],
            command=[
                "./startup_script.sh"
            ],
            logging=ecs.LogDrivers.aws_logs(stream_prefix="VdbHeaderSyncLogs"),
            environment={
                "DATABASE_USER": config['DATABASE_USER'],
                "DATABASE_PASSWORD": config['DATABASE_PASSWORD'],
                "DATABASE_NAME": config['DATABASE_NAME'],
                "DATABASE_PORT": rds.db_instance_endpoint_port,
                "DATABASE_HOSTNAME": rds.db_instance_endpoint_address,
                "STARTING_BLOCK_NUMBER": "8928152",
                "CLIENT_IPCPATH": config['CLIENT_IPCPATH']
            }
        )

        ecs.FargateService(
            self, "VdbHeaderSyncService",
            cluster=cluster,
            task_definition=header_sync_task_definition,
            service_name="VdbHeaderSyncService",
            security_group=security_group
        )

class VdbExtractDiffsEcsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, cluster: ecs.Cluster, security_group: ec2.SecurityGroup,
                 rds: rds.DatabaseInstance, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        extract_diffs_task_definition = ecs.FargateTaskDefinition(
            self,
            "ExtractDiffsTaskDef",
            cpu=1024,
            memory_limit_mib=2048
        )

        extract_diffs_container = extract_diffs_task_definition.add_container(
            "extract-diffs",
            image=ecs.ContainerImage.from_registry(name=config['VDB_EXTRACT_DIFFS_IMAGE']),
            entry_point=[
                "sh",
                "-c"
            ],
            command=[
                "./startup_script.sh"
            ],
            logging=ecs.LogDrivers.aws_logs(stream_prefix="VdbExtractDiffsLogs"),
            environment={
                "DATABASE_USER": config['DATABASE_USER'],
                "DATABASE_PASSWORD": config['DATABASE_PASSWORD'],
                "DATABASE_NAME": config['DATABASE_NAME'],
                "DATABASE_PORT": rds.db_instance_endpoint_port,
                "DATABASE_HOSTNAME": rds.db_instance_endpoint_address,
                "CLIENT_IPCPATH": config['CLIENT_IPCPATH'],
                "STORAGEDIFFS_SOURCE": "geth"
            }
        )

        ecs.FargateService(
            self, "VdbHExtractDiffsService",
            cluster=cluster,
            task_definition=extract_diffs_task_definition,
            service_name="VdbExtractDiffsService",
            security_group=security_group
        )

class VdbPostgraphileEcsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, cluster: ecs.Cluster, rds: rds.DatabaseInstance,
                 config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        postgraphile_task_image_options = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_registry(name=config['VDB_POSTGRAPHILE_IMAGE']),
            container_name="vdb-postgraphile",
            container_port=5000,
            environment={
                "SCHEMAS": "api,maker,public",
                "DATABASE_URL": f"postgresql://{config['DATABASE_USER']}:{config['DATABASE_PASSWORD']}"
                f"@{rds.db_instance_endpoint_address}:{rds.db_instance_endpoint_port}/{config['DATABASE_NAME']}",
            }
        )

        ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "VdbPostgraphileAlbService",
            service_name="VdbPostgraphileService",
            cluster=cluster,
            task_image_options=postgraphile_task_image_options,
            cpu=1024,
            memory_limit_mib=2048
        )
