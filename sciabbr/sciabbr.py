# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
import sqlite3 as sql
from collections import namedtuple


Recd = namedtuple('Recd', ('full', 'abbr', 'lang', 'type'))


db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abbrv.db')
conn = sql.connect(db_path)
cur = conn.cursor()


def abbreviate(word):
    is_capital = word[0].isupper()
    recds = [Recd(*abbr) for abbr in
             cur.execute('select * from abbrvs where ? like full', (word,))]
    if not recds and word[-1] == 's':
        recds = [Recd(*abbr) for abbr in
                 cur.execute('select * from abbrvs where ? like full', (word[:-1],))]
    if recds:
        if len(recds) > 1:
            fulls = [r for r in recds if r.type == 0]
            if len(fulls) == 1:
                # if only one non-affix abbreviation
                recds = fulls
            elif all(r.abbr == recds[0].abbr for r in recds):
                # if all abbreviations equivalent
                pass
            else:
                for recd in recds:
                    print(recd)
                raise Exception('Multiple nonequivalent abbreviations possible')
        abbr = recds[0].abbr
        if abbr != 'n.a.':
            word = abbr
        return word.capitalize() if is_capital else word
    else:
        return word
