# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2016 Jonathan Labéjof <jonathan.labejof@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------------------------------------------------------

"""Specification of the request interface."""

__all__ = ['Request']


class Request(object):
    """In charge of executing nodes.

    The result is saved in the attribute ``resctx``

    A request save references to nodes, context and a dispatcher."""

    __slots__ = ['dispatcher', 'nodes', 'ctx', 'resctx']

    def __init__(self, dispatcher, nodes, ctx=None, *args, **kwargs):
        """
        :param Dispatcher dispatcher: dispatcher.
        :param list nodes: nodes to execute.
        :param dict ctx: default expression execution context.
        """

        super(Request, self).__init__(*args, **kwargs)

        self.nodes = nodes
        self.ctx = ctx
        self.dispatcher = dispatcher
        self.resctx = None

    def run(self):
        """Execute this nodes.

        :rtype: dict"""

        result = None

        if self.nodes:
            self.resctx = result = self.dispatcher.run(
                nodes=self.nodes, ctx=self.ctx
            )

        return result
