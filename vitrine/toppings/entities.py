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
