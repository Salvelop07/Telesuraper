FROM scrapinghub/scrapinghub-stack-scrapy:1.5-py3

ENV TERM xterm

ENV SCRAPY_SETTINGS_MODULE Telesuraper.settings

ENV PRISMA_ENDPOINT=
ENV PRISMA_SECRET=
ENV SERVICE_ID=

# Broadcast schedules
ENV SCHEDULE_TIMEZONE='UTC'
ENV SCHEDULE_URL=

# Article listings
ENV JSPLISTING_PAGE_SIZE=
ENV JSPLISTING_MAX_PAGES=
ENV JSPLISTING_URL=

RUN apt-get update && apt-get install -y libtidy-dev

RUN mkdir -p /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN python setup.py install
