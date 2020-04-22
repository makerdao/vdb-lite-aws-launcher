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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from aws_cdk import (
    core,
    aws_rds as rds,
    aws_ec2 as ec2
)


class VdbRdsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, security_group: ec2.SecurityGroup,
                 config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vdb_rds_params = rds.ParameterGroup(
            self,
            id='rds-pg-vdb-cdk',
            family='postgres11',
            parameters={
                'autovacuum': '1',
                'autovacuum_work_mem': '-1',
                'autovacuum_max_workers': '3',
                'huge_pages': 'on',
                'log_min_duration_statement': '1000',
                'track_counts': '1',
                'maintenance_work_mem': '524288',
                'shared_buffers': '262144',
                'seq_page_cost': '1',
                'random_page_cost': '2',
                'min_wal_size': '512',
                'max_wal_size': '4096',
                'wal_compression': '1',
                'work_mem': '262144',
                'temp_file_limit': '10485760',
                'effective_cache_size': '786432'
            }
        )

        self.vdb_rds = rds.DatabaseInstance(
            self,
            id='VdbCdk',
            database_name=config['DATABASE_NAME'],
            instance_identifier='vdb-prod-cdk',
            master_username=config['DATABASE_USER'],
            master_user_password=core.SecretValue(value=config['DATABASE_PASSWORD']),
            port=5432,
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            engine_version='11.6',
            instance_class=ec2.InstanceType('t3.large'),
            allocated_storage=100,
            storage_encrypted=False,
            multi_az=False,
            storage_type=rds.StorageType.GP2,

            allow_major_version_upgrade=False,
            auto_minor_version_upgrade=False,
            preferred_maintenance_window='sun:02:00-sun:04:00',
            copy_tags_to_snapshot=True,
            backup_retention=core.Duration.days(7),
            preferred_backup_window='04:00-06:00',

            parameter_group=vdb_rds_params,

            vpc=vpc,
            security_groups=[security_group]
        )







