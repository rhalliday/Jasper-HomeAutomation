# -*- coding: utf-8-*-
"""
    A HomeAutomation plugin for the Jasper automated voice recognition software
    
    Based on the Domoticz plugin from Niels Looije which is based on script v1.6.2
    by Chopper_Rob:
    https://www.chopperrob.nl/domoticz/5-report-devices-online-status-to-domoticz
"""
import re
import urllib2
import json
import base64
import ssl
from client import app_utils

__author__ = "Rob Halliday"
__license__ = "MIT"
__version__ = "0.0.3"
__maintainer__ = "Rob Halliday"
__email__ = "rob_halliday_1@hotmail.com"
__status__ = "Development"

DEBUG = False

WORDS = [ "RUN", "SCENE", "EVENING", "MODE", "NIGHT", "KIDS", "LOUNGE", "LIGHT", "ON", "OFF", "OUT", "BEDTIME", "RISE", "SHINE", "YES", "NO" ]
PRIORITY = 10

def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, with the result of
        a command given by the user to control devices, scenes and/or groups
        in different rooms through the HomeAutomation JSON API.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., HomeAutomation
                   server address, username and password)
        
        Returns:
        The result of a command issued to HomeAutomation through Jasper
    """
    def get_credentials():
        """
            Get the server, username and password from profile

            Returns:
            Server url and encoded credentials for HomeAutomation server
        """
        server = profile['ha']['server']
        username = profile['ha']['username']
        password =  profile['ha']['password']
        encoded_creds = encode_credentials(username, password)
        return server, encoded_creds

    def encode_credentials(username, password):
        """
            Encode the credentials into a base64 encoded string

            Arguments:
            username -- a username for the HomeAutomation server
            password -- a password corresponding to the username

            Returns:
            Encoded string of credentials
        """
        return base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    def send_request(data):
        """
            Sends a json request to the HomeAutomation server
            The request is appended to the server url and
            the encoded credentials are added to the header

            Arguments:
            data -- json string

            Returns:
            Response to json request
        """
        server, encoded_creds = get_credentials()
        request = urllib2.Request(server + 'api')
        request.add_header("Authorization", "Basic %s" % encoded_creds)
        request.add_header("Content-Type", "application/json")
        request.add_data(data)
	# TODO: find out how to use my cert, wget uses it :(
	context = ssl._create_unverified_context()
        response = urllib2.urlopen(request, context=context)
        return response.read()

    # find the scene being referenced
    m = re.search('run \w+ (.+)', text, re.IGNORECASE)
    search = m.group(0).lower()
    mic.say('searching for ' + search);
    data = json.dumps({ 'scene': search })

    obj = json.loads(send_request(data))
    # if we have a scene id then try to run it, or report the error
    if 'scenes' in obj:
        run = False;
        for scene in obj['scenes']:
            mic.say('do you want me to run scene ' + scene['scene'])
            if app_utils.isPositive(mic.activeListen()):
                mic.say('running scene ' + scene['scene'])
                request = json.dumps({ 'scene': scene['scene_id'] })
                result = json.loads(send_request(request))
                mic.say(result['message'])
                run = True;
                break
        if not run:
            mic.say('ok, awaiting further commands')
    else:
        mic.say(obj['message'])

def isValid(text):
    """
        Returns True if the input is related to home automation.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(run|scene|seen)\b', text, re.IGNORECASE))
