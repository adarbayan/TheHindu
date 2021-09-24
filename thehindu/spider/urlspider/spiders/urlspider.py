import scrapy
import re
import logging
import codecs
import json
from scrapy.utils.log import configure_logging
import logging
from datetime import timedelta, datetime


class QuotesSpider(scrapy.Spider):
    name = "urlspider"
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='urlspiderlog.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def start_requests(self):
        date_start = datetime(2018,1,1)
        date_end = datetime(2021,9,15)
        #date_number = The number of days between the start and end date.
        date_number = date_end - date_start 
        numberOfDays=date_number.days
        url=  'https://www.thehindu.com/archive/print/2018/01/01/'
        for i in range(numberOfDays):
            yield scrapy.Request(url=url, callback=self.parse)
            self.date_start += timedelta(days=1)
            url = "https://www.thehindu.com/archive/print/" + self.date_start.strftime('%Y/%m/%d/')

    def parse(self, response):
        print(response.url)
        urlfilename = re.sub(r"\/|:", r"_", response.url)
           

        urls = response.xpath('//ul[@class="archive-list"]//a/@href').extract()
        filename = 'urls.jl'
        with codecs.open(filename, 'a', 'utf-8') as f:
            for rl in urls:
                line = json.dumps(rl,ensure_ascii=False) + "\n"
                f.write(line)        

