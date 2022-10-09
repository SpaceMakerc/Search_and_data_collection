import scrapy
from scrapy.http import HtmlResponse
import requests
from pars_gb.items import ParsGbItem
import os
from copy import deepcopy


class GbRuSpider(scrapy.Spider):
    name = 'gb_ru'
    allowed_domains = ['gb.ru']
    start_urls = ['https://gb.ru/login/']
    login_link = 'https://gb.ru/login'
    client = requests.session()
    login_x = 'mabemi6344@oncebar.com'
    password_x = 'test1234'


    def parse(self, response: HtmlResponse):
        print('@##################################')
        post_hashe = response.text[response.text.find('csrf-token')+21:response.text.find('csrf-token')+109]
        yield scrapy.FormRequest(
            'https://gb.ru/login/',
            method='POST',
            callback=self.login,
            formdata={
                'authenticity_token': post_hashe,
                'email': self.login_x,
                'password': self.password_x,
                'remember_me': '0'})

    def login(self, response: HtmlResponse):
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        if response.text.find('Моё обучение'):
            infa = response.xpath("//div[contains(@class, 'columns_xxl_4')]//a/@href").getall()
            for i in infa:
                yield response.follow(
                    i, callback=self.studying_programs)

    def studying_programs(self, response: HtmlResponse):
        xpath_name = "//div[@class='paragraph new-d w-richtext']/p/text()"
        xpath_description = "//div[@class='collection-list new-d w-dyn-items']//a/@href"
        xpath_link = "//div[@class='collection-list new-d w-dyn-items']//div[@class='product_title new-d']/text()"
        all_descriptions = [i for i in response.xpath(
            f'{xpath_name}|{xpath_description}|{xpath_link}'
        ).getall() if i != '\u200d']
        for num, card in enumerate(all_descriptions):
            if num % 3 == 0:
                description = {'name': all_descriptions[num], 'descr': all_descriptions[num+1]}
                link = all_descriptions[num+2]
                yield response.follow(
                    link, callback=self.description_of_the_training_program, cb_kwargs={'description': deepcopy(description)})

    def description_of_the_training_program(self, response: HtmlResponse, description):
        name = description['name']
        text = description['descr']
        link = response.url
        _id = response.url
        yield ParsGbItem(name=name, text=text, link=link, _id=_id)
