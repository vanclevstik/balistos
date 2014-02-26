# -*- coding: utf-8 -*-
"""Utils for balistos product"""

import re
import unidecode


def normalized_id(title):
    title = unidecode.unidecode(title).lower()
    return re.sub('\W+', '-', title.replace("'", '')).strip('-')
