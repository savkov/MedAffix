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
from os import makedirs
from pandas.io.html import read_html

# output folder
dp = 'data/'

# make sure folder exists
try:
    makedirs(dp)
except OSError:
    pass  # dir exists

# output files
hiphen_affix_path = '%s/medaffix_with_hiphens.txt' % dp
affix_path = '%s/medaffix.txt' % dp
suffix_path = '%s/medsuffix.txt' % dp
prefix_path = '%s/medprefix.txt' % dp

# Wikipedia URL
url = 'http://en.wikipedia.org/wiki/List_of_medical_roots,_' \
      'suffixes_and_prefixes'

# parsed tables at this URL
tables = read_html(url, attrs={'class': 'wikitable'}, header=0)

# names of interesting columns in the tables
regular_keys = [
    'Affix',
    'Greek root in English',
    'Latin root in English',
    'Other root in English'
]

# former names of interesting columns
# in case they are restored in the future
ignoramus_keys = [
    'Preffix or suffix',
    'Preffix/suffix'
]

# all column names
keys = regular_keys + ignoramus_keys

# affix entries
entries = []

# collecting all entries
for t in tables:
    for k in keys:
        try:
            entries.extend(t[k])
        except KeyError:
            pass  # no biggie: not all keys and tables are interesting

# processed affixes
terms = []

for e in entries:
    # check for empty entries
    if len(e) < 2:
        continue
    # split possible comma separated sub-entries and clean them
    sub_entries = map(lambda x: x.strip(), e.split(','))

    # expanding all entries with longer forms in braces
    # e.g. cry(o)- => cry-, cryo-
    for se in sub_entries:
        if re.search('\([^\)]+\)', se):
            short_entry = re.sub('\([^\)]+\)', '', se).split(' ')[0]
            long_entry = re.sub(r'\(([^\)]+)\)', r'\1', se).split(' ')[0]
            if short_entry:
                terms.append(short_entry)
            if long_entry:
                terms.append(long_entry)
        elif se:
            terms.append(se.split(' ')[0])

# writing to files
with open(hiphen_affix_path, 'w') as f:
    f.write('\n'.join(terms))
with open(affix_path, 'w') as f:
    f.write('\n'.join([x.replace('-', '') for x in terms]))
with open(prefix_path, 'w') as f:
    f.write('\n'.join([x.replace('-', '') for x in terms if x.endswith('-')]))
with open(suffix_path, 'w') as f:
    f.write('\n'.join([x.replace('-', '') for x in terms if x.startswith('-')]))