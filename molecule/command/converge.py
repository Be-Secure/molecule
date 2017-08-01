#  Copyright (c) 2015-2017 Cisco Systems, Inc.
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

import click

import molecule.command
from molecule import logger
from molecule import scenarios
from molecule.command import base

LOG = logger.get_logger(__name__)


class Converge(base.Base):
    """
    Target the default scenario:

    >>> molecule converge

    Targeting a specific scenario:

    >>> molecule converge --scenario-name foo

    Executing with `debug`:

    >>> molecule --debug converge
    """

    def execute(self):
        """
        Execute the actions necessary to perform a `molecule converge` and
        returns None.

        :return: None
        """
        self._config.provisioner.converge()
        self._config.state.change_state('converged', True)


@click.command()
@click.pass_context
@click.option(
    '--scenario-name',
    '-s',
    default='default',
    help='Name of the scenario to target. (default)')
def converge(ctx, scenario_name):  # pragma: no cover
    """ Use a provisioner to configure instances (create, converge). """
    args = ctx.obj.get('args')
    command_args = {
        'subcommand': __name__,
    }

    s = scenarios.Scenarios(
        base.get_configs(args, command_args), scenario_name)
    for scenario in s.all:
        for sequence in scenario.converge_sequences:
            s.print_sequence_info(scenario, sequence)
            command_module = getattr(molecule.command, sequence)
            command = getattr(command_module, sequence.capitalize())
            command(scenario.config).execute()
