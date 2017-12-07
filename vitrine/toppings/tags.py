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
        return key

    def _get_dl(self, entry):
        aggregate = "<dl>"
        for k, v in entry.iteritems():
            aggregate += "<dt>%s</dt>" % k
            aggregate += "<dd>%s</dd>" % (
                "<br/>".join([self.make_internal_link(v["type"], val) for val in v["values"]])
            )
        aggregate += "</dl>"
        return aggregate

    def make_internal_link(self, group, id):
        if id.startswith("minecraft:"):
            id = id[len("minecraft:"):]
        anchor = self._anchor_escape(group) + ":" + self._anchor_escape(id)
        return "<a href=\"#%s\">%s</a>" % (anchor, id)