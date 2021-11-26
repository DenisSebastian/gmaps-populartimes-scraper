#! /usr/bin/python

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
import re
import datetime
import sys
import argparse
import json

url = 'https://www.google.com/maps/place/Plaza+La+Concordia/@-33.4279616,-70.5706575,18z/data=!4m5!3m4!1s0x9662cefe973d6dcb:0x94ec55ea4a798e74!8m2!3d-33.4282188!4d-70.5699103'

class PopularTimes:
    def __init__(self, path = '/usr/bin/chromedriver'):
        self.service = Service(path) # chromedriver path
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--lang=es-CL')

    def make_driver(self):
        '''
        Initialize Selenium ChormeDriver 
        '''
        self.driver = webdriver.Chrome(service=self.service, options = self.options) 

    def get_parsed_days(self,url,wait):
        ''' Get parsed daily info from the url html

        Parameters:
        url(string): a Google Maps place url

        Saves a parsed daily info on 'days' attribute
        '''
        assert PlaceUrlChecker.check(url),'Not valid url'

        try:
            self.driver.get(url) # load gmaps url
        except:
            self.make_driver() # re-make driver
            self.driver.get(url) 

        self.now_hour = datetime.datetime.now().hour # save current hour
        sleep(wait) # wating time for load gmaps
        
        # get the html
        html = self.driver.page_source
        # parsing
        soup = BeautifulSoup(html, features='html.parser')
        # popular times section
        section = soup.find('div',{'class':'O9Q0Ff-NmME3c-Utye1-haAclf'})
        
        # days list
        self.days = section.findChildren('div',recursive=False)
        
    def hours_of_day(self,i):
        '''Get a dict with popular times of a day

        Parameters:
        day (int): integer from 0 to 6. The day 0 is Sunday and so on.

        Return:
        A dictionary with the form {hour: percentage of concurrence}. If the place is close, returns an empty dict
        '''

        hours =  self.days[i].findChildren('div',recursive=False)[1].findChildren('div',recursive=False)
        hours = [h['aria-label'] for h in hours if 'aria-label' in h.attrs.keys()]
        hours_dict = {}

        for h in hours:
            pattern = re.search('(\d\d?)%[\w\s\(\)]+(\d\d):00',h)
            try:
                hour = int(pattern.group(2))
                percent = int(pattern.group(1)) 
                hours_dict[hour] = percent
            except:
                # info of current time and day appears differently. This solve this
                # works for spanish
                currently = re.search('generalmente (\d\d?)%',h)
                if currently:
                    hours_dict[self.now_hour] = int(currently.group(1))
                else:
                    hours_dict = {}
                    break
        
        return hours_dict

    def get_populartimes(self,url,wait = 2):
        '''Get popular times from a gmaps url

        Parameters:
        url(string): a Google Maps place url  

        Return:
        A nested dictionary with a dictionary of hourly concurrence by day.
        '''
        self.get_parsed_days(url, wait)
        self.days_hours = {}

        for i in range(7):
            self.days_hours[i] = list(self.hours_of_day(i).items())
    
        self.fix_hours()

        self.days_hours = {k:dict(self.days_hours[k]) for k in self.days_hours}

    @staticmethod
    def HourIterator(items):
        for i in items:
            yield i[0]

    def fix_hours(self):
        valid_days = [k for k in self.days_hours.keys() if len(self.days_hours[k]) != 0]
        for day in valid_days:
            if day == 6:
                next_day = 0
            else:
                next_day = day + 1

            hours_items =  self.days_hours[day]
            prev_hour = hours_items[0][0]
            it = PopularTimes.HourIterator(hours_items)
            for i,hour in enumerate(it):
                if prev_hour > hour:
                    idx = i
                    break
                
                prev_hour = hour
            
            if 'idx' in vars():
                extra_hours = []
                for i in range(len(hours_items)- idx):
                    extra_hours.append(hours_items.pop(idx))
        
                self.days_hours[next_day] = extra_hours + self.days_hours[next_day]

    def to_json(self,output, mode = 'w'):
        if hasattr(self,'days_hours'):
            file = open(output,mode)
            json.dump(self.days_hours,file)
        else:
            raise Exception('Popular schedules have not been obtained yet')

class PlaceUrlChecker:
    full_url_pattern_1 = '^https?://(www.|maps.)?google.[a-z]+/maps/place/'
    full_url_pattern_2 = '-?\d{,2}\.\d{7},-?\d{,2}\.\d{7},\d{,2}[\.\d{2}]?z/data?=.*'
    short_url_pattern = 'https?://goo.gl/maps/[\w]+$' 

    @classmethod
    def full_url(cls,url):
        url = url.split('@')
        match_1 = re.match(cls.full_url_pattern_1,url[0])
        try:
            match_2 = re.match(cls.full_url_pattern_2,url[1])
        except:
            return False
        
        return match_1 and match_2 

    @classmethod
    def short_url(cls,url):
        return re.match(cls.short_url_pattern,url)
        
    @classmethod
    def check(cls,url):
        match_1 = cls.full_url(url)
        match_2 = cls.short_url(url)

        return match_1 or match_2


class PopularTimesCLI:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Scrap popular times for places from Google Maps.',
                formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=40))
        parser.add_argument('-u','--url', type=str, help='the Google Maps Place URL you want to get hourly concurrence from', required = True)
        parser.add_argument('-o','--output', nargs='?', type=str, help='path of the JSON output file')
        parser.add_argument('--chromedriver', nargs='?', type=str, help='chromedriver path', default = '/usr/bin/chromedriver')
        parser.add_argument('--wait', nargs='?', type=int, help='second to wait for google maps to load', default = 2)

        self.args = vars(parser.parse_args())
        
        self.pt = PopularTimes(path = self.args['chromedriver'])
        self.pt.get_populartimes(url = self.args['url'], wait = self.args['wait'])
        self.pt.driver.close()

    def Action(self):
        if self.args['output'] == None:
            print(self.pt.days_hours)
        else:
            self.pt.to_json(output = self.args['output'])


def main():
    ptCLI = PopularTimesCLI()
    ptCLI.Action()


if __name__ == '__main__':
    main()

