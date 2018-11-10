from datetime import time
import os
import re

import scrapy
from scraper.items import BroadcastEventItem

SERVICE_ID = os.environ.get('SERVICE_ID')
SCHEDULE_URL = os.environ.get('SCHEDULE_URL')
SCHEDULE_TIMEZONE = os.environ.get('SCHEDULE_TIMEZONE')

WEEKDAYS = ('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo')
MONTHS = ('ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC')


class BroadcastSchedule(scrapy.Spider):
    name = 'broadcast-schedule'
    start_urls = ['{}?tz=0&all=true&day={}'.format(SCHEDULE_URL, dia)
                  for dia in WEEKDAYS]

    def parse(self, response):
        """ Parses teleSUR broadcast events schedule

        @url https://www.telesurtv.net/seccion/programas/helper.html?tz=0&all=true&day=lunes
        @returns items 12 48
        @returns requests 0 0
        @scrapes service timezone weekday start end serie
        """
        for schedule in response.css('#grilla-web .scheduleback'):
            time_ranges = list(map(int, schedule.css('.sdate::text').re(r'(\d\d):(\d\d)')))
            yield BroadcastEventItem(
                service=SERVICE_ID,
                timezone=SCHEDULE_TIMEZONE,
                start=time(*time_ranges[:2]),
                end=time(*time_ranges[2:]),
                serie=schedule.css('.stitle a::text').extract_first(),
                weekday=next(WEEKDAYS.index(day) for day in WEEKDAYS
                             if 'day={}'.format(day) in response.request.url))
