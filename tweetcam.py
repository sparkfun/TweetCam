#!/usr/bin/env python2.7  
# TweetCam - Take a photo on GPIO input and post to Twitter
# Based on tweetpic.py by Alex Eames http://raspi.tv/?p=5918  
# Modified by Nick Poole http://sparkfun.com
import RPi.GPIO as GPIO
import tweepy  
from subprocess import call  
from datetime import datetime  

GPIO.setmode(GPIO.BCM) #we want to reference the GPIO by chip number

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) #our shutter switch is on pin 18
GPIO.setup(4, GPIO.OUT, initial=GPIO.HIGH) #our status LED is on pin 4, turn it on

while 1: #loop forever

  while GPIO.input(18): #wait for the shutter button. do nothing.
    pass

  i = datetime.now()               #take time and date for filename  
  now = i.strftime('%Y%m%d-%H%M%S')  
  photo_name = now + '.jpg'  
  cmd = 'raspistill -t 500 -w 1024 -h 768 -o /home/pi/' + photo_name   
  call ([cmd], shell=True)         #shoot the photo  

  # Consumer keys and access tokens, used for OAuth  
  consumer_key = 'copy your consumer key here'  
  consumer_secret = 'copy your consumer secret here'  
  access_token = 'copy your access token here'  
  access_token_secret = 'copy your access token secret here'  

  GPIO.output(4, 0) #turn off status LED to signal the user to wait

  # OAuth process, using the keys and tokens  
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
  auth.set_access_token(access_token, access_token_secret)  

  # Creation of the actual interface, using authentication  
  api = tweepy.API(auth)  

  # Send the tweet with photo  
  photo_path = '/home/pi/' + photo_name  
  status = 'Photo auto-tweet from Pi: ' + i.strftime('%Y/%m/%d %H:%M:%S')   
  api.update_with_media(photo_path, status=status)  
  
  GPIO.output(4, 1) #turn on status LED for OK
  
