# -*- coding: utf-8 -*-
import scrapy


class TranslateEasyRussianSpider(scrapy.Spider):
    name = 'translate_easy_russian'
    allowed_domains = ['easypronunciation.com']
    start_urls = ['https://easypronunciation.com/']

    def start_requests(self):
        url = "https://easypronunciation.com/zh/russian-phonetic-transcription-converter"

        headers = {
            "Cookie": 'PHPSESSID=987c252f057c5753550091a7f03ca404; text_length_today=0; text_length_today_time=1584097367; unique_cookie_id=0850ceb13e92301b253ef757cf4f75c3; _ga=GA1.2.128044801.1584097371; _gid=GA1.2.841991531.1584097371; _gat=1',
            'Referer': "https://easypronunciation.com/zh/russian-phonetic-transcription-converter",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",

        }

        form_data = {
            'initial_text': "пожалуйста",
            'Convert_to_russian': "IPA",
            'Display': 'above_each_word',
            'line_break': 'p_tag',
            'click_the_word_phonetic_symbols': 'on',
            'click_the_word_audio_video': 'on',
            'frequency_rating_russian': 'russian_subtitles',
            'spell_the_numbers': 'on',
            'show_cheat_sheet_button': 'on',
            'MM_update2': 'form2',
        }
        yield scrapy.FormRequest(url=url, formdata=form_data, headers=headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
        with open('easy.html', 'w', encoding='utf8')as f:
            f.write(response.text)
