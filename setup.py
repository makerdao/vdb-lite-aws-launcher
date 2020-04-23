# setup.py
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
import setuptools

setuptools.setup(
    name="vdb-lite-aws-launcher",
    version="0.0.1",

    description="vdb-lite-aws-launcher",

    author="author",

    package_dir={"": "vdb-lite-aws-launcher"},
    packages=setuptools.find_packages(where="vdb-lite-aws-launcher"),

    install_requires=[
        "aws-cdk.core",
    ],

    python_requires=">=3.6",
)
