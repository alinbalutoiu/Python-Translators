from translator import Translator
import urllib
import requests


class GlosbeTranslator(Translator):

    API_BASE_URL = 'https://glosbe.com/gapi/translate?'

    def translate(self, query, source_language, target_language, max_translations=2):

        # Construct url
        api_url = GlosbeTranslator.build_url(query, source_language, target_language)

        # Send request
        response = requests.get(api_url).json()['tuc']

        # Extract the translations
        translations = [translation['phrase']['text'] for translation in response[:max_translations]]

        return translations

    @staticmethod
    def build_url(query, source_language, target_language):
        query_params = {
            'from': source_language,
            'dest': target_language,
            'format': 'json',
            'phrase': query
        }

        return GlosbeTranslator.API_BASE_URL + urllib.urlencode(query_params)