# -*- coding: utf8 -*-
import unittest
from unittest import TestCase
from translators import GoogleTranslator


class TestGoogleTranslator(TestCase):
    def setUp(self):
        self.translators = {
            'en-nl': GoogleTranslator('en', 'nl'),
            'es-en': GoogleTranslator('es', 'en'),
            'de-en': GoogleTranslator('de', 'en'),
            'en-de': GoogleTranslator('en', 'de')
        }

    def testContextMatters(self):
        translation = self.translators['en-nl'].ca_translate(before_context='Dark',
                                                             query='matter',
                                                             after_context='is to be found in the universe')

        self.assertEqual(translation, 'materie')

    def testSuffixIsEmpty(self):
        translation = self.translators['es-en'].ca_translate(before_context='Estoy en la',
                                                             query='cama',
                                                             after_context='')
        self.assertEqual(translation, 'bed')

    def testUnicodeCharactersInContext(self):
        translation = self.translators['de-en'].ca_translate(before_context='Ein',
                                                             query='klein',
                                                             after_context=u'löwe')

        self.assertEqual(translation, "small")

    def testUnicodeCharactersInWordToTranslate(self):
        translation = self.translators['de-en'].ca_translate(before_context=u'Die schön',
                                                             query=u'löwen',
                                                             after_context=u' geht zum Wald'
                                                             )

        self.assertIn(translation, ['lion', 'beautiful lion'])

    def testUnicodeInResult(self):
        translation = self.translators['en-de'].ca_translate(before_context='The ',
                                                             query='lion',
                                                             after_context=' goes to the forrest.')

        self.assertEqual(translation, u'Löwe')

    def testSuffixStartsWithPunctuation(self):
        translation = self.translators['es-en'].ca_translate(before_context='Estoy en la',
                                                             query='cama',
                                                             after_context=', e soy dormiendo')

        self.assertEqual(translation, 'bed')

        translation = self.translators['es-en'].ca_translate(before_context='Estoy en la',
                                                             query='cama',
                                                             after_context=' , e soy dormiendo')
        self.assertEqual(translation, 'bed')

    def testQueryEndsWithPunctuation(self):
        translation = self.translators['es-en'].ca_translate(before_context='Estoy en la',
                                                             query='cama,',
                                                             after_context=' e soy dormiendo')

        self.assertIn(translation, ['bed,', 'bed'])

    def test_strange_span_in_return(self):
        translation = self.translators['de-en'].ca_translate(before_context='Ich hatte mich',
                                                             query='eigentlich schon',
                                                             after_context=' mit dem 1:1-Unentschieden abgefunden')
        assert "</span>" not in translation

    def test_escaped_characters_in_translation(self):
        translation = self.translators['de-en'].ca_translate(
            before_context=u'Um Fernbusse aus dem Geschäft zu drängen, hat das Unternehmen damit begonnen, das',
            query='konzerneigene Flaggschiff',
            after_context=u'ICE straßentauglich zu machen. ')

        self.assertNotIn('&#39;', translation)


if __name__ == '__main__':
    unittest.main()
