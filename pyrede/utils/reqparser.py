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

def requ_parser(requirements, limit=30):
    """
    Parse the content of a requirements.txt

    Return an array of array
    Each line is an array of 1 or 3 elements
    - element 1 : package name
    - element 2 : restriction sign '==' or '>='
    - element 3 : version number
    
    """
    datas = []

    for req in requirements.split('\n'):
        data = parse_line(req.strip())
        if data is not None:
            datas.append(data)

    return datas[:limit]

def parse_line(line):

    if line.startswith('#'):
        # remove comments
        return None
    elif line.startswith('-'):
        return None
    else:
        if '==' in line:
            parts = line.split('==')
            return [str(parts[0]), '==', str(parts[1])]
        elif '>=' in line:
            parts = line.split('>=')
            return [str(parts[0]), '>=', str(parts[1])]
        elif '=<' in line:
            parts = line.split('=<')
            return [str(parts[0]), '=<', str(parts[1])]
        else:
            if line != '':
                return [str(line)]
            else:
                return None
