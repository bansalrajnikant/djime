import random
import time
import unittest
import urllib
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import *
from django.utils.http import urlencode
from djime.models import Slip, TimeSlice
from djime.tests import RESTClient
from exceptions import ImportError
from statistics.colour import colour
from teams.models import Team
import datetime
try:
    import json
except ImportError:
    import simplejson as json

class StatisticsRESTActionsTestCase(TestCase):
    fixtures = ['auth.json','slip.json', 'slice.json', 'team.json']

    def setUp(self):
        self.client = RESTClient()

    # note, the User/Team tests are very much alike, only difference is the time period - a week, a  month, from/to two dates, and if they display a team with users or a user.
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
                for numb in range(7):
                    self.failUnlessEqual(json_content['x_axis']['labels']['labels'][numb], datetime.datetime.strftime(datetime.datetime(2008,12,numb+1), '%A'))
                
                self.failUnlessEqual(json_content['title']['text'], '%s Week: %s Year: %s' % (user.username, week, year))
                    
                # logout when finished testing a user, to create simelar starting points for every user.
                self.client.get('/accounts/logout/')


    def testUserMonthView(self):
        # This is basicly the same as UserWeelView.
        for pk in range(2,7):
            user = User.objects.get(pk=pk)
            for month in range(1,13):
                year = 2008
                response = self.client.get('/statistics/user/%s/year/%s/month/%s/' % (user.id, year, month))
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.post('/accounts/login/',
                                            {'username': user.username, 'password': 'pass'})
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.get('/statistics/user/%s/year/%s/month/%s/' % (user.id-1, year, month))
                self.failUnlessEqual(response.status_code, 403)
        
                response = self.client.get('/statistics/data/user/%s/year/%s/month/%s/' % (user.id, year, month))
        
                json_content = json.loads(response.content)
                
                start_date = datetime.date(year, month, 1)
                end_date = start_date + datetime.timedelta(days=30)
                while end_date.month != start_date.month:
                    end_date -= datetime.timedelta(days=1)        
                
                slice_set = user.timeslices.filter(create_date__range=(start_date, end_date))
                slip_dict = {}
                for slic in slice_set:
                    if not slip_dict.has_key(slic.begin.date()):
                        slip_dict[slic.begin.date()] = [slic.slip]
                    else:
                        if slic.slip not in slip_dict[slic.begin.date()]:
                             slip_dict[slic.begin.date()].append(slic.slip)
                                
                # make a list of all the dates for the chosen month:
                w_date = start_date
                all_dates_list = []
                while w_date != end_date + datetime.timedelta(days=1):
                    all_dates_list.append(w_date)
                    w_date += datetime.timedelta(days=1)
        
                for date in all_dates_list:
                    if date not in slip_dict.keys():
                        self.failUnlessEqual(json_content['elements'][0]['values'][date.day-1], [0])
                    else:
                        for number in range(len(slip_dict[date])):
                            self.failUnlessEqual(json_content['elements'][0]['values'][date.day-1][number]['val'], round(slip_dict[date][number].display_days_time(date), 1))
            
                for numb in range(1, end_date.day+1):
                     self.failUnlessEqual(json_content['x_axis']['labels']['labels'][numb-1], str(numb))
                     
                self.failUnlessEqual(json_content['title']['text'], '%s %s %s' % (user.username, datetime.datetime.strftime(start_date, '%B'), year))
            
                self.client.get('/accounts/logout/')
                
                
    def testUserDateView(self):
        for pk in range(2,7):
            user = User.objects.get(pk=pk)
            year = 2008
            for random_generator in range(12):
                start_date = datetime.date(year, random.randrange(1,13), random.randrange(1,29))
                end_date = start_date + datetime.timedelta(days=random.randrange(1,61))
                
                response = self.client.get('/statistics/user/%s/date/%s/%s/' % (user.id, start_date, end_date))
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.post('/accounts/login/',
                                            {'username': user.username, 'password': 'pass'})
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.get('/statistics/user/%s/date/%s/%s/' % (user.id-1, start_date, end_date))
                self.failUnlessEqual(response.status_code, 403)
        
                response = self.client.get('/statistics/data/user/%s/date/%s/%s/' % (user.id, start_date, end_date))
                json_content = json.loads(response.content)
                
                slice_set = user.timeslices.filter(create_date__range=(start_date, end_date))
                slip_dict = {}
                for slic in slice_set:
                    if not slip_dict.has_key(slic.begin.date()):
                        slip_dict[slic.begin.date()] = [slic.slip]
                    else:
                        if slic.slip not in slip_dict[slic.begin.date()]:
                             slip_dict[slic.begin.date()].append(slic.slip)
                                
                # make a list of all the dates for the chosen time period:
                w_date = start_date
                all_dates_list = []
                while w_date != end_date + datetime.timedelta(days=1):
                    all_dates_list.append(w_date)
                    w_date += datetime.timedelta(days=1)
        
                for date in all_dates_list:
                    if date not in slip_dict.keys():
                        self.failUnlessEqual(json_content['elements'][0]['values'][(date-start_date).days], [0])
                    else:
                        for number in range(len(slip_dict[date])):
                            self.failUnlessEqual(json_content['elements'][0]['values'][(date-start_date).days][number]['val'], round(slip_dict[date][number].display_days_time(date), 1))
            
                for numb in range((end_date-start_date).days):
                     self.failUnlessEqual(json_content['x_axis']['labels']['labels'][numb], str(all_dates_list[numb].day))
                     
                self.failUnlessEqual(json_content['title']['text'], '%s %s to %s' % (user.username, start_date, end_date))
            
                self.client.get('/accounts/logout/')
                
                
    def testTeamWeekView(self):
        for pk in range(2,4):
            team = Team.objects.get(pk=pk)
            year = 2008
            for week in range(1,53):            
                response = self.client.get('/statistics/team/%s/year/%s/week/%s/' % (team.id, year, week))
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.post('/accounts/login/',
                                            {'username': team.creator.username, 'password': 'pass'})
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.get('/statistics/team/%s/year/%s/week/%s/' % (team.id-1, year, week))
                self.failUnlessEqual(response.status_code, 403)
        
                response = self.client.get('/statistics/data/team/%s/year/%s/week/%s/' % (team.id, year, week))
        
                json_content = json.loads(response.content)
                
                members = team.members.all()
                members_id = []
                for member in members:
                    members_id.append(member.id)
                slice_set = TimeSlice.objects.filter(week_number=week, create_date__year=year, user__in=members_id)
                
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
                                
                end_date = start_date + datetime.timedelta(days=6)
                w_date = start_date
                all_dates_list = []
                while w_date != end_date + datetime.timedelta(days=1):
                    all_dates_list.append(w_date)
                    w_date += datetime.timedelta(days=1)
        
                for date in all_dates_list:
                    if date not in slip_dict.keys():
                        self.failUnlessEqual(json_content['elements'][0]['values'][date.weekday()], [0])
                    else:
                        for number in range(len(slip_dict[date])):
                            self.failUnlessEqual(json_content['elements'][0]['values'][date.weekday()][number]['val'], round(slip_dict[date][number].display_days_time(date), 1))
        
                self.failUnlessEqual(json_content['elements'][0]['type'], 'bar_stack')
        
                for numb in range(7):
                    self.failUnlessEqual(json_content['x_axis']['labels']['labels'][numb], datetime.datetime.strftime(datetime.datetime(2008,12,numb+1), '%A'))
                
                self.failUnlessEqual(json_content['title']['text'], '%s Week: %s Year: %s' % (team.name, week, year))
                    
                self.client.get('/accounts/logout/')
                
                
    def testTeamMonthView(self):
        for pk in range(2,4):
            team = Team.objects.get(pk=pk)
            year = 2008
            for month in range(1,13):
                response = self.client.get('/statistics/team/%s/year/%s/month/%s/' % (team.id, year, month))
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.post('/accounts/login/',
                                            {'username': team.creator.username, 'password': 'pass'})
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.get('/statistics/team/%s/year/%s/month/%s/' % (team.id-1, year, month))
                self.failUnlessEqual(response.status_code, 403)
        
                response = self.client.get('/statistics/data/team/%s/year/%s/month/%s/' % (team.id, year, month))
        
                json_content = json.loads(response.content)
        
                start_date = datetime.date(year, month, 1)
                end_date = start_date + datetime.timedelta(days=30)
                while end_date.month != start_date.month:
                    end_date -= datetime.timedelta(days=1)
                members = team.members.all()
                members_id = []
                for member in members:
                    members_id.append(member.id)
                slice_set = TimeSlice.objects.filter(create_date__range=(start_date, end_date), user__in=members_id)
                
                slip_dict = {}
                for slic in slice_set:
                    if not slip_dict.has_key(slic.begin.date()):
                        slip_dict[slic.begin.date()] = [slic.slip]
                    else:
                        if slic.slip not in slip_dict[slic.begin.date()]:
                             slip_dict[slic.begin.date()].append(slic.slip)
                                
                # make a list of all the dates for the chosen month:
                w_date = start_date
                all_dates_list = []
                while w_date != end_date + datetime.timedelta(days=1):
                    all_dates_list.append(w_date)
                    w_date += datetime.timedelta(days=1)
        
                for date in all_dates_list:
                    if date not in slip_dict.keys():
                        self.failUnlessEqual(json_content['elements'][0]['values'][date.day-1], [0])
                    else:
                        for number in range(len(slip_dict[date])):
                            self.failUnlessEqual(json_content['elements'][0]['values'][date.day-1][number]['val'], round(slip_dict[date][number].display_days_time(date), 1))
            
                for numb in range(1, end_date.day+1):
                     self.failUnlessEqual(json_content['x_axis']['labels']['labels'][numb-1], str(numb))
                     
                self.failUnlessEqual(json_content['title']['text'], '%s %s %s' % (team.name, datetime.datetime.strftime(start_date, '%B'), year))
            
                self.client.get('/accounts/logout/')
                
                
    def testTeamDateView(self):
        for  pk in range (2,4):
            team = Team.objects.get(pk=pk)
            year = 2008
            for random_generator in range(20):
                start_date = datetime.date(year, random.randrange(1,13), random.randrange(1,29))
                end_date = start_date + datetime.timedelta(days=random.randrange(1,61))
        
                response = self.client.get('/statistics/team/%s/date/%s/%s/' % (team.id, start_date, end_date))
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.post('/accounts/login/',
                                            {'username': team.creator.username, 'password': 'pass'})
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.get('/statistics/team/%s/date/%s/%s/' % (team.id-1, start_date, end_date))
                self.failUnlessEqual(response.status_code, 403)
        
                response = self.client.get('/statistics/data/team/%s/date/%s/%s/' % (team.id, start_date, end_date))
                json_content = json.loads(response.content)
                
                members = team.members.all()
                members_id = []
                for member in members:
                    members_id.append(member.id)
                
                slice_set = TimeSlice.objects.filter(create_date__range=(start_date, end_date), user__in=members_id)
                slip_dict = {}
                for slic in slice_set:
                    if not slip_dict.has_key(slic.begin.date()):
                        slip_dict[slic.begin.date()] = [slic.slip]
                    else:
                        if slic.slip not in slip_dict[slic.begin.date()]:
                             slip_dict[slic.begin.date()].append(slic.slip)
                                
                # make a list of all the dates for the chosen time period:
                w_date = start_date
                all_dates_list = []
                while w_date != end_date + datetime.timedelta(days=1):
                    all_dates_list.append(w_date)
                    w_date += datetime.timedelta(days=1)
        
                for date in all_dates_list:
                    if date not in slip_dict.keys():
                        self.failUnlessEqual(json_content['elements'][0]['values'][(date-start_date).days], [0])
                    else:
                        for number in range(len(slip_dict[date])):
                            self.failUnlessEqual(json_content['elements'][0]['values'][(date-start_date).days][number]['val'], round(slip_dict[date][number].display_days_time(date), 1))
            
                for numb in range((end_date-start_date).days):
                     self.failUnlessEqual(json_content['x_axis']['labels']['labels'][numb], str(all_dates_list[numb].day))
                     
                self.failUnlessEqual(json_content['title']['text'], '%s %s to %s' % (team.name, start_date, end_date))
            
                self.client.get('/accounts/logout/')
                
                
    def testTeamStatWeekView(self):
        for pk in range(2,4):
            team = Team.objects.get(pk=pk)
            year = 2008
            for week in range(1,53):
                response = self.client.get('/statistics/team_stat/%s/year/%s/week/%s/' % (team.id, year, week))
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.post('/accounts/login/',
                                            {'username': team.creator.username, 'password': 'pass'})
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.get('/statistics/team_stat/%s/year/%s/week/%s/' % (team.id-1, year, week))
                self.failUnlessEqual(response.status_code, 403)
        
                response = self.client.get('/statistics/data/team_stat/%s/year/%s/week/%s/' % (team.id, year, week))
        
                json_content = json.loads(response.content)
                
                members = team.members.all()
                members_id = []
                for member in members:
                    members_id.append(member.id)
                
                slice_set = TimeSlice.objects.filter(week_number=week, create_date__year=year, user__in=members_id)
                
                # new slip_dict has keys equal to the team members id, and values equal to a new dict.
                slip_dict = {}
                for member in members_id:
                    slip_dict[member] = {}
                   
                start_date = datetime.date(year, 1, 1) + datetime.timedelta(days = (week-2)*7)
                while start_date.isocalendar()[1] != week:
                    start_date += datetime.timedelta(days=1)
                end_date = start_date + datetime.timedelta(days=6)
                    
                w_date = start_date
                all_dates_list = []
                # this loop generates all the dates in a list and keys for all the dates in each members dict in the slip_dict.
                # each date_key is a new dict with two keys, slip, a list to hold the slips, for checking and 'value' default 0 which is the value for that day for that user.
                while w_date != end_date + datetime.timedelta(days=1):
                    all_dates_list.append(w_date)
                    for member in members_id:
                        slip_dict[member][w_date] = {'slip' : [], 'value': 0}
                    w_date += datetime.timedelta(days=1)
                
                # this loop checks if the timeslice's slip has been processed, if it hasn't it appends the slip to the slip_key list,
                # and adds the value to the value_key int/float
                for slic in slice_set:
                    if not slic.slip in slip_dict[slic.user_id][slic.begin.date()]['slip']:
                        slip_dict[slic.user_id][slic.begin.date()]['slip'].append(slic.slip)
                        slip_dict[slic.user_id][slic.begin.date()]['value'] += slic.slip.display_days_time(slic.begin.date())
                
                counter = -1
                # this loops over members and then loops over the dates in the all_dates_list, a counter is used to keep track of the members
                # so first member looped, has counter 0, 2nd counter 1 ect. This is used to pick the dictionary in the elements list.
                for member in members_id:
                    counter += 1
                    self.failUnlessEqual(json_content['elements'][counter]['type'], 'bar') 
                    for date in all_dates_list:
                        # this statement checks to see if the value is a float or not(= int). When it is a int, rounding isn't nessesary as the value
                        # will be 0, but to keep it more simple, all numbers will be rounded, floats with 1, and ints with 0
                        if type(json_content['elements'][counter]['values'][date.weekday()]) == type(float()):
                            rounding = 1
                        else:
                            rounding = 0
                        self.failUnlessEqual(json_content['elements'][counter]['values'][date.weekday()], round(slip_dict[member][date]['value'], rounding))
                
                for numb in range(7):
                    self.failUnlessEqual(json_content['x_axis']['labels']['labels'][numb], datetime.datetime.strftime(datetime.datetime(2008,12,numb+1), '%A'))
                
                self.failUnlessEqual(json_content['title']['text'], '%s Week: %s Year: %s' % (team.name, week, year))
                    
                self.client.get('/accounts/logout/')
                
    def testTeamStatMonthView(self):
        for pk in range(2,4):
            team = Team.objects.get(pk=pk)
            year = 2008
            for month in range(1,13):
                response = self.client.get('/statistics/team_stat/%s/year/%s/month/%s/' % (team.id, year, month))
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.post('/accounts/login/',
                                            {'username': team.creator.username, 'password': 'pass'})
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.get('/statistics/team_stat/%s/year/%s/month/%s/' % (team.id-1, year, month))
                self.failUnlessEqual(response.status_code, 403)
        
                response = self.client.get('/statistics/data/team_stat/%s/year/%s/month/%s/' % (team.id, year, month))
        
                json_content = json.loads(response.content)
                
                members = team.members.all()
                members_id = []
                for member in members:
                    members_id.append(member.id)
                
                start_date = datetime.date(year, month, 1)
                end_date = start_date + datetime.timedelta(days=30)
                while end_date.month != start_date.month:
                    end_date -= datetime.timedelta(days=1)
        
                slice_set = TimeSlice.objects.filter(create_date__range=(start_date, end_date), user__in=members_id)
                
        
                slip_dict = {}
                for member in members_id:
                    slip_dict[member] = {}
                    
                w_date = start_date
                all_dates_list = []
                while w_date != end_date + datetime.timedelta(days=1):
                    all_dates_list.append(w_date)
                    for member in members_id:
                        slip_dict[member][w_date] = {'slip' : [], 'value': 0}
                    w_date += datetime.timedelta(days=1)
                
                for slic in slice_set:
                    if not slic.slip in slip_dict[slic.user_id][slic.begin.date()]['slip']:
                        slip_dict[slic.user_id][slic.begin.date()]['slip'].append(slic.slip)
                        slip_dict[slic.user_id][slic.begin.date()]['value'] += slic.slip.display_days_time(slic.begin.date())
                
                counter = -1
                
                for member in members_id:
                    counter += 1
                    self.failUnlessEqual(json_content['elements'][counter]['type'], 'scatter_line') 
                    for date in all_dates_list:
                        if type(json_content['elements'][counter]['values'][date.day-1]) == type(float()):
                            rounding = 1
                        else:
                            rounding = 0
                        self.failUnlessEqual(json_content['elements'][counter]['values'][date.day-1]['y'], round(slip_dict[member][date]['value'], rounding))
                        self.failUnlessEqual(json_content['elements'][counter]['values'][date.day-1]['x'], date.day)
                
                self.failUnlessEqual(json_content['x_axis']['min'], start_date.day)
                self.failUnlessEqual(json_content['x_axis']['max'], end_date.day)        
                self.failUnlessEqual(json_content['title']['text'], '%s, %s %s' % (team.name, datetime.datetime.strftime(start_date, '%B'), year))
                    
                self.client.get('/accounts/logout/')
        
    def testTeamStatDateView(self):
        for pk in range(2,4):
            team = Team.objects.get(pk=pk)
            year = 2008
            for random_generator in range(20):
                start_date = datetime.date(year, random.randrange(1,13), random.randrange(1,29))
                end_date = start_date + datetime.timedelta(days=random.randrange(1,61))
        
                response = self.client.get('/statistics/team_stat/%s/date/%s/%s/' % (team.id, start_date, end_date))
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.post('/accounts/login/',
                                            {'username': team.creator.username, 'password': 'pass'})
                self.failUnlessEqual(response.status_code, 302)
        
                response = self.client.get('/statistics/team_stat/%s/date/%s/%s/' % (team.id-1, start_date, end_date))
                self.failUnlessEqual(response.status_code, 403)
        
                response = self.client.get('/statistics/data/team_stat/%s/date/%s/%s/' % (team.id, start_date, end_date))
                json_content = json.loads(response.content)
        
                members = team.members.all()
                members_id = []
                for member in members:
                    members_id.append(member.id)
        
                slice_set = TimeSlice.objects.filter(create_date__range=(start_date, end_date), user__in=members_id)
                                
                slip_dict = {}
                for member in members_id:
                    slip_dict[member] = {}
                    
                w_date = start_date
                all_dates_list = []
                while w_date != end_date + datetime.timedelta(days=1):
                    all_dates_list.append(w_date)
                    for member in members_id:
                        slip_dict[member][w_date] = {'slip' : [], 'value': 0}
                    w_date += datetime.timedelta(days=1)
                
                for slic in slice_set:
                    if not slic.slip in slip_dict[slic.user_id][slic.begin.date()]['slip']:
                        slip_dict[slic.user_id][slic.begin.date()]['slip'].append(slic.slip)
                        slip_dict[slic.user_id][slic.begin.date()]['value'] += slic.slip.display_days_time(slic.begin.date())
                
                counter = -1
                
                for member in members_id:
                    counter += 1
                    self.failUnlessEqual(json_content['elements'][counter]['type'], 'scatter_line') 
                    for date in all_dates_list:
                        if type(json_content['elements'][counter]['values'][(date-start_date).days]) == type(float()):
                            rounding = 1
                        else:
                            rounding = 0
                        self.failUnlessEqual(json_content['elements'][counter]['values'][(date-start_date).days]['y'], round(slip_dict[member][date]['value'], rounding))
                        self.failUnlessEqual(json_content['elements'][counter]['values'][(date-start_date).days]['x'], time.mktime(date.timetuple())) #unix time stamp
                
                self.failUnlessEqual(json_content['x_axis']['min'], time.mktime(start_date.timetuple()))
                self.failUnlessEqual(json_content['x_axis']['max'], time.mktime(end_date.timetuple()))
                self.failUnlessEqual(json_content['x_axis']['steps'], 86400)
                self.failUnlessEqual(json_content['title']['text'], '%s: From %s to %s' % (team.name, start_date, end_date))
                    
                self.client.get('/accounts/logout/')
