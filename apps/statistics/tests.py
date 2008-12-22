import unittest
import urllib
from django.test.client import *
from django.contrib.auth.models import User
from django.utils.http import urlencode
from tracker.models import Slip, TimeSlice
from teams.models import Team
from statistics.colour import colour
import datetime
from tracker.tests import RESTClient
from django.test import TestCase
from exceptions import ImportError
try:
    import json
except ImportError:
    import simplejson as json


class StatisticsRESTActionsTestCase(TestCase):
    fixtures = ['auth.json','slip.json', 'slice.json', 'team.json']

    def setUp(self):
        self.client = RESTClient()

    # note, this test is set to test an entire year for all 6 test users, so it can take a little while for the test to run.
    def testUserWeekView(self):
        for pk in range(2,7):
            user = User.objects.get(pk=pk)
            for week in range(1,53):
                year = 2008
                # Before we log in, we should be redirected to the login page.
                response = self.client.get('/statistics/user/%s/year/%s/week/%s/' % (user.id, year, week))
                self.failUnlessEqual(response.status_code, 302)
        
                 # Then log in
                response = self.client.post('/accounts/login/',
                                            {'username': user.username, 'password': 'pass'})
                # TODO: Properly check if we're logged in instead of just checking for redirect.
                self.failUnlessEqual(response.status_code, 302)
        
                # Test to see if access to a different user's statistic is denied:
                response = self.client.get('/statistics/user/%s/year/%s/week/%s/' % (user.id-1, year, week))
                self.failUnlessEqual(response.status_code, 403)
        
                # view the data source:
                response = self.client.get('/statistics/data/user/%s/year/%s/week/%s/' % (user.id, year, week))
        
                # converting the data in the content from json to python dictionaries and lists
                json_content = json.loads(response.content)
        
                # test to see if the value is shown as is should. This work by getting the value(s) from the fixture DB and comparing to the json_content
                # first get the timetimes and put the slip into the dict if it's not there:
                slice_set = user.timeslices.filter(week_number=week)
                slip_dict = {}
                for slic in slice_set:
                    if not slip_dict.has_key(slic.begin.date()):
                        slip_dict[slic.begin.date()] = [slic.slip]
                    else:
                        if slic.slip not in slip_dict[slic.begin.date()]:
                             slip_dict[slic.begin.date()].append(slic.slip)
        
                start_date = datetime.date(year, 1, 1) + datetime.timedelta(days = (week-2)*7)
                while start_date.isocalendar()[1] != week:
                    start_date += datetime.timedelta(days=1)
                                
                # make a list of all the dates for the chosen week:
                end_date = start_date + datetime.timedelta(days=6)
                w_date = start_date
                all_dates_list = []
                while w_date != end_date + datetime.timedelta(days=1):
                    all_dates_list.append(w_date)
                    w_date += datetime.timedelta(days=1)
    
                # iterate over the dates, if the date is not in the slip_dict, the value should be [0].
                # If the date is in the slip_dict, the value should be the slips display_days_time (rounded to 1 dec).    
                for date in all_dates_list:
                    if date not in slip_dict.keys():
                        self.failUnlessEqual(json_content['elements'][0]['values'][date.weekday()], [0])
                    else:
                        for number in range(len(slip_dict[date])):
                            self.failUnlessEqual(json_content['elements'][0]['values'][date.weekday()][number]['val'], round(slip_dict[date][number].display_days_time(date), 1))
        
                # test to see if graph type is bar_stack:
                self.failUnlessEqual(json_content['elements'][0]['type'], 'bar_stack')
        
                # test to see if the labels on the x-axis is correct
                # it sould be monday-sunday which dec 1-7 also is.
                if week == 1:
                    pass
                    for numb in range(7-start_date.weekday()):
                        self.failUnlessEqual(json_content['x_axis']['labels']['labels'][numb], datetime.datetime.strftime(datetime.datetime(2008,12, numb + 1 + start_date.weekday()), '%A'))
                else:
                    for numb in range(7):
                        self.failUnlessEqual(json_content['x_axis']['labels']['labels'][numb], datetime.datetime.strftime(datetime.datetime(2008,12,numb+1), '%A'))
                
                self.failUnlessEqual(json_content['title']['text'], '%s Week %s' % (user.username, week))
                    
                # logout when finished testing a user, to create simelar starting points for every user.
                self.client.get('/accounts/logout/')
