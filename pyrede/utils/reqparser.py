# -*- coding: utf-8 -*-  pylint: disable-msg=R0801
#
# Copyright (c) 2013 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

def requ_parser(requirements):

    datas = []

    for req in requirements.split('\n'):
        data = parse_line(req.strip())
        if data is not None:
            datas.append(data)

    return datas

def parse_line(line):

    if line.startswith('#'):
        # remove comments
        return None
    elif line.startswith('-'):
        return None
    else:
        if '==' in line:
            parts = line.split('==')
            return [parts[0], '==', parts[1]]
        elif '>=' in line:
            parts = line.split('>=')
            return [parts[0], '>=', parts[1]]
        else:
            if line != '':
                return line
            else:
                return None