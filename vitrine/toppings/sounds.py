# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from .topping import Topping


class SoundsTopping(Topping):
    KEY = "sounds"
    NAME = "Sounds"
    PRIORITY = 3.5
    RESOURCES_SITE = "https://resources.download.minecraft.net/%s/%s"

    def parse_entry(self, entry, key=None):
        return entry["name"]

    def _get_dl(self, entry):
        aggregate = "<dl>"
        aggregate += "<dt>Name</dt>"
        aggregate += "<dd>%s</dd>" % entry["name"]
        aggregate += "<dt>ID</dt>"
        aggregate += "<dd>%s</dd>" % entry["id"]
        if "field" in entry:
            aggregate += "<dt>Field</dt>"
            aggregate += "<dd>%s</dd>" % entry["field"]
        if "subtitle_key" in entry:
            aggregate += "<dt>Subtitle key</dt>"
            aggregate += "<dd>%s</dd>" % entry["subtitle_key"]
        if "subtitle" in entry:
            aggregate += "<dt>Subtitle</dt>"
            aggregate += "<dd>%s</dd>" % entry["subtitle"]
        if "sounds" in entry:
            aggregate += "<dt>Sounds (%s)</dt>" % len(entry["sounds"])
            aggregate += "<dd>%s</dd>" % (
                "<br/>".join([self.make_sound_link(sound) for sound in entry["sounds"]])
            )
        aggregate += "</dl>"
        return aggregate

    def make_sound_link(self, sound):
        """Makes a link for the given sound variant"""
        sound_name = sound["name"]
        if "hash" in sound:
            sound_hash = sound["hash"]
            link = self.RESOURCES_SITE % (sound_hash[0:2], sound_hash)
            extra_info = ""
            if "pitch" in sound and sound["pitch"] != 1:
                pitch_data = " data-pitch=\"%s\"" % sound["pitch"]
                extra_info = "Pitch %s" % sound["pitch"]
            else:
                pitch_data = ""
            if "volume" in sound and sound["volume"] != 1:
                volume_data = " data-volume=\"%s\"" % sound["volume"]
                if extra_info != "":
                    extra_info += ", "
                extra_info += "Volume %s" % sound["volume"]
            else:
                volume_data = ""
            if extra_info != "":
                extra_info = "<br>(" + extra_info + ")"
            a_tag = "<a title=\"%s\" href=\"%s\">%s</a>" % (sound_hash, link, sound_name)
            play_button = "<span><button data-link=\"%s\"%s%s onclick=\"playSound(this)\">Play</button></span>" % (link, pitch_data, volume_data)
            return a_tag + extra_info + play_button
        else:
            return sound_name
