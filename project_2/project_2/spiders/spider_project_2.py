import scrapy
import requests

class SpiderProject2Spider(scrapy.Spider):
    name = "spider_project_2"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/coronavirus"]
    
    def parse(self, response):
        coun = response.xpath("//table[@id='main_table_countries_today']/tbody[1]/tr/td[2]/a[@class='mt_a']")
        for country in coun:
            names=country.xpath("text()").get()
            link=country.xpath("@href").get()
            #ab_link=f"https://www.worldometers.info/coronavirus/{link}"
            ab_link = response.urljoin(link)
            yield response.follow(url=ab_link,callback=self.page_parser,meta={'country':names}) 
            
    def page_parser(self,response):
        names = response.request.meta["country"]
        active_cases = response.xpath("(//div[@class='maincounter-number'])[1]/span/text()").get()
        death_cases = response.xpath("(//div[@class='maincounter-number'])[2]/span/text()").get()
        recover_cases = response.xpath("(//div[@class='maincounter-number'])[3]/span/text()").get()
        
        yield{
            'Name':names,
            'Active_Cases' : active_cases,
            'Deaths' : death_cases,
            'Recovery' : recover_cases
        }