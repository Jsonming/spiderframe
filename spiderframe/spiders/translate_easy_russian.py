# -*- coding: utf-8 -*-
import scrapy


class TranslateEasyRussianSpider(scrapy.Spider):
    name = 'translate_easy_russian'
    allowed_domains = ['easypronunciation.com']
    start_urls = ['https://easypronunciation.com/']

    def start_requests(self):
        url = "https://easypronunciation.com/zh/russian-phonetic-transcription-converter"
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
        yield scrapy.FormRequest(url=url, formdata=form_data, callback=self.parse, dont_filter=True)

    def parse(self, response):
        with open('easy.html', 'w', encoding='utf8')as f:
            f.write(response.text)
