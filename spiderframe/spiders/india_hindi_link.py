# -*- coding: utf-8 -*-
import scrapy

from spiderframe.items import ImgsItem


class IndiaHindiLinkSpider(scrapy.Spider):
    name = 'india_hindi_image'
    allowed_domains = ['hindi.webdunia.com']
    start_urls = [
        'https://hindi.webdunia.com/ganesh-utsav-special?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/indian-festivals?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/indian-religion?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/shirdi-sai-baba?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/astrology-hindi#498?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/mahabharat?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/sanatan-dharma?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/religious-journey#999?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'http://hindi.webdunia.com/religion/religion/hindu/ramcharitmanas/?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/religious-unbelievable-facts?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/religious-article?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/bollywood-hindi-news?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/bollywood-gossip?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/bollywood-movie-review?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/bollywood-article?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/bollywood-movie-preview?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/bollywood-focus?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/dilip-kumar-special?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/bollywood-khul-jaa-sim-sim?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/salman-khan-special?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/sunny-leone-special?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/shahrukh-khan-special?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/indian-television?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/bollywood-celebrity-interview#272?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/entertainment?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/astrology-hindi?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/birthday-astrology?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/astrology-muhurat?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'http://astrology.webdunia.com/hindi/predictions/Predictions.aspx?rashiId=1&rashiMode=1?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/astrology-2019?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/astrology-zodiac-signs?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/lal-kitab?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/astrology-tantra-mantra-yantra?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/vastu-fengshui?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'http://astrology.webdunia.com/hindi/tarot/?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'http://astrology.webdunia.com/hindi/Matchmaking/?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'http://astrology.webdunia.com/hindi/Horoscope/?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'http://hindi.webdunia.com/astrology/ramshalaka/?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'http://hindi.webdunia.com/astrology/choghadia/index.htm?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/astrology-articles?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/learn-astrology?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/astrology-nakshatra-sign?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/astrology-navagraha?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/celibrity-horoscope?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/astrology-gems-stone?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/cricket-news?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/sports-update?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/sports-coverage?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/cricket-score-card?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'http://hindi.webdunia.com/icc-rankings?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/cricket-fixtures?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'http://utilities.webdunia.com/downloadzone.html#wd_ticker?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/hindi-news?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/latest-hindi-news?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/national-hindi-news?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/international-hindi-news?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/regional-hindi-news?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/madhya-pradesh?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/uttar-pradesh?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/crime?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/web-viral?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/latest-cricket-news#568?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/business?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/mobile-news?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/lifestyle?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/health-tips?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/yoga?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/nri#957?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/recipe?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/women?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/kids-world?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/literature?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.com/romance?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://www.youtube.com/user/webduniaindia?utm_source=Top_Nav_Listing&utm_medium=Site_Internal',
        # 'https://hindi.webdunia.comhindi.webdunia.com/channels/list?utm_source=Top_Nav_Listing&utm_medium=Site_Internal'
    ]

    def parse(self, response):
        images = response.xpath(r'//div[@id="contentListingData"]/div//img/@src').extract()
        if images:
            category_id = response.xpath('//input[@id="category_id"]/@value').extract()[0]
            category_creation_id = response.xpath('//input[@id="category_creation_id"]/@value').extract()[0]
            page = '1'
        else:
            images = response.xpath(r'//img/@src').extract()
            category_id = response.meta.get("category_id")
            category_creation_id = response.meta.get("category_creation_id")
            page = response.meta.get("page")
            page = str(int(page) + 1)

        if images:
            image_url = ["https:" + url for url in images]
            item = ImgsItem()
            item["category"] = category_creation_id
            item["image_urls"] = image_url
            yield item

            url = "https://hindi.webdunia.com/core/home-page/more-category-news"
            form_data = {"page": page, "item_per_page": '', "category_id": category_id,
                         "category_creation_id": category_creation_id}
            yield scrapy.FormRequest(url=url, formdata=form_data, meta={"page": page, "category_id": category_id,
                                                                        "category_creation_id": category_creation_id},
                                     callback=self.parse, dont_filter=True)

