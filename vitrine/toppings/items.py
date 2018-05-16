# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from .itemtitletopping import ItemTitleTopping


class ItemsTopping(ItemTitleTopping):
    KEY = "items.item"
    NAME = "Items"
    ITEMS = (("text_id", "ID"),
             ("numeric_id", "Numeric ID"),
             ("display_name", "Name"),
             ("max_stack_size", "Max Stack Size"))
    SORTING = ItemTitleTopping.NUMERIC_SORT
    ESCAPE_TITLE = False
    PRIORITY = 9

    def parse_entry(self, entry, key):
        if "display_name" in entry:
            title = entry["display_name"]
        elif "name" in entry:
            title = entry["name"]
        else:
            assert "text_id" in entry
            title = entry["text_id"]
        if "icon" in entry:
        #if True:
            #if isinstance(entry['icon'], basestring):
            icon = (-(entry['numeric_id'] % 1800 - 256) * 32, 0)
        #    else:
        #        icon = tuple(-entry["icon"][axis] * 32 for axis in ("x", "y"))
            style = 'background-position:%spx %spx;' % icon
        else:
            style = 'background-image:none;'
        return ('<div class="item" title="%s" ' +
                'style="%s"></div>') % (
                    title, style
                ), entry["text_id"]
