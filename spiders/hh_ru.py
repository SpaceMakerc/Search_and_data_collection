import scrapy
from scrapy.http import HtmlResponse
from home_pars.items import HomeParsItem


class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']

    start_urls = ['https://krasnoyarsk.hh.ru/search/vacancy?area=88&search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post'
                  ]

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vac_links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for i in vac_links:
            yield response.follow(i, callback=self.parse_vac)

    def parse_vac(self, response:HtmlResponse):

        vac_name = response.css("h1::text").get()
        vac_url = response.url
        vac_salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()

        yield HomeParsItem(name = vac_name, salary = vac_salary, link = vac_url)
