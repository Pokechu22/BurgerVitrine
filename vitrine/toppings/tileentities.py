# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from .topping import Topping


class TileEntities(Topping):
    KEY = "tileentity.tileentities"
    NAME = "Tile entities"
    PRIORITY = 7

    def parse_entry(self, entry, key=None):
        return key

    def _get_dl(self, entry):
        aggregate = "<dl>"
        aggregate += "<dt>Name</dt>"
        aggregate += "<dd>%s</dd>" % entry["name"]
        aggregate += "<dt>Network ID</dt>"
        aggregate += "<dd>%s</dd>" % (entry["network_id"] if "network_id" in entry else "N/A")
        if "blocks" in entry:
            aggregate += "<dt>Blocks</dt>"
            aggregate += "<dd>%s</dd>" % ("<br />".join(block for block in entry['blocks']))
        aggregate += "</dl>"
        return aggregate

    def SORTING(self, (k, v)):
        return k, v