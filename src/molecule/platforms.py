#  Copyright (c) 2015-2018 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
"""PLatforms Module."""

import logging

from molecule import util

LOG = logging.getLogger(__name__)


class Platforms(object):
    """
    Platforms define the instances to be tested, and the groups to which the \
    instances belong.

    ``` yaml

        platforms:
          - name: instance-1
    ```

    Multiple instances can be provided.

    ``` yaml
        platforms:
          - name: instance-1
          - name: instance-2
    ```

    Mapping instances to groups.  These groups will be used by the Provisioner_
    for orchestration purposes.

    ``` yaml
        platforms:
          - name: instance-1
            groups:
              - group1
              - group2
    ```

    Children allow the creation of groups of groups.

    ``` yaml
        platforms:
          - name: instance-1
            groups:
              - group1
              - group2
            children:
              - child_group1
    ```
    """

    def __init__(self, config, parallelize_platforms=False, platform_name=None):
        """
        Initialize a new platform class and returns None.

        :param config: An instance of a Molecule config.
        :param parallelize_platforms: Parallel mode. Default is False.
        :param platform_name: One platform to target only, defaults to None.
        :return: None
        """
        if platform_name:
            config.config["platforms"] = util._filter_platforms(
                config.config, platform_name
            )
        if parallelize_platforms:
            config.config["platforms"] = util._parallelize_platforms(
                config.config, config._run_uuid
            )
        self._config = config

    @property
    def instances(self):
        return self._config.config["platforms"]
