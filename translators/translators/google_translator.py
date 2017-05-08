# -*- coding: utf-8 -*-

import re

import HTMLParser
from googleapiclient.discovery import build
import xml.etree.ElementTree as ET


from translator import Translator
from config_parsing import get_key_from_config

re_opening_tag = re.compile(r"<[\s]*[sS]pan[\s]*>(.*)", flags=re.DOTALL)  # <span> tag
re_closing_tag = re.compile(r"(.*?)<[\s]*/[\s]*[sS]pan[\s]*>", flags=re.DOTALL)  # </span> tag


class GoogleTranslator(Translator):

    gt_instance = None

    def __init__(self, source_language, target_language, key=None):
        super(GoogleTranslator, self).__init__(source_language, target_language)

        if not key:
            key = get_key_from_config('GOOGLE_TRANSLATE_API_KEY')

        self.key = key
        self.translation_service = build('translate', 'v2', developerKey=key)

    def translate(self, query, before_context='', after_context='', max_translations=1):
        """
        Translate a query from source language to target language
        :param max_translations: 
        :param after_context: 
        :param before_context: 
        :param query:
        :param source_language:
        :param target_language:
        :return:
        """

        params = {
            'source': self.source_language,
            'target': self.target_language,
            'q': query,
            'format': 'html'
        }

        translations = self.translation_service.translations().list(**params).execute()

        translation = translations['translations'][0][u'translatedText']

        # Unescape HTML characters
        unescaped_translation = HTMLParser.HTMLParser().unescape(translation)

        return unescaped_translation

    def ca_translate(self, query, before_context='', after_context=''):
        """
        Function to translate a query by taking into account the context
        :param query:
        :param source_language:
        :param target_language:
        :param before_context:
        :param after_context:
        :return:
        """
        query = u'%(before_context)s<span>%(query)s</span>%(after_context)s' % locals()  # enclose query in span tags

        translation = self.translate(query, self.source_language, self.target_language)

        translated_query = GoogleTranslator.parse_spanned_string(translation).strip()

        stripped_after_context = after_context.strip()

        if stripped_after_context and translated_query and stripped_after_context[0] in ",;'.\"-" \
                and translated_query[-1] == stripped_after_context[0]:
            translated_query = translated_query[:-1]

        return translated_query

    @staticmethod
    def parse_spanned_string(spanned_string):

        xml_object = ET.fromstring('<s>' + spanned_string.encode('utf-8') + '</s>')

        return xml_object.find('span').text


if __name__ == '__main__':
    g = GoogleTranslator('en', 'de')
    g.ca_translate(
        before_context='The ', query='lion', after_context=' goes to the forrest.')
