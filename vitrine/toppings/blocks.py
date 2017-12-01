# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from .itemtitletopping import ItemTitleTopping


class BlocksTopping(ItemTitleTopping):
    KEY = "blocks.block"
    NAME = "Blocks"
    ITEMS = (("text_id", "ID"),
             ("numeric_id", "Numeric ID"),
             ("name", "Name"),
             ("hardness", "Hardness"))
    ESCAPE_TITLE = False
    PRIORITY = 10

    def SORTING(self, (k, v)):
        if self.diff:
            if v[0] is not None:
                return v[0]["text_id"], k
            else:
                return v[1]["text_id"], k
        else:
            return v["text_id"], k

    def parse_entry(self, entry, key):
        if "display_name" in entry:
            entry["name"] = entry["display_name"]
        elif "name" not in entry:
            entry["name"] = "Unknown"
        if "texture" in entry:
        #    if isinstance(entry['texture'], basestring):
            icon = (-entry['numeric_id'] * 32, 0)
        #    else:
        #        icon = [-entry["texture"][axis] * 32 for axis in ("x", "y")]
            return ('<div title="%s" class="texture" ' +
                    'style="background-position:%spx %spx;"></div>') % (
                        entry["name"], icon[0], icon[1]
                    ), entry["numeric_id"]
        else:
            #class_ = "craftitem large" if entry["id"] < 100 else "craftitem"
            class_ = "craftitem"
            return '<div title="%s" class="%s">%s</div>' % (
                entry["name"], class_, entry["text_id"] if "text_id" in entry else entry["numeric_id"]
            ), entry["text_id"]

    def _get_dl(self, entry):
        aggregate = "<dl>"
        aggregate += "<dt>ID</dt>"
        aggregate += "<dd>%s</dd>" % entry["text_id"]
        if "numeric_id" in entry:
            aggregate += "<dt>Numeric ID</dt>"
            aggregate += "<dd>%s</dd>" % entry["numeric_id"]
        if "name" in entry:
            aggregate += "<dt>Name</dt>"
            aggregate += "<dd>%s</dd>" % entry["name"]
        if "hardness" in entry:
            aggregate += "<dt>Hardness</dt>"
            aggregate += "<dd>%s</dd>" % entry["hardness"]

        if "states" in entry:
            if "num_states" in entry:
                aggregate += "<dt>State IDs</dt>"
                aggregate += "<dd>%s</dd>" % entry["num_states"]
            aggregate += "<dt>States</dt>"
            aggregate += "<dd>%s total<dl>" % len(entry["states"])
            for state in entry["states"]:
                aggregate += "<dt>%s</dt>" % state["name"]
                aggregate += "<dd>"
                if state["type"] in ("direction", "enum"):
                    aggregate += "<br/>".join(state["values"])
                elif state["type"] == "int":
                    aggregate += "[%s...%s]" % (state["min"], state["max"])
                elif state["type"] == "bool":
                    aggregate += "boolean"
                aggregate += "</dd>"
            aggregate += "</dl></dd>"
        aggregate += "</dl>"
        return aggregate