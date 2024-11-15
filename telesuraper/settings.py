# -*- coding: utf-8 -*-

# Scrapy settings for Telesuraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

import os

# Database
PRISMA_ENDPOINT = os.getenv('PRISMA_ENDPOINT', 'http://localhost:4466/')
PRISMA_TOKEN = os.getenv('PRISMA_TOKEN')

# Tenant
SERVICE_ID = os.getenv('SERVICE_ID')

# Broadcast schedules
SCHEDULE_URL = os.getenv('SCHEDULE_URL')
SCHEDULE_TIMEZONE = os.getenv('SCHEDULE_TIMEZONE')

# Article listings
JSPLISTING_PAGE_SIZE = os.getenv('JSPLISTING_PAGE_SIZE')
JSPLISTING_MAX_PAGES = os.getenv('JSPLISTING_MAX_PAGES')
JSPLISTING_START_PAGE = os.getenv('JSPLISTING_START_PAGE')
JSPLISTING_URL = os.getenv('JSPLISTING_URL')

BOT_NAME = 'Telesuraper'

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Telesuraper.pipelines.PrismaArticlePipeline': 300,
}

SPIDER_MODULES = ['Telesuraper.spiders']
NEWSPIDER_MODULE = 'Telesuraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'telesur (+https://www.telesurtv.net)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Telesuraper.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'Telesuraper.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'Telesuraper.extensions.telnet.TelnetConsole': None,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
