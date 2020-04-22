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
    aws_ec2 as ec2
)


class VdbVpcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            id="VdbVPCCdk",
            cidr="172.15.0.0/21",
            enable_dns_support=True,
            max_azs=2,
            subnet_configuration=
            [
                ec2.SubnetConfiguration(
                    name="public-vdb-cdk-net",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="private-vdb-cdk-net",
                    subnet_type=ec2.SubnetType.PRIVATE,
                    cidr_mask=24
                )
            ]
        )

        self.vdb_security_group = ec2.SecurityGroup(
            self,
            id="VdbRdsCdkSecurityGroup",
            security_group_name="vdb-cdk-sg",
            vpc=self.vpc
        )

        self.vdb_security_group.add_ingress_rule(ec2.Peer.ipv4("172.15.0.0/24"), ec2.Port.tcp(5000), "allow access from the world")
        self.vdb_security_group.add_ingress_rule(ec2.Peer.ipv4("172.15.1.0/24"), ec2.Port.tcp(5000), "allow access from the world")

        self.vdb_security_group.add_ingress_rule(ec2.Peer.ipv4("172.15.2.0/24"), ec2.Port.tcp(5432), "allow internal access")
        self.vdb_security_group.add_ingress_rule(ec2.Peer.ipv4("172.15.3.0/24"), ec2.Port.tcp(5432), "allow internal access")







