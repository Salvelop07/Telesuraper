# teleSUR scraper

## Extracted data

### Broadcast Events schedule

    {
        "end": datetime.time(21, 29),
        "service": "telesur",
        "start": datetime.time(20, 59),
        "serie": "Reportajes teleSUR - Medio Ambiente el combustible",
        "weekday": 2,
        "timezone": "America/Caracas"
    }

## Spiders

    $ scrapy list
    broadcast-schedule

## Running the spiders

    $ scrapy crawl broadcast-schedule
