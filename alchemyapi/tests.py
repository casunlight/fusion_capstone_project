#!/usr/bin/env python

#	Copyright 2013 AlchemyAPI
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from __future__ import print_function
from alchemyapi import AlchemyAPI


test_text = 'Bob broke my heart, and then made up this silly sentence to test the PHP SDK'
test_html = '<html><head><title>The best SDK Test | AlchemyAPI</title></head><body><h1>Hello World!</h1><p>My favorite language is PHP</p></body></html>'
test_url = 'http://www.nytimes.com/2013/07/13/us/politics/a-day-of-friction-notable-even-for-a-fractious-congress.html?_r=0'
test_jpg = 'pigeon.jpg'


alchemyapi = AlchemyAPI()


# Entities
print('Checking entities . . . ')
response = alchemyapi.entities('text', test_text)
assert(response['status'] == 'OK')
response = alchemyapi.entities('html', test_html)
assert(response['status'] == 'OK')
response = alchemyapi.entities('url', test_url)
assert(response['status'] == 'OK')
response = alchemyapi.entities('random', test_url)
assert(response['status'] == 'ERROR')  # invalid flavor
print('Entity tests complete!')
print('')


# Keywords
print('Checking keywords . . . ')
response = alchemyapi.keywords('text', test_text)
assert(response['status'] == 'OK')
response = alchemyapi.keywords('html', test_html)
assert(response['status'] == 'OK')
response = alchemyapi.keywords('url', test_url)
assert(response['status'] == 'OK')
response = alchemyapi.keywords('random', test_url)
assert(response['status'] == 'ERROR')  # invalid flavor
print('Keyword tests complete!')
print('')


# Concepts
print('Checking concepts . . . ')
response = alchemyapi.concepts('text', test_text)
assert(response['status'] == 'OK')
response = alchemyapi.concepts('html', test_html)
assert(response['status'] == 'OK')
response = alchemyapi.concepts('url', test_url)
assert(response['status'] == 'OK')
response = alchemyapi.concepts('random', test_url)
assert(response['status'] == 'ERROR')  # invalid flavor
print('Concept tests complete!')
print('')


# Sentiment
print('Checking sentiment . . . ')
response = alchemyapi.sentiment('text', test_text)
assert(response['status'] == 'OK')
response = alchemyapi.sentiment('html', test_html)
assert(response['status'] == 'OK')
response = alchemyapi.sentiment('url', test_url)
assert(response['status'] == 'OK')
response = alchemyapi.sentiment('random', test_url)
assert(response['status'] == 'ERROR')  # invalid flavor
print('Sentiment tests complete!')
print('')


# Targeted Sentiment
print('Checking targeted sentiment . . . ')
response = alchemyapi.sentiment_targeted('text', test_text, 'heart')
assert(response['status'] == 'OK')
response = alchemyapi.sentiment_targeted('html', test_html, 'language')
assert(response['status'] == 'OK')
response = alchemyapi.sentiment_targeted('url', test_url, 'Congress')
assert(response['status'] == 'OK')
response = alchemyapi.sentiment_targeted('random', test_url, 'Congress')
assert(response['status'] == 'ERROR')  # invalid flavor
response = alchemyapi.sentiment_targeted('text', test_text,  None)
assert(response['status'] == 'ERROR')  # missing target
print('Targeted sentiment tests complete!')
print('')


# Text
print('Checking text . . . ')
response = alchemyapi.text('text', test_text)
assert(response['status'] == 'ERROR')  # only works for html and url content
response = alchemyapi.text('html', test_html)
assert(response['status'] == 'OK')
response = alchemyapi.text('url', test_url)
assert(response['status'] == 'OK')
print('Text tests complete!')
print('')


# Text Raw
print('Checking raw text . . . ')
response = alchemyapi.text_raw('text', test_text)
assert(response['status'] == 'ERROR')  # only works for html and url content
response = alchemyapi.text_raw('html', test_html)
assert(response['status'] == 'OK')
response = alchemyapi.text_raw('url', test_url)
assert(response['status'] == 'OK')
print('Raw text tests complete!')
print('')


# Author
print('Checking author . . . ')
response = alchemyapi.author('text', test_text)
assert(response['status'] == 'ERROR')  # only works for html and url content
response = alchemyapi.author('html', test_html)
assert(response['status'] == 'ERROR')  # there's no author in the test HTML
response = alchemyapi.author('url', test_url)
assert(response['status'] == 'OK')
print('Author tests complete!')
print('')


