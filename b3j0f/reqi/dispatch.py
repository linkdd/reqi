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

"""Specification of the dispatcher interface."""

from b3j0f.utils.version import OrderedDict

from .request.core import Request


class Dispatcher(object):
    """In charge of dispatching requests."""

    def __init__(self, systems, *args, **kwargs):
        """
        :param dict systems: systems by name to handle.
        """

        super(Dispatcher, self).__init__(*args, **kwargs)

        self.systems = systems

        self._systemsperschema = OrderedDict()
        self._schemaspersystem = OrderedDict()
        self._schemasbyname = OrderedDict()
        self._schemasperprop = OrderedDict()

        self._loadsystems()

    def _loadsystems(self):
        """Load this systems in referencing sys name by schema and reciprocally.
        """

        self._systemsperschema.clear()
        self._schemaspersystem.clear()
        self._schemasbyname.clear()
        self._schemasperprop.clear()

        for sysn in self.systems:

            system = self.systems[sysn]

            for schema in system.schemas:

                schn = schema.name

                self._schemasbyname[schn] = schema
                self._schemaspersystem.setdefault(sysn, []).append(schn)
                self._systemsperschema.setdefault(schn, []).append(sysn)

                for propn in schema:

                    self._schemasperprop.setdefault(propn, []).append(schn)

    def getsystemswithschemas(
            self, system=None, schema=None, prop=None,
            defsystems=None, defschemas=None
    ):
        """Get systems and schemas corresponding to input system, schema and
        prop if not given.

        :param str system: system name.
        :param str schema: schema name.
        :param str prop: property name.
        :param list defsystems: default system names.
        :param list defschemas: default schema names.
        :return: corresponding (systems, schemas)
        :rtype: tuple
        """

        if defsystems is None:

            if defschemas is None:
                defsystems = list(self._schemaspersystem)

            else:
                defsystems = [
                    _system
                    for _schema in defschemas
                    for _system in self._systemsperschema[_schema]
                ]

        if defschemas is None:

            defschemas = [
                _schema
                for _system in defsystems
                for _schema in self._schemaspersystem[_system]
            ]

        if system is not None:
            systems = [system]

        if schema is not None:
            schemas = [schema]

        if prop is None:

            if schema is None:

                if system is None:
                    systems = defsystems
                    schemas = defschemas

                else:
                    schemas = [
                        schema for schema in self._schemaspersystem[system]
                        if schema in defschemas
                    ]

            else:
                if system is None:
                    systems = [
                        system for system in self._systemsperschema[schema]
                        if system in defsystems
                    ]

        else:

            if schema is None:

                if system is None:
                    schemas = [
                        schema
                        for schema in self._schemasperprop[prop]
                        if schema in defschemas
                    ]
                    systems = [
                        system
                        for schema in schemas
                        for system in self._systemsperschema[schema]
                        if system in defsystems
                    ]

                else:
                    schemas = [
                        schema
                        for schemas in self._schemasperprop[prop]
                        if schema in self._schemaspersystem[system]
                        and schema in defschemas
                    ]

            else:

                if system is None:
                    systems = [
                        system for system in self._systemsperschema[schema]
                        if system in defsystems
                    ]

        _removeoccurences(systems)
        _removeoccurences(schemas)

        return systems, schemas

    def queue(self):
        """Create a new Request Queue.

        :rtype: RequestQueue"""

        return RequestQueue(dispatcher=self)


def _removeoccurences(l):
    """Ensure to have one item value in removing multi-occurences from the end
    of the input list.

    :param list l: list from where remove multi-occurences.
    """

    if len(l) != len(set(l)):
        l.reverse()

        for item in list(l):
            for _ in range(1, l.count(item)):
                l.remove(item)

        l.reverse()
