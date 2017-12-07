# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from .topping import Topping


class TagsTopping(Topping):
    KEY = "tags"
    NAME = "Tags"
    PRIORITY = 8.5

    def parse_entry(self, entry, key=None):
        return entry["name"]

    def _get_dl(self, entry):
        aggregate = "<dl>"
        aggregate += "<dt>Type</dt>"
        aggregate += "<dd>%s</dd>" % entry["type"]
        aggregate += "<dt>Name</dt>"
        aggregate += "<dd>%s</dd>" % entry["name"]
        aggregate += "<dt>Values</dt>"
        aggregate += "<dd>%s</dd>" % (
            "<br/>".join([self.make_internal_link(entry["type"], val) for val in entry["values"]])
        )
        aggregate += "</dl>"
        return aggregate

    def make_internal_link(self, group, id):
        if id.startswith("minecraft:"):
            id = id[len("minecraft:"):]
        anchor = self._anchor_escape(group) + ":" + self._anchor_escape(id)
        return "<a href=\"#%s\">%s</a>" % (anchor, id)