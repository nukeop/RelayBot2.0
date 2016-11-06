#-*- coding: utf-8 -*-
def rating_to_stars(rating):
    rating = int(rating)
    return ("★" * rating) + ("☆"*(5-rating))