# Language
print('Checking language . . . ')
response = alchemyapi.language('text', test_text)
assert(response['status'] == 'OK')
response = alchemyapi.language('html', test_html)
assert(response['status'] == 'OK')
response = alchemyapi.language('url', test_url)
assert(response['status'] == 'OK')
response = alchemyapi.language('random', test_url)
assert(response['status'] == 'ERROR')  # invalid flavor
print('Language tests complete!')
print('')


# Title
print('Checking title . . . ')
response = alchemyapi.title('text', test_text)
assert(response['status'] == 'ERROR')  # only works for html and url content
response = alchemyapi.title('html', test_html)
assert(response['status'] == 'OK')
response = alchemyapi.title('url', test_url)
assert(response['status'] == 'OK')
print('Title tests complete!')
print('')


# Relations
print('Checking relations . . . ')
response = alchemyapi.relations('text', test_text)
assert(response['status'] == 'OK')
response = alchemyapi.relations('html', test_html)
assert(response['status'] == 'OK')
response = alchemyapi.relations('url', test_url)
assert(response['status'] == 'OK')
response = alchemyapi.relations('random', test_url)
assert(response['status'] == 'ERROR')  # invalid flavor
print('Relation tests complete!')
print('')


# Category
print('Checking category . . . ')
response = alchemyapi.category('text', test_text)
assert(response['status'] == 'OK')
response = alchemyapi.category('html', test_html, {'url': 'test'})
assert(response['status'] == 'OK')
response = alchemyapi.category('url', test_url)
assert(response['status'] == 'OK')
response = alchemyapi.category('random', test_url)
assert(response['status'] == 'ERROR')  # invalid flavor
print('Category tests complete!')
print('')


# Feeds
print('Checking feeds . . . ')
response = alchemyapi.feeds('text', test_text)
assert(response['status'] == 'ERROR')  # only works for html and url content
response = alchemyapi.feeds('html', test_html, {'url': 'test'})
assert(response['status'] == 'OK')
response = alchemyapi.feeds('url', test_url)
assert(response['status'] == 'OK')
print('Feed tests complete!')
print('')


# Microformats
print('Checking microformats . . . ')
response = alchemyapi.microformats('text', test_text)
assert(response['status'] == 'ERROR')  # only works for html and url content
response = alchemyapi.microformats('html', test_html, {'url': 'test'})
assert(response['status'] == 'OK')
response = alchemyapi.microformats('url', test_url)
assert(response['status'] == 'OK')
print('Microformat tests complete!')
print('')
print('')

# imagetagging
print('Checking imagetagging . . . ')
response = alchemyapi.imageTagging('text', test_text)
assert(response['status'] == 'ERROR')
response = alchemyapi.imageTagging('html', test_html)
assert(response['status'] == 'ERROR')
response = alchemyapi.imageTagging('url', test_url)
assert(response['status'] == 'OK')
response = alchemyapi.imageTagging('image', test_jpg)
assert(response['status'] == 'OK')
print('Image tagging tests complete!')
print('')
print('')

# combined
print('Checking combined . . . ')
response = alchemyapi.combined('text', test_text)
assert(response['status'] == 'OK')
response = alchemyapi.combined('html', test_html)
assert(response['status'] == 'ERROR')
response = alchemyapi.combined('url', test_url)
assert(response['status'] == 'OK')
print('Combined tests complete!')
print('')
print('')

# taxonomy
print('Checking taxonomy . . . ')
response = alchemyapi.taxonomy('text', test_text)
assert(response['status'] == 'OK')
response = alchemyapi.taxonomy('html', test_html, {'url': 'test'})
assert(response['status'] == 'OK')
response = alchemyapi.taxonomy('url', test_url)
assert(response['status'] == 'OK')
print('Taxonomy tests complete!')
print('')
print('')

# image
print('Checking image extraction . . . ')
response = alchemyapi.imageExtraction('text', test_text)
assert(response['status'] == 'ERROR')
response = alchemyapi.imageExtraction('html', test_html)
assert(response['status'] == 'ERROR')
response = alchemyapi.imageExtraction('url', test_url)
assert(response['status'] == 'OK')
print('Image Extraction tests complete!')
print('')
print('')


print('**** All tests complete! ****')
