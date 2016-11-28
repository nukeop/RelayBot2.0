#-*- coding: utf-8 -*-
def rating_to_stars(rating):
    rating = int(rating)
    return ("★" * rating) + ("☆"*(5-rating))


def minutes_to_hours(minutes):
    return (minutes / 60, minutes % 60)


def has_authority(bot, userid, groupid):
        """Checks if the user has a rank higher than Member in a given group
        """
        permissions = [x for x in bot.user.permissions[userid] if x[0] ==
                       groupid][0][1]
        return (permissions & 3) != 0 #3 bit flag represents owner or officer`
