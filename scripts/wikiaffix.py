# This file is part of MedAffix.
#
# MedAffix is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MedAffix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MedAffix.  If not, see <http://www.gnu.org/licenses/>.
__author__ = 'Aleksandar Savkov'

import re
import warnings
import urllib2
from BeautifulSoup import BeautifulSoup
from os import makedirs


def get_next_cat_page(soup, affix_type):
    atags = soup.findAll(name='a',
                         attrs={'title': 'Category:English %ses' % affix_type})
    urls = [x['href'] for x in atags if 'next 200' in x.string and x['href']]
    if len(urls) > 2:
        warnings.warn('There is more than two url candidates.')
    elif len(urls) == 0:
        return None
    return 'https://en.wiktionary.org/%s' % urls[0]


def scrape_category(url, affix_type=None):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    next_url = get_next_cat_page(soup, affix_type) if affix_type else None
    atags = soup.findAll(name='a')
    affixes = [x['title']
               for x
               in atags
               if x.has_key('title') and re.match('^[a-z-]+$', x['title'])]
    if next_url:
        affixes.extend(scrape_category(next_url, affix_type))
    return affixes


# output folder
dp = 'data/'

# make sure folder exists
try:
    makedirs(dp)
except OSError:
    pass  # dir exists

# output files
hiphen_affix_path = '%s/wikiaffix_with_hiphens.txt' % dp
affix_path = '%s/wikiaffix.txt' % dp
suffix_path = '%s/wikisuffix.txt' % dp
prefix_path = '%s/wikiprefix.txt' % dp
vsfxp = '%s/wikiverbsuffix.txt' % dp
nsfxp = '%s/wikinounsuffix.txt' % dp
asfxp = '%s/wikiadjsuffix.txt' % dp
rsfxp = '%s/wikiadvsuffix.txt' % dp
isfxp = '%s/wikiinflsuffix.txt' % dp

# Wiktionary Category URLs
suff_url = 'https://en.wiktionary.org/wiki/Category:English_suffixes'
pref_url = 'https://en.wiktionary.org/wiki/Category:English_prefixes'
verb_url = 'https://en.wiktionary.org/wiki/Category:' \
           'English_verb-forming_suffixes'
noun_url = 'https://en.wiktionary.org/wiki/Category:' \
           'English_noun-forming_suffixes'
infl_url = 'https://en.wiktionary.org/wiki/Category:' \
           'English_inflectional_suffixes'
adv_url = 'https://en.wiktionary.org/wiki/Category:' \
          'English_adverb-forming_suffixes'
adj_url = 'https://en.wiktionary.org/wiki/Category:' \
          'English_adjective-forming_suffixes'

# scraping the categories
sfxs = scrape_category(suff_url, affix_type='suffix')
prfxs = scrape_category(pref_url, affix_type='prefix')

# scraping the subcategories
vsfxs = scrape_category(verb_url)  # forming verbs
nsfxs = scrape_category(noun_url)  # forming nouns
isfxs = scrape_category(infl_url)  # inflectional
asfxs = scrape_category(adv_url)  # forming adjectives
rsfxs = scrape_category(adj_url)  # forming adverbs


# writing to files
with open(hiphen_affix_path, 'w') as f:
    f.write('\n'.join(sfxs + prfxs))
with open(affix_path, 'w') as f:
    f.write('\n'.join([x.replace('-', '') for x in sfxs + prfxs]))
with open(prefix_path, 'w') as f:
    f.write('\n'.join([x.replace('-', '') for x in prfxs if x.endswith('-')]))
with open(suffix_path, 'w') as f:
    f.write('\n'.join([x.replace('-', '') for x in sfxs if x.startswith('-')]))
with open(vsfxp, 'w') as f:
    f.write('\n'.join([x.replace('-', '') for x in vsfxs if x.startswith('-')]))
with open(nsfxp, 'w') as f:
    f.write('\n'.join([x.replace('-', '') for x in nsfxs if x.startswith('-')]))
with open(isfxp, 'w') as f:
    f.write('\n'.join([x.replace('-', '') for x in isfxs if x.startswith('-')]))
with open(asfxp, 'w') as f:
    f.write('\n'.join([x.replace('-', '') for x in asfxs if x.startswith('-')]))
with open(rsfxp, 'w') as f:
    f.write('\n'.join([x.replace('-', '') for x in rsfxs if x.startswith('-')]))