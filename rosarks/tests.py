"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


    rosa = Deltas()

    datas = []

    for i in range(0,400):
        datas.append([datetime(2013,2,7,23,50,0) - timedelta(i), 
                      1000 - i*int(date.strftime(datetime.today(), '%m')) ])

    print rosa.delta_byweek(datas)
    print rosa.delta_bymonth(datas)
    print rosa.delta_byyear(datas)


