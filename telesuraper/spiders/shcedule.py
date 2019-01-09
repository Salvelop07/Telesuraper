from datetime import time
from scrapy.spiders import Spider, Request

from Telesuraper.items import BroadcastEventItem

WEEKDAYS = ('lunes', 'martes', 'miercoles',
            'jueves', 'viernes', 'sabado', 'domingo')
MONTHS = ('ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN',
          'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC')


class BroadcastSchedule(Spider):
    name = 'schedule'

    def start_requests(self):
        for weekday in WEEKDAYS:
            url = '{}?tz=0&all=true&day={}'.format(
                self.settings['SCHEDULE_URL'], weekday)
            yield Request(url, self.parse)

    def parse(self, response):
        """ Parses teleSUR broadcast events schedule

        @url https://www.telesurtv.net/seccion/programas/helper.html?tz=0&all=true&day=lunes
        @returns items 12 48
        @returns requests 0 0
        @scrapes service timezone weekday start end serie
        """
        for schedule in response.css('#grilla-web .scheduleback'):
            time_ranges = list(map(int, schedule.css(
                '.sdate::text').re(r'(\d\d):(\d\d)')))
            yield BroadcastEventItem(
                service=self.settings['SERVICE_ID'],
                timezone=self.settings['SCHEDULE_TIMEZONE'],
                start=time(*time_ranges[:2]),
                end=time(*time_ranges[2:]),
                serie=schedule.css('.stitle a::text').extract_first(),
                weekday=next(WEEKDAYS.index(day) for day in WEEKDAYS
                             if 'day={}'.format(day) in response.request.url))
