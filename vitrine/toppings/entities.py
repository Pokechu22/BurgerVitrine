# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from .topping import Topping


class EntitiesTopping(Topping):
    KEY = "entities.entity"
    NAME = "Entities"
    ITEMS = (
        ("id", "ID"),
        ("name", "Name"),
        ("display_name", "Display name"),
        ("height", "Height"),
        ("width", "Width"),
        ("texture", "Texture"),
        ("egg_secondary", "Egg foreground"),
        ("egg_primary", "Egg background")
    )
    ESCAPE_TITLE = False
    PRIORITY = 7.2

    def parse_entry(self, entry, key=None):
        name = entry["name"] if "name" in entry else entry["id"]
        if "egg_primary" in entry:
            entry["egg_primary"] = "#%06x" % entry["egg_primary"]
            entry["egg_secondary"] = "#%06x" % entry["egg_secondary"]
            return '%s<div class="color" style="background:%s;"></div><div class="color" style="background:%s;"></div>' % (
                name, entry["egg_primary"], entry["egg_secondary"])
        else:
            return name

    def _get_dl(self, entry):
        parent = Topping._get_dl(self, entry)
        if "metadata" in entry:
            aggregate = "<dt>Metadata</dt>"
            for metadata in entry["metadata"]:
                if metadata["class"] == entry["class"]:
                    source = "Own metadata:"
                elif "entity" in metadata:
                    # Concrete parent
                    source = 'Inhertits from <a href="#%s">%s</a>' % (self.anchor(metadata["entity"]), metadata["entity"])
                else:
                    # Abstract parent
                    source = "Abstract parent:"
                aggregate += "<dd>" + source
                if "data" in metadata:
                    aggregate += "<ol>"
                    for metadata_entry in metadata["data"]:
                        aggregate += '<li value="%d"><a href="#entity_metadata_serializers:%s">%s</a></li>' % (metadata_entry["index"], self._anchor_escape(metadata_entry["serializer"]), metadata_entry["serializer"])
                    aggregate += "</ol>"
                aggregate += "</dd>"
            # Insert before the trailing </dl>
            parent = parent[:parent.index("</dl>")] + aggregate + parent[parent.index("</dl>"):]
        return parent
