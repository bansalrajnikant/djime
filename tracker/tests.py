import unittest
import urllib
from django.test.client import *
from django.contrib.auth.models import User
from django.utils.http import urlencode
from djime.tracker.models import Slip, TimeSlice
from datetime import datetime


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



class SlipRESTActionsTestCase(unittest.TestCase):
    #fixtures = ['test_users.yaml'] This doesn't seem to work :(

    def setUp(self):
        # Set up a test user
        self.john = User(username='john')
        self.john.set_password('ponies')
        self.john.save()

        # And a slip owned by our user.
        self.fish = Slip(name='Prepare for fishing trip', user=self.john)
        self.fish.save()

        # Set up a test user
        self.johny = User(username='johny')
        self.johny.set_password('ponies')
        self.johny.save()

        # And a slip owned by our user.
        self.fish = Slip(name='Prepare for fishing trip', user=self.john)
        self.fish.save()

         # And a slip owned by our user.
        self.fishy = Slip(name='Prepare for fishing trip', user=self.johny)
        self.fishy.save()

        self.client = RESTClient()


    def tearDown(self):
        self.john.delete()
        self.johny.delete()
        self.fish.delete()
        self.fishy.delete()


    def testGet(self):
        # Before we log in, we should be redirected to the login page.
        response = self.client.get('/tracker/slip/%i/' % self.fish.id)
        self.failUnlessEqual(response.status_code, 302)

        # Then log in
        response = self.client.post('/accounts/login/',
                                    {'username': 'john', 'password': 'ponies'})
        # TODO: Properly check if we're logged in instead of just checking for redirect.
        self.failUnlessEqual(response.status_code, 302)

        # Then try getting the slip again
        response = self.client.get('/tracker/slip/%i/' % self.fish.pk)
        self.failUnlessEqual(response.status_code, 200)

        # Then let's delete the slip
        response = self.client.delete('/tracker/slip/%i/' % self.fish.pk)
        self.failUnlessEqual(response.status_code, 200)

        # Then try getting the slip again, this time we should get 404, since
        # it has been deleted.
        response = self.client.get('/tracker/slip/%i/' % self.fish.pk)
        self.failUnlessEqual(response.status_code, 404)


    def testChangeSlipName(self):
        # First login
        response = self.client.post('/accounts/login/',
                                    {'username': 'john', 'password': 'ponies'})

        # Then getting the slip
        response = self.client.get('/tracker/slip/%i/' % self.fish.pk)

        # Now let's change the slip name
        response = self.client.put('/tracker/slip/%i/' % self.fish.pk,
                                   {'name': 'Polishing horses'})
        self.failUnlessEqual(response.status_code, 200)

        # Lets reload the object from the db
        response = self.client.get('/tracker/slip/%i/' % self.fish.pk)
        self.failUnlessEqual(response.status_code, 200)

        # Last, we're going to check the new name of the slip
        self.failUnlessEqual(self.fish.name, 'Polishing horses')


    def testStartTimeSlice(self):
        # Login
        response = self.client.post('/accounts/login/',
                                    {'username': 'john', 'password': 'ponies'})

        # Get slip
        response = self.client.get('/tracker/slip/%i/' % self.fish.pk)

        # Send the request to start a new timeslip
        # first we'll create a time to send, that we can use to compare later
        timeSetBegin = datetime.now()
        response = self.client.put('/tracker/slip/%i/start/' % self.fish.pk,
                                   {'begin': timeSetBegin})
        self.failUnlessEqual(response.status_code, 200)

        # Let's see if the timeslice has been created and have the correct start time
        try:
            timeSlice = TimeSlice.objects.get(begin = timeSetBegin)

        except TimeSlice.DoesNotExist:
            self.fail('Failed to get TimeSlice, TimeSlice has not been created with correct begin time')


    def testStopTimeSlice(self):
        # Login
        response = self.client.post('/accounts/login/',
                                    {'username': 'john', 'password': 'ponies'})

        # Get slip
        response = self.client.get('/tracker/slip/%i/' % self.fish.pk)

        # Send the request to start a new timeslip
        # first we'll create a time to send, that we can use to compare later
        timeSetBegin = datetime.now()
        response = self.client.put('/tracker/slip/%i/start/' % self.fish.pk,
                                   {'begin': timeSetBegin})

        # Now stopping the timeslip with a new timeSet
        timeSetEnd = datetime.now()
        response = self.client.put('/tracker/slip/%i/stop/' % self.fish.pk,
                                   {'end': timeSetEnd})
        self.failUnlessEqual(response.status_code, 200)

        # Lets see if we have a created timeslice with the correct end time
        # we do that, by try, exepting that is does not exist.
        try:
            timeSlice = TimeSlice.objects.get(end = timeSetBegin)

        except TimeSlice.DoesNotExist:
            self.fail('Failed to get TimeSlice, TimeSlice has not been stopped with correct end time')

    def testCreateSlip(self):
         # Login
        response = self.client.post('/accounts/login/',
                                    {'username': 'john', 'password': 'ponies'})

        # Get slip
        response = self.client.get('/tracker/slip/%i/' % self.fish.pk)

        # Create the slip
        response = self.client.post('/tracker/slip/create/',
                                    {'name': 'Working all night with 5 ponies'})

        # now lets see if our slip has been created
        try:
            Slip.objects.get(name = 'Working all night with 5 ponies')

        except Slip.DoesNotExist:
            self.fail('Failed to get Slip, Slip has not been created with the correct time')
