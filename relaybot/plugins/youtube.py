# -*- coding: utf-8 -*-
import re
import urllib

import requests

import plugin
import util

class YoutubePlugin(plugin.Plugin):
    """Monitors group chat and whenever someone posts a youtube video, it
    fetches info about it and shows it in the group.
    """
    def __init__(self, bot):
        super(YoutubePlugin, self).__init__(bot)
        self.yt_regex = re.compile("(((youtube.*(v=|\/v\/))|(youtu.be/))(?P<ID>[-_a-zA-Z0-9]+))")


    @property
    def description(self):
        return "Shows info about Youtube videos posted by users in group chat."


    def group_chat_hook(self, groupid, userid, message):
        if self.yt_regex.search(message):
            self.bot.user.send_group_msg(groupid, self.get_video_info(message).encode('utf-8'))


    def get_video_info(self, message):
        match = self.yt_regex.search(message)
        yt_id = match.group('ID')

        reply = requests.get("http://youtube.com/get_video_info", params={
            "video_id": yt_id,
            "el": ["vevo", "embedded"]
            })

        if reply.text:
            info = reply.text.encode('utf-8')
            info = urllib.unquote(urllib.unquote(urllib.unquote(info))).decode('utf-8')

            title = self.get_args(info, "title", "&").replace("+", " ")
            rating = util.rating_to_stars(float(self.get_args(info, "avg_rating", "&")))
            length = int(self.get_args(info, "length_seconds", "&"))
            length = "{}:{}".format(length/60, length%60)

            return "{} | {} | {}".format(title, rating, length).decode('utf-8')


    @staticmethod
    def get_args(args, key, query):
        args = args.encode('utf-8')
        try:
            iqs = args.index(query)
            querystring = args[iqs+1:] if (iqs < len(args)-1) else None
            args = {}
            for q in querystring.split("&"):
                try:
                    args[q.strip().split("=")[0]] = q.strip().split("=")[1]
                except IndexError:
                    #If the string doesn't correspond to a key-value pair, we
                    #can simply skip it
                    pass
            return args[key]

        except ValueError:
            return None
