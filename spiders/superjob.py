import scrapy
from scrapy.http import HtmlResponse
from home_pars.items import HomeParsItem

class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/slesar.html?geo%5Bt%5D%5B0%5D=4&page=1']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[contains(@rel, 'next')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vac_link = response.xpath("//a[contains(@class, 'YrERR HyxLN')]/@href").getall()
        for i in vac_link:
            yield response.follow(i, callback=self.parse_vac)

    def parse_vac(self, response: HtmlResponse):

        vac_name = response.css("//h1/text()").get()
        vac_url = response.url
        vac_salary = response.xpath("//span[@class='_4Gt5t _2nJZK']//text()").getall()

        HomeParsItem(name = vac_name, salary = vac_salary, link = vac_url)
