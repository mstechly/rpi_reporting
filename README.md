# rpi_reporting
Project for gathering data, storing them on rpi and sending regularly with email.


## Motivation

I had to gather data from the internet regularly for a longer period of time.
Since I had a RPi I decided to use it.
But since I wanted the whole process automated and reusable I decided to separate the reporting part from the gathering.
And that's why I created this project.


## Prerequisites

In order to use it, you need:
a) raspberry pi connected to the internet
b) a gmail account (however after small modifications any email account will do)
c) some script for gathering data

## What it does?

It:
1. Gathers data in the regular intervals and saves them into separate, datetime-tagged files.
2. After specified time zips the data and sends them to your e-mail
3. Creates new directory and goes back to 1.
4. If some kind of error occurs it also sends you an e-mail and retries to do the job.


## Getting started

There is a dummy data gathering script in this project, which collects weather data from http://apidev.accuweather.com.

Before you start, put the credentials for your gmail account into credentials.txt with the following format:

`
user:email1:password
recipient:email2
`

In order to run the scripy just type:

`
python main.py 60 300
`

60 means, that you will gather data every 60 seconds.
300 means, that you will send an e-mail report every 300 seconds

If you don't want the process to be killed after closing shell:

`
sudo nohup python main.py &
`

## Why not cronjob?

Functionalities of these scripts could easily be achieved with cronjob.
I haven't used it since:
a) I am more familiar with doing it in python
b) I like to have everything in the script
c) I suppose error handling is easier this way.