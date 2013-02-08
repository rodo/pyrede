#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import unittest
import urllib2
from datetime import datetime
from datetime import timedelta
from datetime import date


class Deltas():
    """Main parts"""
    def delta_byweek(self, datas):
        """Consolidate datas by week

        datas : Array(2)
          - datetime
          - value
        """
        code = "delta_week"
        timecode = '%Y%U'
        return self.delta_period(datas, code, timecode)

    def delta_bymonth(self, datas):
        """Consolidate datas by month

        datas : Array(2)
          - datetime
          - value
        """
        code = "delta_month"
        timecode = '%Y%m'
        return self.delta_period(datas, code, timecode)

    def delta_byyear(self, datas):
        """Consolidate datas by year

        datas : Array(2)
          - datetime
          - value
        """
        code = "delta_year"
        timecode = '%Y'
        return self.delta_period(datas, code, timecode)

    def delta_period(self, datas, code, timecode):
        """Consolidate datas by period

        datas : Array(2)
          - datetime
          - value
        code : string
        timecode : string

        Return : dict
        """
        datas.sort()
        old = datas[0]
        result = {}
        delta = 0
        for data in datas:
            if (date.strftime(data[0], timecode) == date.strftime(old[0], timecode)):
                delta = delta + (data[1] - old[1])
                key = '{}_{}'.format(code, date.strftime(data[0], timecode))
                result[key] = delta
            else:
                delta = delta + (data[1] - old[1])
                key = '{}_{}'.format(code, date.strftime(old[0], timecode))
                result[key] = delta
                delta = 0
            old=data
        return result



if __name__ == '__main__':
    rosa = Rosarks()

    datas = []

    for i in range(0,400):
        datas.append([datetime(2013,2,7,23,50,0) - timedelta(i), 
                      1000 - i*int(date.strftime(datetime.today(), '%m')) ])

    print rosa.delta_byweek(datas)
    print rosa.delta_bymonth(datas)
    print rosa.delta_byyear(datas)


