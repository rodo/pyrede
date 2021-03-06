# -*- coding: utf-8 -*-
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
"""
Distributions tools
"""
import logging
import requests
from celery.task import task


@task
def check_dispack_link(dispack):
    """
    Check if an url exists
    """
    user_agent = 'Pyrede bot, contact http://pyrede.quiedeville.org/about/'
    headers = {'User-agent': user_agent}

    logger.debug('check {}'.format(dispack.link))
    req = requests.get(dispack.link, headers=headers)
    dispack.valid_link = req.ok
    dispack.save()
