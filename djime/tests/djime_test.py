import random
from django.test import TestCase
import urllib
from datetime import datetime
from django.test.client import *
from django.contrib.auth.models import User
from django.utils.http import urlencode
from djime.models import Slip, TimeSlice


class RESTClient(Client):
    """
    Subclass of django.test.client.Client, enabling more HTTP methods

    Since http://code.djangoproject.com/ticket/5888 is not going to be fixed for
    Django 1.0.x, we will implement the same behavior in a subclass.
    """

    def head(self, path, data={}, **extra):
        """
        Request a response from the server using HEAD.
        """
        r = {
            'CONTENT_LENGTH':  None,
            'CONTENT_TYPE':    'text/html; charset=utf-8',
            'PATH_INFO':       urllib.unquote(path),
            'QUERY_STRING':    urlencode(data, doseq=True),
            'REQUEST_METHOD': 'HEAD',
        }
        r.update(extra)

        return self.request(**r)

    def options(self, path, data={}, **extra):
        """
        Request a response from the server using OPTIONS.
        """
        r = {
            'CONTENT_LENGTH':  None,
            'CONTENT_TYPE':    None,
            'PATH_INFO':       urllib.unquote(path),
            'QUERY_STRING':    urlencode(data, doseq=True),
            'REQUEST_METHOD': 'OPTIONS',
        }
        r.update(extra)

        return self.request(**r)

    def put(self, path, data={}, content_type=MULTIPART_CONTENT, **extra):
        """
        Send a resource to the server using PUT.
        """
        if content_type is MULTIPART_CONTENT:
            post_data = encode_multipart(BOUNDARY, data)
        else:
            post_data = data
        r = {
            'CONTENT_LENGTH': len(post_data),
            'CONTENT_TYPE':   content_type,
            'PATH_INFO':      urllib.unquote(path),
            'REQUEST_METHOD': 'PUT',
            'wsgi.input':     FakePayload(post_data),
        }
        r.update(extra)

        return self.request(**r)

    def delete(self, path, data={}, **extra):
        """
        Send a DELETE request to the server.
        """
        r = {
            'CONTENT_LENGTH':  None,
            'CONTENT_TYPE':    None,
            'PATH_INFO':       urllib.unquote(path),
            'REQUEST_METHOD': 'DELETE',
            }
        r.update(extra)

        return self.request(**r)



