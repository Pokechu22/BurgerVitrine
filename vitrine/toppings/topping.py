# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

import json
from html import escape

class Topping(object):
    KEY = None
    NAME = "Unimplemented topping"
    ITEMS = (("json", None),)
    NO_ESCAPE = ()
    ESCAPE_TITLE = True
    PRIORITY = 0

    NO_ENTRIES = '<span class="info">No entries</span>'

    def __init__(self, data, all_data, diff, wiki=None, highlight=None):
        """
        data: data for this topping
        all_data: the entire data set
        diff: True if this is a diff
        wiki: optional wiki to get packet names from
        highlight: optional function that takes code and returns escaped HTML
        """

        self.data = data
        self.all_data = all_data
        self.diff = diff
        self.wiki = wiki
        self.wiki_links = wiki is not None
        self.highlight = highlight or self.escape

    def __str__(self):
        return'<a href="#{1}"><h2 id="{1}">{0}</h2></a>{2}\n'.format(
            self.NAME, self.anchor(), self._parse_data()
        )

    def _parse_data(self):
        aggregate = ""

        if isinstance(self.data, dict):
            if len(self.data) == 0:
                aggregate += self.NO_ENTRIES
            else:
                for key, entry in sorted(self.data.items()):
                    aggregate += self._parse_entry(entry, key)
        elif isinstance(self.data, list):
            if len(self.data) == 0:
                aggregate += self.NO_ENTRIES
            else:
                for entry in sorted(self.data):
                    aggregate += self._parse_entry(entry)
        else:
            aggregate += '<span class="info">Unexpected data</span>'

        return aggregate

    def _parse_entry(self, entry, key=None):
        if self.diff:
            self.side = False
            old = self._get_entry_html(entry[0], key)
            self.side = True
            new = self._get_entry_html(entry[1], key)
            return self._split(old, new)
        else:
            self.side = None
            return self._get_entry_html(entry, key)

    def _get_entry_html(self, entry, key=None):
        if entry is None:
            return '<div class="no entry"></div>\n'
        else:
            anchor = title = self.parse_entry(entry, key)
            links = "".join(self._link(txt, url) for 
                (txt, url) in self.links(entry, key))
            if links is not "":
                links = '<div class="links">%s</div>' % links
            if(isinstance(title, tuple)):
                title, anchor = title
            return self._entry(title, "%s%s" % (links, self._get_dl(entry)),
                               anchor, self.ESCAPE_TITLE)

    def _get_dl(self, entry):
        aggregate = "<dl>"
        post_dl = ""
        for key in self.ITEMS:
            if isinstance(key, tuple):
                new_key = key[1]
                key = key[0]
            else:
                new_key = key
            if key not in entry:
                continue
            value = entry[key]
            if key not in self.NO_ESCAPE:
                value = self.escape(value)
            if new_key is None:
                post_dl += value
            else:
                aggregate += "<dt>%s</dt><dd>%s</dd>" % (
                    self.escape(new_key), value
                )
        return aggregate + "</dl>" + post_dl

    def parse_entry(self, entry, key=None):
        entry["json"] = json.dumps(entry)
        return "NA"

    def links(self, entry, key=None):
        return tuple()
        
    def _link(self, title, url):
        return '<a href="%s">%s</a>' % (url, title);

    def escape(self, string):
        try:
            return escape(str(string))
        except UnicodeEncodeError:
            return "[too cool to be parsed]"

    def _entry(self, title, content, anchor, escape=True):
        if escape:
            title = self.escape(title)
        return ('<div class="entry"><a href="#{2}"><h3 id="{2}">{0}</h3></a>' +
            '<div>{1}</div></div>\n').format(title, content, self.anchor(anchor))

    def _split(self, left, right):
        return ('<div class="split"><div class="left">%s</div>' +
                '<div class="right">%s</div></div>') % (left, right)

    def _anchor_escape(self, string):
        return escape(str(string).lower().replace(" ", "_"))

    def anchor(self, child=None):
        anchor = self._anchor_escape(self.NAME)
        if child is None:
            return anchor
        else:
            return anchor + ":" + self._anchor_escape(child)
