import argparse
import boto3
import botocore
import json
import sys
import urllib.request


class LanguageEngine:
    """A class for Natural Language Processing"""


    def __init__(self, region_name, language='en'):
        self._region = region_name
        self._language_code = language
        self._comprehend = boto3.client(
            service_name='comprehend',
            region_name=region_name)


    def get_dominant_language(self, text):
        try:
            json_obj = self._comprehend.detect_dominant_language(
                Text=text)
            result = json.dumps(json_obj['Languages'], sort_keys=True, indent=4)
        except (Exception, botocore.exceptions.EndpointConnectionError) as e:
            result = str(e)
        finally:
            return result


    def get_key_phrases(self, text):
        try:
            json_obj = self._comprehend.detect_key_phrases(
                Text=text,
                LanguageCode=self._language_code)
            result = json.dumps(json_obj['KeyPhrases'], sort_keys=True, indent=4)
        except Exception as e:
            result = e
        finally:
            return result


class LanguageEngineMedical:
    """A class for Natural Language Processing of Medical Information"""


    def __init__(self, region_name, language='en'):
        self._region = region_name
        self._language_code = language
        self._comprehend = boto3.client(
            service_name='comprehendmedical',
            region_name=region_name)


    def get_entities(self, text):
        try:
            result = self._comprehend.detect_entities(
                Text=text)
            entities = result['Entities']
            txt = ''
            for entity in entities:
                txt += f'{json.dumps(entity, sort_keys=True, indent=4)}\n'
        except Exception as e:
            txt = e
        finally:
            return txt.strip()


IDENTITY = json.loads(urllib.request.urlopen('http://169.254.169.254/latest/dynamic/instance-identity/document').read().decode())
AWS_REGION = IDENTITY['region']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', default='')
    args = parser.parse_args()

    if len(args.text) == 0:
        print(f'Usage: {sys.argv[0]} --text "text to analyze"')
        exit()

    LE = LanguageEngine(AWS_REGION)
    txt = LE.get_dominant_language(args.text)
    print('----- Dominant Language -----')
    print(txt)

    txt = LE.get_key_phrases(args.text)
    print('----- Key Phrases -----')
    print(txt)

    LEM = LanguageEngineMedical('us-west-2')
    txt = LEM.get_entities(args.text)
    print('----- Entities (Medical) -----')
    print(txt)