class SlipRESTActionsTestCase(TestCase):
    fixtures = ['auth.json','slip.json', 'slice.json', 'team.json']

    def setUp(self):
        self.client = RESTClient()

    def testGet(self):
        user = User.objects.get(pk=2)
        for pk in range(1,13):
            slip = Slip.objects.get(pk=pk)
            # Before we log in, we should be redirected to the login page.
            response = self.client.get('/slip/%i/' % 3)
            self.failUnlessEqual(response.status_code, 302)

            # Then log in
            response = self.client.post('/accounts/login/',
                                        {'username': user.username, 'password': 'pass'})
            # TODO: Properly check if we're logged in instead of just checking for redirect.
            self.failUnlessEqual(response.status_code, 302)

            # Then try getting the slip again
            response = self.client.get('/slip/%i/' % slip.id)
            if slip.user == user:
                self.failUnlessEqual(response.status_code, 200)
            else:
                self.failUnlessEqual(response.status_code, 403)

            # Then let's delete the slip
            response = self.client.delete('/slip/%i/' % slip.id)
            if slip.user == user:
                self.failUnlessEqual(response.status_code, 200)
            else:
                self.failUnlessEqual(response.status_code, 403)

            # Then try getting the slip again, this time we should get 404, since
            # it has been deleted.
            response = self.client.get('/slip/%i/' % slip.id)
            if slip.user == user:
                self.failUnlessEqual(response.status_code, 404)
            else:
                self.failUnlessEqual(response.status_code, 403)

            # logout when finished testing a slip, to create simelar starting
            # points for every slip
            self.client.get('/accounts/logout/')

    def testChangeSlipName(self):
        # First login
        for pk in range(2,7):
            user = User.objects.get(pk=pk)
            for pk in range(1,13):
                slip = Slip.objects.get(pk=pk)
                response = self.client.post('/accounts/login/',
                                    {'username': user.username, 'password': 'pass'})

                # Then getting the slip
                response = self.client.get('/slip/%i/' % slip.id)

                name = random.randrange(1,100000000)
                # Now let's change the slip name
                response = self.client.post('/slip/%i/' % slip.id,
                                   {'name': name})
                if user == slip.user:
                    self.failUnlessEqual(response.status_code, 200)
                else:
                    self.failUnlessEqual(response.status_code, 403)

                # Last, we're going to check the new name of the slip
                slip_new_name = Slip.objects.get(pk=slip.id)
                if user == slip.user:
                    self.failUnlessEqual(int(slip_new_name.name), name)


    def testStartTimeSlice(self):
        for pk in range(2,7):
            user = User.objects.get(pk=pk)
            for pk in range(1,13):
                slip = Slip.objects.get(pk=pk)
                # Login
                response = self.client.post('/accounts/login/',
                                            {'username': user.username, 'password': 'pass'})

                # Get slip
                response = self.client.get('/slip/%i/' % slip.id)

                # Send the request to start a new timeslip
                # first we'll create a time to send, that we can use to compare later
                timeSetBegin = datetime.now()
                begin = '%s, %s, %s, %s, %s, %s, %s' % (timeSetBegin.year, timeSetBegin.month, timeSetBegin.day, timeSetBegin.hour, timeSetBegin.minute, timeSetBegin.second, timeSetBegin.microsecond)
                response = self.client.post('/slip/%i/start/' % slip.id,
                                           {'begin': begin})
                if user == slip.user:
                    self.failUnlessEqual(response.status_code, 200)
                else :
                    self.failUnlessEqual(response.status_code, 403)

                # Let's see if the timeslice has been created and have the correct start time
                try:
                    timeSlice = TimeSlice.objects.get(begin = timeSetBegin)
                    if user != slip.user:
                        self.fail('Unauthorized user started timeslice')

                except TimeSlice.DoesNotExist:
                    if user == slip.user:
                        self.fail('Failed to get TimeSlice, TimeSlice has not been created with correct begin time')


    def testStopTimeSlice(self):
        for pk in range(2,7):
            user = User.objects.get(pk=pk)
            for pk in range(1,13):
                slip = Slip.objects.get(pk=pk)
                # Login
                response = self.client.post('/accounts/login/',
                                            {'username': user.username, 'password': 'pass'})

                # Get slip
                response = self.client.get('/slip/%i/' % slip.pk)

                # Send the request to start a new timeslip
                # first we'll create a time to send, that we can use to compare later
                timeSetBegin = datetime.now()
                begin = '%s, %s, %s, %s, %s, %s, %s' % (timeSetBegin.year, timeSetBegin.month, timeSetBegin.day, timeSetBegin.hour, timeSetBegin.minute, timeSetBegin.second, timeSetBegin.microsecond)
                response = self.client.post('/slip/%i/start/' % slip.pk,
                                           {'begin': begin})

                # Now stopping the timeslip with a new timeSet
                timeSetEnd = datetime.now()
                end = '%s, %s, %s, %s, %s, %s, %s' % (timeSetEnd.year, timeSetEnd.month, timeSetEnd.day, timeSetEnd.hour, timeSetEnd.minute, timeSetEnd.second, timeSetEnd.microsecond)
                response = self.client.post('/slip/%i/stop/' % slip.pk,
                                           {'end': end})
                if user == slip.user:
                    self.failUnlessEqual(response.status_code, 200)
                else:
                    self.failUnlessEqual(response.status_code, 403)

                # Lets see if we have a created timeslice with the correct end time
                # we do that, by try, exepting that is does not exist.
                try:
                    time_slice = TimeSlice.objects.get(end = timeSetEnd)
                    if user != slip.user:
                        self.fail('Unauthorized user stopped timeslice')
                    else:
                        self.failUnlessEqual(timeSetBegin, time_slice.begin)
                        self.failUnlessEqual(timeSetEnd, time_slice.end)

                except TimeSlice.DoesNotExist:
                    if user == slip.user:
                        self.fail('Failed to get TimeSlice, TimeSlice has not been stopped with correct end time')

    def testCreateSlip(self):
        for pk in range(2,7):
            user = User.objects.get(pk=pk)
             # Login
            response = self.client.post('/accounts/login/',
                                        {'username': user.username, 'password': 'pass'})

            # Create the slip
            response = self.client.post('/slip/add/',
                                        {'name': '%s is working all night with 5 ponies' % (user.username,)})

            # now lets see if our slip has been created
            try:
                Slip.objects.get(name = '%s is working all night with 5 ponies' % (user.username,))

            except Slip.DoesNotExist:
                self.fail('Failed to get Slip, Slip has not been created')
