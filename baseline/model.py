"""
Modeling users, interactions and items from
the recsys challenge 2017.

by Daniel Kohlsdorf
"""

import math

class User:
    def __init__(self, id, jobroles, clevel, disc, indus, expn, expy,
                 expyc, edud, edufos, country, region, xtcj, premium):
        self.id = id
        self.jobroles = jobroles
        self.clevel = clevel
        self.disc = disc
        self.indus = indus
        self.expn = expn
        self.expy = expy
        self.expyc = expyc
        self.edud = edud
        self.edufos = edufos
        self.country = country
        self.region = region
        self.xtcj = xtcj
        self.premium = premium
        self.CBF_weights = {}
        self.interacted_with = {}


class Item:
    def __init__(self, id, title, tags, clevel, indus, disc,
                 country, region, paid, lat, lon, etype, time):
        self.id = id
        self.title = title
        self.tags = tags
        self.disc = disc
        self.indus = indus
        self.clevel = clevel
        self.country = country
        self.region = region
        self.paid = paid
        self.lat = lat
        self.lon = lon
        self.etype = etype
        self.time = time
        self.CBF_weights = {}
        self.interacted_with = {}


class Interaction:
    def __init__(self, i_type, time):
        self.i_type = i_type
        self.time = time


class Interactions:
    def __init__(self, user, item, interactions, data):
        self.user = user
        self.item = item
        self.interactions = interactions
        self.country = data[0]
        self.lat = data[1]
        self.lon = data[2]
        self.user_concepts = data[3]
        self.item_concepts = data[4]

    ### BASELINE FEATURES
    def clevel_match(self):
        if self.user.clevel == self.item.clevel:
            return 1.0
        else:
            return 0.0

    def indus_match(self):
        if self.user.indus == self.item.indus:
            return 1.0
        else:
            return 0.0

    def discipline_match(self):
        if self.user.disc == self.item.disc:
            return 1.0
        else:
            return 0.0

    def country_match(self):
        if self.user.country == self.item.country:
            return 1.0
        else:
            return 0.0

    def region_match(self):
        if self.user.region == self.item.region:
            return 1.0
        else:
            return 0.0

    ### Interaction features ##########################################

    def interaction0_titletags(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            intersect = set(self.item.title)
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].tags))/(len(intersect.union(items[i].tags))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction0_tagstitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.tags)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].title))/(len(intersect.union(items[i].title))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction0_titletitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.title)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].title))/(len(intersect.union(items[i].title))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction0_tagstags(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.tags)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].tags))/(len(intersect.union(items[i].tags))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction0_clevel(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].clevel == self.item.clevel:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction0_disc(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].disc == self.item.disc:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction0_indus(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].indus == self.item.indus:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction0_region(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].region == self.item.region:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction0_country(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].country == self.item.country:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction0_etype(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].etype == self.item.etype:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction0_distance(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
        length = len(interacted_with)
        if length != 0 and self.item.lat is not None and self.item.lon is not None:
            sim = 0.0
            (lat1, lon1) = (self.item.lat, self.item.lon)
            radius = 6371
            for i in interacted_with:
                (lat2, lon2) = (items[i].lat, items[i].lon)
                dlat = math.radians(lat2-lat1)
                dlon = math.radians(lon2-lon1)
                a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
                sim += radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
            return sim/len(interacted_with)
        else:
            return 100000.0

    def interaction0_clevel_change(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                sim += ((items[i].clevel - self.item.clevel)/10)+0.5
            return sim/len(interacted_with)
        else:
            return 0.5

    def interaction1_titletags(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            intersect = set(self.item.title)
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].tags))/(len(intersect.union(items[i].tags))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction1_tagstitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.tags)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].title))/(len(intersect.union(items[i].title))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction1_titletitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.title)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].title))/(len(intersect.union(items[i].title))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction1_tagstags(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.tags)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].tags))/(len(intersect.union(items[i].tags))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction1_clevel(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].clevel == self.item.clevel:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction1_disc(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].disc == self.item.disc:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction1_indus(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].indus == self.item.indus:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction1_region(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].region == self.item.region:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction1_country(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].country == self.item.country:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction1_etype(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].etype == self.item.etype:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction1_distance(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
        length = len(interacted_with)
        if length != 0 and self.item.lat is not None and self.item.lon is not None:
            sim = 0.0
            (lat1, lon1) = (self.item.lat, self.item.lon)
            radius = 6371
            for i in interacted_with:
                (lat2, lon2) = (items[i].lat, items[i].lon)
                dlat = math.radians(lat2-lat1)
                dlon = math.radians(lon2-lon1)
                a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
                sim += radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
            return sim/len(interacted_with)
        else:
            return 100000.0

    def interaction1_clevel_change(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                sim += ((items[i].clevel - self.item.clevel)/10)+0.5
            return sim/len(interacted_with)
        else:
            return 0.5

    def interaction2_titletags(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            intersect = set(self.item.title)
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].tags))/(len(intersect.union(items[i].tags))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction2_tagstitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.tags)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].title))/(len(intersect.union(items[i].title))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction2_titletitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.title)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].title))/(len(intersect.union(items[i].title))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction2_tagstags(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.tags)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].tags))/(len(intersect.union(items[i].tags))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction2_clevel(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].clevel == self.item.clevel:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction2_disc(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].disc == self.item.disc:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction2_indus(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].indus == self.item.indus:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction2_region(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].region == self.item.region:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction2_country(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].country == self.item.country:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction2_etype(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].etype == self.item.etype:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction2_distance(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
        length = len(interacted_with)
        if length != 0 and self.item.lat is not None and self.item.lon is not None:
            sim = 0.0
            (lat1, lon1) = (self.item.lat, self.item.lon)
            radius = 6371
            for i in interacted_with:
                (lat2, lon2) = (items[i].lat, items[i].lon)
                dlat = math.radians(lat2-lat1)
                dlon = math.radians(lon2-lon1)
                a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
                sim += radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
            return sim/len(interacted_with)
        else:
            return 100000.0

    def interaction2_clevel_change(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                sim += ((items[i].clevel - self.item.clevel)/10)+0.5
            return sim/len(interacted_with)
        else:
            return 0.5

    def interaction3_titletags(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            intersect = set(self.item.title)
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].tags))/(len(intersect.union(items[i].tags))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction3_tagstitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.tags)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].title))/(len(intersect.union(items[i].title))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction3_titletitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.title)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].title))/(len(intersect.union(items[i].title))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction3_tagstags(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.tags)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].tags))/(len(intersect.union(items[i].tags))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction3_clevel(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].clevel == self.item.clevel:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction3_disc(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].disc == self.item.disc:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction3_indus(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].indus == self.item.indus:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction3_region(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].region == self.item.region:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction3_country(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].country == self.item.country:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction3_etype(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].etype == self.item.etype:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction3_distance(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
        length = len(interacted_with)
        if length != 0 and self.item.lat is not None and self.item.lon is not None:
            sim = 0.0
            (lat1, lon1) = (self.item.lat, self.item.lon)
            radius = 6371
            for i in interacted_with:
                (lat2, lon2) = (items[i].lat, items[i].lon)
                dlat = math.radians(lat2-lat1)
                dlon = math.radians(lon2-lon1)
                a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
                sim += radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
            return sim/len(interacted_with)
        else:
            return 100000.0

    def interaction3_clevel_change(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                sim += ((items[i].clevel - self.item.clevel)/10)+0.5
            return sim/len(interacted_with)
        else:
            return 0.5

    def interaction4_titletags(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            intersect = set(self.item.title)
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].tags))/(len(intersect.union(items[i].tags))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction4_tagstitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.tags)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].title))/(len(intersect.union(items[i].title))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction4_titletitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.title)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].title))/(len(intersect.union(items[i].title))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction4_tagstags(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.tags)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].tags))/(len(intersect.union(items[i].tags))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction4_clevel(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].clevel == self.item.clevel:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction4_disc(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].disc == self.item.disc:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction4_indus(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].indus == self.item.indus:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction4_region(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].region == self.item.region:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction4_country(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].country == self.item.country:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction4_etype(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].etype == self.item.etype:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction4_distance(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
        length = len(interacted_with)
        if length != 0 and self.item.lat is not None and self.item.lon is not None:
            sim = 0.0
            (lat1, lon1) = (self.item.lat, self.item.lon)
            radius = 6371
            for i in interacted_with:
                (lat2, lon2) = (items[i].lat, items[i].lon)
                dlat = math.radians(lat2-lat1)
                dlon = math.radians(lon2-lon1)
                a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
                sim += radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
            return sim/len(interacted_with)
        else:
            return 100000.0
        
    def interaction4_clevel_change(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                sim += ((items[i].clevel - self.item.clevel)/10)+0.5
            return sim/len(interacted_with)
        else:
            return 0.5
        
    def interaction5_titletags(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            intersect = set(self.item.title)
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].tags))/(len(intersect.union(items[i].tags))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction5_tagstitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.tags)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].title))/(len(intersect.union(items[i].title))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction5_titletitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.title)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].title))/(len(intersect.union(items[i].title))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction5_tagstags(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            intersect = set(self.item.tags)
            sim = 0.0
            for i in interacted_with:
                sim += len(intersect.intersection(items[i].tags))/(len(intersect.union(items[i].tags))+1)
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction5_clevel(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].clevel == self.item.clevel:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction5_disc(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].disc == self.item.disc:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction5_indus(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].indus == self.item.indus:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction5_region(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].region == self.item.region:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction5_country(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].country == self.item.country:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction5_etype(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                if items[i].etype == self.item.etype:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction5_distance(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
        length = len(interacted_with)
        if length != 0 and self.item.lat is not None and self.item.lon is not None:
            sim = 0.0
            (lat1, lon1) = (self.item.lat, self.item.lon)
            radius = 6371
            for i in interacted_with:
                (lat2, lon2) = (items[i].lat, items[i].lon)
                dlat = math.radians(lat2-lat1)
                dlon = math.radians(lon2-lon1)
                a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
                sim += radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
            return sim/len(interacted_with)
        else:
            return 100000.0

    def interaction5_clevel_change(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            sim = 0.0
            for i in interacted_with:
                sim += ((items[i].clevel - self.item.clevel)/10)+0.5
            return sim/len(interacted_with)
        else:
            return 0.5


    ### Temporal interactions #################################################

    def recent0_titletags(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/(len(intersect.union(interact.tags))+1)
        return 0.0

    def recent0_tagstitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.title))/(len(intersect.union(interact.title))+1)
        else:
            return 0.0

    def recent0_titletitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.title))/(len(intersect.union(interact.title))+1)
        return 0.0

    def recent0_tagstags(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/(len(intersect.union(interact.tags))+1)
        else:
            return 0.0

    def recent0_clevel(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].clevel == self.item.clevel:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent0_disc(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].disc == self.item.disc:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent0_indus(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].indus == self.item.indus:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent0_region(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].region == self.item.region:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent0_country(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].country == self.item.country:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent0_etype(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].etype == self.item.etype:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent0_distance(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
        if len(interacted_with) != 0 and self.item.lat is not None and self.item.lon is not None:
            (lat1, lon1) = (self.item.lat, self.item.lon)
            radius = 6371
            (lat2, lon2) = (items[interacted_with[0]].lat, items[interacted_with[0]].lon)
            dlat = math.radians(lat2-lat1)
            dlon = math.radians(lon2-lon1)
            a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
            return radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
        else:
            return 100000.0

    def recent0_clevel_change(self, items):
        interacted_with = [x for x in self.user.interacted_with[0] if x != self.item.id]
        if len(interacted_with) != 0:
            return ((items[interacted_with[0]].clevel - self.item.clevel)/10)+0.5
        else:
            return 0.5

    def recent1_titletags(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/(len(intersect.union(interact.tags))+1)
        return 0.0

    def recent1_tagstitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.title))/(len(intersect.union(interact.title))+1)
        else:
            return 0.0

    def recent1_titletitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.title))/(len(intersect.union(interact.title))+1)
        return 0.0

    def recent1_tagstags(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/(len(intersect.union(interact.tags))+1)
        else:
            return 0.0

    def recent1_clevel(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].clevel == self.item.clevel:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent1_disc(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].disc == self.item.disc:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent1_indus(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].indus == self.item.indus:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent1_region(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].region == self.item.region:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent1_country(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].country == self.item.country:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent1_etype(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].etype == self.item.etype:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent1_distance(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
        if len(interacted_with) != 0 and self.item.lat is not None and self.item.lon is not None:
            (lat1, lon1) = (self.item.lat, self.item.lon)
            radius = 6371
            (lat2, lon2) = (items[interacted_with[0]].lat, items[interacted_with[0]].lon)
            dlat = math.radians(lat2-lat1)
            dlon = math.radians(lon2-lon1)
            a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
            return radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
        else:
            return 100000.0

    def recent1_clevel_change(self, items):
        interacted_with = [x for x in self.user.interacted_with[1] if x != self.item.id]
        if len(interacted_with) != 0:
            return ((items[interacted_with[0]].clevel - self.item.clevel)/10)+0.5
        else:
            return 0.5

    def recent2_titletags(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/(len(intersect.union(interact.tags))+1)
        return 0.0

    def recent2_tagstitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.title))/(len(intersect.union(interact.title))+1)
        else:
            return 0.0

    def recent2_titletitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.title))/(len(intersect.union(interact.title))+1)
        return 0.0

    def recent2_tagstags(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/(len(intersect.union(interact.tags))+1)
        else:
            return 0.0

    def recent2_clevel(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].clevel == self.item.clevel:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent2_disc(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].disc == self.item.disc:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent2_indus(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].indus == self.item.indus:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent2_region(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].region == self.item.region:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent2_country(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].country == self.item.country:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent2_etype(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].etype == self.item.etype:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent2_distance(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
        if len(interacted_with) != 0 and self.item.lat is not None and self.item.lon is not None:
            (lat1, lon1) = (self.item.lat, self.item.lon)
            radius = 6371
            (lat2, lon2) = (items[interacted_with[0]].lat, items[interacted_with[0]].lon)
            dlat = math.radians(lat2-lat1)
            dlon = math.radians(lon2-lon1)
            a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
            return radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
        else:
            return 100000.0

    def recent2_clevel_change(self, items):
        interacted_with = [x for x in self.user.interacted_with[2] if x != self.item.id]
        if len(interacted_with) != 0:
            return ((items[interacted_with[0]].clevel - self.item.clevel)/10)+0.5
        else:
            return 0.5

    def recent3_titletags(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/(len(intersect.union(interact.tags))+1)
        return 0.0

    def recent3_tagstitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.title))/(len(intersect.union(interact.title))+1)
        else:
            return 0.0

    def recent3_titletitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.title))/(len(intersect.union(interact.title))+1)
        return 0.0

    def recent3_tagstags(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/(len(intersect.union(interact.tags))+1)
        else:
            return 0.0

    def recent3_clevel(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].clevel == self.item.clevel:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent3_disc(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].disc == self.item.disc:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent3_indus(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].indus == self.item.indus:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent3_region(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].region == self.item.region:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent3_country(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].country == self.item.country:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent3_etype(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].etype == self.item.etype:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent3_distance(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
        if len(interacted_with) != 0 and self.item.lat is not None and self.item.lon is not None:
            (lat1, lon1) = (self.item.lat, self.item.lon)
            radius = 6371
            (lat2, lon2) = (items[interacted_with[0]].lat, items[interacted_with[0]].lon)
            dlat = math.radians(lat2-lat1)
            dlon = math.radians(lon2-lon1)
            a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
            return radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
        else:
            return 100000.0

    def recent3_clevel_change(self, items):
        interacted_with = [x for x in self.user.interacted_with[3] if x != self.item.id]
        if len(interacted_with) != 0:
            return ((items[interacted_with[0]].clevel - self.item.clevel)/10)+0.5
        else:
            return 0.5

    def recent4_titletags(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/(len(intersect.union(interact.tags))+1)
        return 0.0

    def recent4_tagstitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.title))/(len(intersect.union(interact.title))+1)
        else:
            return 0.0

    def recent4_titletitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.title))/(len(intersect.union(interact.title))+1)
        return 0.0

    def recent4_tagstags(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/(len(intersect.union(interact.tags))+1)
        else:
            return 0.0

    def recent4_clevel(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].clevel == self.item.clevel:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent4_disc(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].disc == self.item.disc:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent4_indus(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].indus == self.item.indus:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent4_region(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].region == self.item.region:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent4_country(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].country == self.item.country:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent4_etype(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].etype == self.item.etype:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent4_distance(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
        if len(interacted_with) != 0 and self.item.lat is not None and self.item.lon is not None:
            (lat1, lon1) = (self.item.lat, self.item.lon)
            radius = 6371
            (lat2, lon2) = (items[interacted_with[0]].lat, items[interacted_with[0]].lon)
            dlat = math.radians(lat2-lat1)
            dlon = math.radians(lon2-lon1)
            a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
            return radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
        else:
            return 100000.0

    def recent4_clevel_change(self, items):
        interacted_with = [x for x in self.user.interacted_with[4] if x != self.item.id]
        if len(interacted_with) != 0:
            return ((items[interacted_with[0]].clevel - self.item.clevel)/10)+0.5
        else:
            return 0.5

    def recent5_titletags(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/(len(intersect.union(interact.tags))+1)
        return 0.0

    def recent5_tagstitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.title))/(len(intersect.union(interact.title))+1)
        else:
            return 0.0

    def recent5_titletitle(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.title))/(len(intersect.union(interact.title))+1)
        return 0.0

    def recent5_tagstags(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/(len(intersect.union(interact.tags))+1)
        else:
            return 0.0

    def recent5_clevel(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].clevel == self.item.clevel:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent5_disc(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].disc == self.item.disc:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent5_indus(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].indus == self.item.indus:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent5_region(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].region == self.item.region:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent5_country(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].country == self.item.country:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent5_etype(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].etype == self.item.etype:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent5_distance(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
        if len(interacted_with) != 0 and self.item.lat is not None and self.item.lon is not None:
            (lat1, lon1) = (self.item.lat, self.item.lon)
            radius = 6371
            (lat2, lon2) = (items[interacted_with[0]].lat, items[interacted_with[0]].lon)
            dlat = math.radians(lat2-lat1)
            dlon = math.radians(lon2-lon1)
            a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
            return radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
        else:
            return 100000.0

    def recent5_clevel_change(self, items):
        interacted_with = [x for x in self.user.interacted_with[5] if x != self.item.id]
        if len(interacted_with) != 0:
            return ((items[interacted_with[0]].clevel - self.item.clevel)/10)+0.5
        else:
            return 0.5

    ### Extended feature set ##########################################

    def clevel_change(self):
            return ((self.user.clevel - self.item.clevel)/10)+0.5

    def title_match(self):
        jobroles = set(self.user.jobroles)
        return len(jobroles.intersection(self.item.title))/len(jobroles.union(self.item.title))

    def tags_match(self):
        jobroles = set(self.user.jobroles)
        return len(jobroles.intersection(self.item.tags))/len(jobroles.union(self.item.tags))

    def user_clevel(self):
        return self.user.clevel

    def user_disc(self):
        return self.user.disc

    def user_indus(self):
        return self.user.indus

    def user_expy(self):
        return self.user.expy

    def user_expn(self):
        return self.user.expn

    def user_expyc(self):
        return self.user.expyc

    def user_edud(self):
        return self.user.edud

    def user_country(self):
        c = {"de": 0, "at": 1, "ch": 2, "non_dach": 3}
        return c[self.user.country]

    def user_region(self):
        return self.user.region

    def item_disc(self):
        return self.item.disc

    def item_indus(self):
        return self.item.indus

    def item_clevel(self):
        return self.item.clevel

    def item_country(self):
        c = {"de": 0, "at": 1, "ch": 2, "non_dach": 3}
        return c[self.item.country]

    def item_region(self):
        return self.item.region

    def item_etype(self):
        return self.item.etype

    def item_time(self):
        return self.item.time

    def item_lat(self):
        return self.item.lat

    def item_lon(self):
        return self.item.lon

    def paid(self):
        return self.item.paid

    def xtcj(self):
        return self.user.xtcj

    # Concept Based features
    def title_tfidf(self, concept_weights, N):
        length = len(self.item.title)
        if length > 0:
            QD = 0.0
            for term in set(self.user.jobroles).intersection(self.item.title):
                QD += math.log(1 + N/concept_weights[term])
            return QD/math.sqrt(length)
        else:
            return 0

    def tags_tfidf(self, concept_weights, N):
        length = len(self.item.tags)
        if length > 0:
            QD = 0.0
            for term in set(self.user.jobroles).intersection(self.item.tags):
                QD += math.log(1 + N/concept_weights[term])
            return QD/math.sqrt(length)
        else:
            return 0

    def titletags_tfidf(self, concept_weights, N):
        document = set(self.item.title).union(self.item.tags)
        length = len(document)
        if length > 0:
            QD = 0.0
            for term in document.intersection(self.user.jobroles):
                QD += math.log(1 + N/concept_weights[term])
            return QD/math.sqrt(length)
        else:
            return 0

    def title_cbf(self, concept_weights, N):
        length = len(self.item.title)
        if length > 0:
            QD = 0.0
            for term in set(self.user.CBF_weights).intersection(self.item.title):
                QD += math.log(1 + N/concept_weights[term])
            return QD/math.sqrt(length)
        else:
            return 0

    def tags_cbf(self, concept_weights, N):
        length = len(self.item.tags)
        if length > 0:
            QD = 0.0
            for term in set(self.user.CBF_weights).intersection(self.item.tags):
                QD += math.log(1 + N/concept_weights[term])
            return QD/math.sqrt(length)
        else:
            return 0

    def titletags_cbf(self, concept_weights, N):
        document = set(self.item.title).union(self.item.tags)
        length = len(document)
        if length > 0:
            QD = 0.0
            for term in document.intersection(self.user.CBF_weights):
                QD += math.log(1 + N/concept_weights[term])
            return QD/math.sqrt(length)
        else:
            return 0

    def inverse_title_tfidf(self, concept_weights, N):
        length = len(self.user.jobroles)
        if length > 0:
            QD = 0.0
            for term in set(self.item.title).intersection(self.user.jobroles):
                QD += math.log(1 + N/concept_weights[term])
            return QD/math.sqrt(length)
        else:
            return 0

    def inverse_tags_tfidf(self, concept_weights, N):
        length = len(self.user.jobroles)
        if length > 0:
            QD = 0.0
            for term in set(self.item.tags).intersection(self.user.jobroles):
                QD += math.log(1 + N/concept_weights[term])
            return QD/math.sqrt(length)
        else:
            return 0

    def inverse_titletags_tfidf(self, concept_weights, N):
        query = set(self.item.title).union(self.item.tags)
        length = len(self.user.jobroles)
        if length > 0:
            QD = 0.0
            for term in query.intersection(self.user.jobroles):
                    QD += math.log(1 + N/concept_weights[term])
            return QD/math.sqrt(length)
        else:
            return 0

    def inverse_titletags_cbf(self, concept_weights, N):
        length = len(self.user.jobroles)
        if length > 0:
            QD = 0.0
            for term in set(self.item.CBF_weights).intersection(self.user.jobroles):
                QD += math.log(1 + N/concept_weights[term])
            return QD/math.sqrt(length)
        else:
            return 0

    ### ONE HOT MODEL ###########################################################

    def onehot_features(self):
        f_list = [0]*363
        f_list[self.user.clevel] = 1
        f_list[7+self.user.disc] = 1
        f_list[31+self.user.indus] = 1
        f_list[55+self.user.expn] = 1
        f_list[59+self.user.expy] = 1
        f_list[66+self.user.expyc] = 1
        f_list[73+self.user.edud] = 1
        f_list[77+self.user.region] = 1
        f_list[94+self.user.xtcj] = 1
        f_list[96+self.country[self.user.country]] = 1
        f_list[100+self.item.clevel] = 1
        f_list[107+self.item.disc] = 1
        f_list[131+self.item.indus] = 1
        f_list[155+self.item.paid] = 1
        f_list[157+self.item.etype] = 1
        f_list[161+self.item.region] = 1
        f_list[178+self.country[self.item.country]] = 1
        f_list[182+self.lat[self.item.lat]] = 1
        f_list[267+self.lon[self.item.lon]] = 1
        possible = [0,1,2,3,4,5,6,7,8,9]
        edufos_list = [0]*len(possible)
        for i in self.user.edufos:
            if i in possible:
                edufos_list[possible.index(i)] = 1
        jobroles_list = [0]*len(self.user_concepts)
        for i in self.user.jobroles:
            if i in self.user_concepts:
                jobroles_list[self.user_concepts[i]] = 1
        title_list = [0]*len(self.item_concepts)
        for i in self.item.title:
            if i in self.item_concepts:
                title_list[self.item_concepts[i]] = 1
        tags_list = [0]*len(self.item_concepts)
        for i in self.item.tags:
            if i in self.item_concepts:
                tags_list[self.item_concepts[i]] = 1
        return (f_list + edufos_list + jobroles_list + title_list + tags_list)
    
    def features(self, items):
        return self.onehot_features() + [
            self.clevel_match(), self.indus_match(), self.discipline_match(), 
            self.country_match(), self.region_match(), self.clevel_change(),
            self.title_match(), self.tags_match(), #self.titletags_match(),

            #self.user_clevel(),self.user_disc(),
            #self.user_indus(),self.user_expy(),
            #self.user_expn(),
            #self.user_expyc(),self.user_edud(),
            #self.user_country(),self.user_region(),
            #self.xtcj(),

            #self.item_disc(),
            #self.item_indus(),self.item_clevel(),
            #self.item_country(),self.item_region(),
            #self.item_etype(),self.item_time(),
            #self.item_lat(), self.item_lon(),
            #self.paid(),

            #self.title_tfidf(item_cw, item_N), 
            #self.tags_tfidf(item_cw, item_N), 
            #self.titletags_tfidf(item_cw, item_N),
            #self.title_cbf(item_cw, item_N), 
            #self.tags_cbf(item_cw, item_N), 
            #self.titletags_cbf(item_cw, item_N),

            #self.inverse_title_tfidf(user_cw, user_N), 
            #self.inverse_tags_tfidf(user_cw, user_N),
            #self.inverse_titletags_tfidf(user_cw, user_N),
            #self.inverse_titletags_cbf(user_cw, user_N),

            self.interaction0_titletags(items),
            self.interaction0_tagstitle(items),
            self.interaction0_titletitle(items),
            self.interaction0_tagstags(items),
            self.interaction0_distance(items),
            self.interaction0_clevel(items),
            self.interaction0_disc(items),
            self.interaction0_indus(items),
            self.interaction0_region(items),
            self.interaction0_country(items),
            self.interaction0_etype(items),
            self.interaction0_clevel_change(items),

            self.interaction1_titletags(items),
            self.interaction1_tagstitle(items),
            self.interaction1_titletitle(items),
            self.interaction1_tagstags(items),
            self.interaction1_distance(items),
            self.interaction1_clevel(items),
            self.interaction1_disc(items),
            self.interaction1_indus(items),
            self.interaction1_region(items),
            self.interaction1_country(items),
            self.interaction1_etype(items),
            self.interaction1_clevel_change(items),

            self.interaction2_titletags(items),
            self.interaction2_tagstitle(items),
            self.interaction2_titletitle(items),
            self.interaction2_tagstags(items),
            self.interaction2_distance(items),
            self.interaction2_clevel(items),
            self.interaction2_disc(items),
            self.interaction2_indus(items),
            self.interaction2_region(items),
            self.interaction2_country(items),
            self.interaction2_etype(items),
            self.interaction2_clevel_change(items),

            self.interaction3_titletags(items),
            self.interaction3_tagstitle(items),
            self.interaction3_titletitle(items),
            self.interaction3_tagstags(items),
            self.interaction3_distance(items),
            self.interaction3_clevel(items),
            self.interaction3_disc(items),
            self.interaction3_indus(items),
            self.interaction3_region(items),
            self.interaction3_country(items),
            self.interaction3_etype(items),
            self.interaction3_clevel_change(items),

            self.interaction4_titletags(items),
            self.interaction4_tagstitle(items),
            self.interaction4_titletitle(items),
            self.interaction4_tagstags(items),
            self.interaction4_distance(items),
            self.interaction4_clevel(items),
            self.interaction4_disc(items),
            self.interaction4_indus(items),
            self.interaction4_region(items),
            self.interaction4_country(items),
            self.interaction4_etype(items),
            self.interaction4_clevel_change(items),

            self.interaction5_titletags(items),
            self.interaction5_tagstitle(items),
            self.interaction5_titletitle(items),
            self.interaction5_tagstags(items),
            self.interaction5_distance(items),
            self.interaction5_clevel(items),
            self.interaction5_disc(items),
            self.interaction5_indus(items),
            self.interaction5_region(items),
            self.interaction5_country(items),
            self.interaction5_etype(items),
            self.interaction5_clevel_change(items),

            self.recent0_titletags(items),
            self.recent0_tagstitle(items),
            self.recent0_titletitle(items),
            self.recent0_tagstags(items),
            self.recent0_distance(items),
            self.recent0_clevel(items),
            self.recent0_disc(items),
            self.recent0_indus(items),
            self.recent0_region(items),
            self.recent0_country(items),
            self.recent0_etype(items),
            self.recent0_clevel_change(items),
            
            self.recent1_titletags(items),
            self.recent1_tagstitle(items),
            self.recent1_titletitle(items),
            self.recent1_tagstags(items),
            self.recent1_distance(items),
            self.recent1_clevel(items),
            self.recent1_disc(items),
            self.recent1_indus(items),
            self.recent1_region(items),
            self.recent1_country(items),
            self.recent1_etype(items),
            self.recent1_clevel_change(items),

            self.recent2_titletags(items),
            self.recent2_tagstitle(items),
            self.recent2_titletitle(items),
            self.recent2_tagstags(items),
            self.recent2_distance(items),
            self.recent2_clevel(items),
            self.recent2_disc(items),
            self.recent2_indus(items),
            self.recent2_region(items),
            self.recent2_country(items),
            self.recent2_etype(items),
            self.recent2_clevel_change(items),

            self.recent3_titletags(items),
            self.recent3_tagstitle(items),
            self.recent3_titletitle(items),
            self.recent3_tagstags(items),
            self.recent3_distance(items),
            self.recent3_clevel(items),
            self.recent3_disc(items),
            self.recent3_indus(items),
            self.recent3_region(items),
            self.recent3_country(items),
            self.recent3_etype(items),
            self.recent3_clevel_change(items),

            self.recent4_titletags(items),
            self.recent4_tagstitle(items),
            self.recent4_titletitle(items),
            self.recent4_tagstags(items),
            self.recent4_distance(items),
            self.recent4_clevel(items),
            self.recent4_disc(items),
            self.recent4_indus(items),
            self.recent4_region(items),
            self.recent4_country(items),
            self.recent4_etype(items),
            self.recent4_clevel_change(items),

            self.recent5_titletags(items),
            self.recent5_tagstitle(items),
            self.recent5_titletitle(items),
            self.recent5_tagstags(items),
            self.recent5_distance(items),
            self.recent5_clevel(items),
            self.recent5_disc(items),
            self.recent5_indus(items),
            self.recent5_region(items),
            self.recent5_country(items),
            self.recent5_etype(items),
            self.recent5_clevel_change(items),
        ]

    def interaction_weight(self):
        if len(self.interactions) > 0:
            clicked = False
            bmR = False
            RI = False
            deleted = False
            looked = False
            for i in self.interactions:
                if i.i_type == 4:
                    deleted = True
                    break
                elif i.i_type == 1 and clicked == False: 
                    clicked = True
                elif i.i_type == 2 or i.i_type == 3 and bmR == False: 
                    bmR = True
                elif i.i_type == 5 and RI == False:
                    RI = True
                elif i.i_type == 0 and looked == False: 
                    looked = True
            if deleted == True:
                return -1.0
            elif RI == True:
                return 4.0
            elif bmR == True:
                return 3.0
            elif clicked == True:
                return 2.0
            elif looked == True:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0


    def label(self):
        if len(self.interactions) > 0:
            deleted = False
            for i in self.interactions:
                if i.i_type == 4:
                    deleted = True
                    break
            if deleted == True:
                return 0.0
            else:
                return 1.0
        else:
            return 0.0

    """
    def label(self): 
        score = 0.0
        clicked = False
        bmR = False
        RI = False
        deleted = False
        for i in self.interactions:
            if i.i_type == 1 and clicked == False: 
                score+=1
                clicked = True
            if i.i_type == 2 or i.i_type == 3 and bmR == False: 
                    score+=5
                bmR = True
            if i.i_type == 4 and deleted == False:
                deleted = True
            if i.i_type == 5 and RI == False:
                score+=20
                RI = True

        if self.user.premium == 1:
            score = score*2

        if (deleted == True and 
            clicked == False and 
            bmR == False and 
            RI == False):
            score = -10.0

        score = (score/100)+0.1

        return score
        """

def data_dicts():
    user_concepts_list = [58508,56155,7172,57161,14000,16871,776,162794,169814,
                     115127,7619,5694,12801,33204,165466,5087,18378,123244,
                     210327,7989,18386,8906,16368,27808,25769,29688,1177,
                     254053,56355,36078,192748,7875,9979,102508,45957,17761,
                     58534,90696,22014,18927,14523,554,557,2458,42013,6256,
                     550,42365,39563,6663,13667,1016,851,32865,68636,11457,
                     7272,16639,11490,1125,5760,782,4457,19083,3963,3909,
                     3963,17453,17178,32676,26707,588,7322,26921,5433,130181,
                     33689,5776,122246,5663,4274,31718,32019,33784,28563,
                     26958,10550,17110,2292,2504,56685,19578,52987,4747,
                     4721,12039,3343,4693,3417,24935,24966,24105,85191,75193,
                     25138,92067,93532,94318,90874,3531,17204,63291,1416,
                     10991,63311,5243,25615,5171,62073,63987,1583,25620,
                     62920,78228,75142,9698,65737,63257,7796,71866,76055,
                     1259,7717,1069,54987,16758,12139,5035,7685,2661,3124,
                     4301,18227,2420,22839,22114,44475,954,4412,21283,49654,
                     53727,94631,86532,94174,21673,10290,1539,13228,56123,
                     2837,4238,4237,45975,12968,29629,21214,40966,40608,
                     14243,63980,20643,97817,758,8849,5531,7897,39268,18719,
                     42472,47577,60547,12298,83981,6364,97218,89112,12122,
                     7315,25594,25883,11048,8320,2036,7501,7316,32900,7339,
                     13609,20547,36272,72715,84151,12507,14545,12175,14782,
                     14408,12160,10752,8047,1502,2791,27317,1633,6191,24805,
                     4501,40473,30611,44358,46846,44631,24732,1365,5106,
                     4518,10232,13232,7967,6725,5691,5187,1564,5928,18496,
                     13646,5450,5566,6707,2012,1850,3497,3465,3331,11345,
                     6691,6246,1409,2123,19309,91323,23573,8730,4622,86834,
                     5215,28842,82104,7459,21107,3571,11584,2985,17562,48155,
                     30010,23566,8507,9132,9646,10232,18853,102030,10137,
                     4320,1156,2747,19391,23018,9506,7439,2111,53499,10040,
                     5301,1696,5621,18683,14856,1271,657,12618,18918,1829,
                     10791,6109,6313,4583,3789,4859,7690,7100,7575,7575,
                     8543,47813,10525,4731,5174,1170,755,3326,11980,620,
                     7085,5149,2153,2326,2312,2421,4850,4332,14713,93513,
                     82522,47375,783,15971,6085,5050,54524,21578,6457,567,
                     2498,907,22422,10138,22593,1647,20376,10228,51111,2148,
                     54151,15485,9541,25288,25086,9554,9750,63823,51271,
                     1400,9155,17257,21560,2052,19059,30118,1109,1708,4251,
                     6472,50095,52604,61983,9135,4534,12604,9211,4868,857,
                     1027,989,790,2190,10770,1182,628,8948,7951,14781,9783,
                     10877,14208,4159,4006,1876,14442,12941,3913,8570,2200,
                     3229,9602,3172,29001,1911,1390,9227,9335,8992,54638,
                     60446,65905,58876,64786,3994,27398,7946,13802,4721,
                     13081,6086,6120,1908,1234,1231,1341,1157,1371,4434,
                     12446,5213,15582,11112,10975,66364,25215,26730,26890,
                     3759,55017,61206,3700,41089,17152,41258,1598,1597,2517,
                     14533,19881,20139,19691,8081,40340,31421,40072,1604,
                     1649,1780,1637,1140,1178,13941,2609,7539,8109,8624,
                     4366,4912,10207,4699,17085,23673,11913,33575,1022,3008,
                     3007,2828,2701,10103,2615,1452,4458,7071,41495,41211,
                     992,1008,7071,39941,43597,4419,44298,4610,510,6394,
                     3219,3202,795,768,1520,7675,4503,509,33999,10648,6671,
                     3372,3492,1529,4524,609,540,33510,33764,6670,1123,1122,
                     4519,4352,2886,2498,6002,2823,2432,42489,60459,42499,
                     8839,27668,1839,5222,773,1381,669,12416,1322,22964,
                     2943,638,6015,5889,5571,5877,1449,616,2445,3923,2282,
                     1286,5954,6831,5162,1550,1092,522,2139,826,7552,1084,
                     1235,8222,6190,6325,12318,3999,10755,8410,13374,9748,
                     11643,1798,2404,1590,6942,3974,633,22784,12950,638,
                     19655,14932,650,1433,13745,15516,7750,8663,8518,24544,
                     3503,3067,11510,2948,3165,3164,3047,3167,2009,2520,
                     14342,14544,1855,4009,3216,6731,12856,4066,10154,7242,
                     1229,3942,13674,12794,13819,15036,2241,1716,12809,6549,
                     1712,21048,7759,27275,5010,1503,670,1792,14888,955,
                     39609,1517,1939,687,7619,4755,9346,672,1757,1740,2033,
                     2142,1975,1975,2033,47781,4990,31755,5877,2496,2581,
                     10210,2709,18085,6336,921,25040,2733,14062,5211,587,
                     44491,27737,3505,3393,5749,4862,4688,7346,7213,3578,
                     3816,9065,685,3013,3938,684,5297,2978,5273,4451,5716,
                     5297,10991,2462,26485,3875,2116,1189,17656,6154,10945,
                     6153,1269,3328,30748,8409,3563,1767,848,501,5115,21934,
                     23016,21359,13682,5909,5907,5905,4275,3573,1829,3194,
                     3194,5872,5791,5431,4141,6299,8475,4182,5325,12762,
                     4845,3887,9125,775,2887,2178,1726,2395,1179,2582,5232,
                     1518,6602,9215,12894,8204,13642,17170,12702,524,1365,
                     10835,14085,9960,9444,53737,1416,533,14959,1398,1394,
                     8503,14643,3844,3770,3986,3844,3769,1709,6172,8279,
                     3109,6721,1968,2049,2957,1735,1330,4710,622,634,856,
                     6064,1344,1282,1344,819,4063,23998,6647,5958,6130,790,
                     6272,1047,1011,24032,10993,4132,1957,1017,1581,19928,
                     1673,2729,9844,2833,3544,2733,1331,2763,10174,8202,
                     1936,15570,16428,3555,2273,4363,7146,18416,18714,18451,
                     16273,18263,751,1261,730,2505,928,4874,7067,2321,4157,
                     4815,3387,567,7335,1105,5415,5382,5326,14882,3095,1312,
                     2147,3411,2293,1270,1270,4565,2883,2666,2835,551,2713,
                     5320,6175,6183,9479,7101,10181,9650,6736,4221,7137,
                     997,546,3515,702,2289,6828,1301,1801,1358,14492,7042,
                     23502,12690,22104,4692,6676,5033,13166,1991,4970,4160,
                     9973,6597,6479,1779,6722,2343,1088,1065,8414,8174,1561,
                     997,12104,10359,1131,1017,3855,11011,4540,682,1685,
                     1572,1826,1815,4847,4806,3109,3138,9796,2388,3841,3762,
                     834,2315,2356,2382,3837,3047,7303,3454,804,2417,2735,
                     3398,2224,5802,5813,2893,8757,5730,5233,1787,1296,1353,
                     1294,2034,17960,21043,17375,3474,9826,3743,734,7079,
                     4139,4145,4147,6571,4192,1971,3873,3681,5250,2717,4904,
                     2685,2344,13054,1313,565,558,6798,5102,5214,1588,7060,
                     1922,1963,1752,4068,1581,4310,4956,4073,2226,10568,
                     3646,2436,3281,7046,2157,2119,4053,2115,793,892,891,
                     3791,3663,836,4986,7939,1476,5765,3957,6040,2784,1423,
                     1595,3172,5148,7531,1502,1050,1234,9709,2864,9922,9481,
                     9868,3985,9975,12338,5325,11912,4169,5260,13668,13653,
                     15160,13846,16094,5166,5167,5167,1730,5370,3093,6507,
                     6511,3059,4066,926,5885,1382,12309,5618,2382,2146,1894,
                     1972,2601,3726,997,4982,656,4980,4980,4783,11797,1063,
                     1906,1274,5555,7730,1531,7203,1500,2849,8110,616,3102,
                     2487,2400,3764,3077,6692,5501,2116,4375,1390,6314,923,
                     5305,12958,963,3731,3777,727,3009,580,2985,7334,6886,
                     13813,9175,6603,2935,601,2456,2740,2368,2069,2659,1939,
                     5429,2383,1050,5851,5855,5503,601,948,1386,2073,2060,
                     4412,575,5615,4895,1883,2220,3430,1366,3550,833,6232,
                     4854,3246,3249,2998,5112,6251,4433,3835,4429,1123,3598,
                     2727,2600,1611,1456,8058,4610,919,930,1172,1280,3062,
                     1975,1724,1973,709,4369,960,3679,1114,10124,1989,1085,
                     1979,2019,2387,15045,12539,613,2314,3782,1075,3547,
                     3023,3048,4384,622,1286,6166,4669,9325,10643,3399,2330,
                     10259,1056,3592,6352,1200,4169,8431,1997,1771,1830,
                     969,7303,3620,523,1197,2452,848,4553,12965,2459,959,
                     12972,11359,834,2952,4878,7750,3399,4410,535,545,3461,
                     1705,2571,2406,2098,1231,3171,1106,2276,2513,2513,1112,
                     1894,2290,14611,6212,3437,2090,1936,3105,3773,11443,
                     1588,1028,20981,9852,9850,12284,1093,1004,1001,976,
                     8737,2880,2549,1700,7524,10837,7904,9005,1696,818,1407,
                     3850,896,3388,8204,730,7490,7750,1218,7708,1177,2213,
                     2511,2141,7612,7603,7587,929,956,910,910,929,2387,995,
                     2765,2491,1341,2402,4012,2573,3211,4874,1374,2808,8567,
                     2922,616,783,2413,5292,17445,5735,3342,562,1114,2513,
                     5455,806,1875,3219,4940,3622,1294,841,1098,587,3514,
                     588,2228,2486,1664,5671,773,2383,813,766,11264,967,
                     20985,2322,2285,2340,5595,747,603,1056,1154,830,9112,
                     5264,5392,821,1418,2355,1353,4224,3588,1099,3980,1406,
                     811,2130,2117,6874,7030,793,7447,8408,7918,2256,614,
                     610,1006,6305,557,609,1341,1139,1444,2632,940,926,4604,
                     3176,1486,2505,1847,1396,9445,1177,4426,3471,1867,970,
                     1120,970,1587,6628,4271,641,2931,4626,2822,3738,4722,
                     1474,1273,1819,581,3662,3749,2707,4615,1201,2357,8673,
                     3562,3525,584,592,1012,1048,2388,3254,2467,997,1324,
                     4478,12267,3737,3402,3405,624,1506,1381,921,6644,6751,
                     3719,2071,3309,2000,4303,8736,582,582,565,1017,3522,
                     2905,3048,4416,2827,2790,658,2387,12715,1041,3083,3354,
                     2360,721,1997,974,5337,5360,9922,8656,1375,3728,2362,
                     6533,3471,3999,2042,2831,701,2970,2553,1242,2812,9232,
                     3225,8977,3237,3439,5517,2838,1221,1217,1147,4220,1533,
                     590,705,594,3599,4835,1115,1778,1843,1451,2747,5934,
                     4021,645,5290,1208,9415,524,1153,701,748,3769,2167,
                     2592,2313,4560,545,536,2962,2954,8859,2978,1779,1134,
                     2049,1726,1094,7066,693,1716,9978,1487,1958,1822,4731,
                     3452,2626,1079,928,591,663,820,3438,1276,3335,6217,
                     1590,533,533,5036,4875,1915,3568,4981,3622,871,9786,
                     2861,5446,5538,5411,3256,815,799,2685,1572,1572,3384,
                     2126,1447,864,1013,1013,579,1397,5358,798,710,4571,
                     5706,4756,5279,9009,2398,531,957,4179,2692,2649,2844,
                     837,2148,2340,1141,894,555,652,2597,1294,1376,2526,
                     3340,2414,3573,855,1449,3028,3664,4683,1356,5947,572,
                     789,4251,1332,1715,1793,538,2145,1168,3478,763,4633,
                     1427,1639,1969,1882,1741,1113,725,1742,520,10211,2541,
                     3844,4096,927,1849,1562,2494,1062,8938,3669,1503,4255,
                     2380,2070,3347,4345,1018,1018,639,3126,4881,2100,888,
                     957,980,980,970,1125,1288,2120,1194,3215,2964,3592,
                     1432,1288,1192,1981,2766,3702,3141,3325,3441,827,2919,
                     2922,4072,4061,2922,5123,5162,2387,939,1241,4306,1382,
                     1129,12875,2269,1881,6010,966,637,637,863,1519,4322,
                     1423,561,1278,7356,7327,6947,1285,897,1541,4505,1316,
                     5994,2245,1142,710,691,629,999,2405,1815,1306,2669,
                     1229,3551,1445,1685,688,923,930,644,844,1636,710,1786,
                     2116,7729,2320,7806,4101,814,3029,1796,1621,2633,5057,
                     2716,868,830,1953,1392,7088,2505,2494,3340,792,871,
                     3771,3927,729,1366,1366,1320,1457,1320,4936,1162,3132,
                     2371,1756,1605,4537,3755,1743,2236,1264,813,1644,3624,
                     1226,3378,6823,6871,6808,4096,1912,1271,1014,2156,508,
                     552,603,529,546,4095,625,2264,2840,4138,2813,623,2432,
                     2997,1186,2374,1144,1531,1002,1036,2066,1102,2864,2889,
                     731,1084,2514,691,3526,1471,1092,815,536,606,818,1199,
                     3083,3392,3270,3283,1841,3126,3171,1931,925,1966,1313,
                     1957,3170,926,926,1339,2631,1187,1534,1406,747,827,
                     511,10687,12261,12217,5193,3077,3735,1006,2020,1533,
                     2505,1140,1233,720,885,4828,2205,4322,681,606,7389,
                     3508,1459,1469,531,2508,1097,951,951,1385,1475,553,
                     747,1597,1710,1358,1161,3184,2431,2225,708,934,3043,
                     1313,3503,826,1978,648,602,648,798,1310,1271,1006,2299,
                     12276,14103,13112,1858,2467,3424,3896,3624,6667,3372,
                     1374,1803,3228,1386,1041,1506,987,2035,4019,3247,582,
                     1326,624,2639,2209,3321,1084,1155,1394,1326,537,1207,
                     2256,961,1093,1100,1095,6082,905,1530,710,653,1630,
                     2320,1460,1369,1369,5389,4980,4995,5389,2816,653,2244,
                     2954,2950,1778,2240,1837,1888,1363,751,4666,1811,3728,
                     3749,2326,2045,3177,2554,818,1449,689,736,1056,1122,
                     2775,3177,2667,2181,559,2290,559,4408,4447,4418,945,
                     769,1451,597,545,1862,2083,919,4655,1676,2099,2057,
                     3578,3735,5373,534,603,1642,654,551,1028,1768,1103,
                     518,2021,1924,839,684,674,2018,968,1376,596,4448,1787,
                     5846,612,3127,2158,830,3706,1064,1085,812,4436,2260,
                     7296,2723,1961,2228,872,977,787,787,1384,1083,922,650,
                     648,1255,2688,4262,722,714,4954,2283,1536,1743,527,
                     502,560,1052,1296,937,520,1756,2241,2132,1277,1310,
                     1322,1267,1394,1344,648,2076,1417,666,2777,2257,1058,
                     989,667,552,613,2206,1966,1952,3101,3090,1278,589,1214,
                     723,2935,684,3343,3383,604,3320,929,4527,1000,1421,
                     1613,1637,2477,920,2038,2653,656,656,1628,2472,985,
                     1093,624,1306,688,3156,1576,4666,1702,1754,4710,1419,
                     534,3621,611,1526,1516,1741,3009,2049,1604,2045,945,
                     1071,1834,700,1832,983,1003,1845,746,1813,1336,797,
                     1130,792,1256,1066,1027,1830,2636,4533,2475,654,3533,
                     1444,569,1035,661,1473,527,1141,1143,3288,1023,620,
                     3742,502,2092,1066,2395,837,840,1418,2260,5898,1723,
                     3809,3873,1311,731,1392,1062,1246,1517,4228,4293,4177,
                     3751,3754,1818,1318,733,933,2319,2363,1614,1176,2849,
                     694,685,688,1011,2284,903,3593,3543,2641,3595,2451,
                     2529,2258,666,2889,3941,2155,523,751,566,1180,624,654,
                     523,752,788,884,554,621,565,530,743,734,2090,1977,683,
                     2556,999,904,2454,1209,1707,1584,1068,2264,1617,693,
                     988,1374,2402,1270,1019,694,694,584,503,1708,1674,572,
                     714,1498,1468,667,880,1126,617,2381,1228,640,611,611,
                     1723,1903,863,1352,1543,2929,776,1238,1407,649,805,
                     606,2673,940,529,1044,1463,805,518,2119,534,1953,1181,
                     1485,2599,695,512,1829,591,1700,968,773,768,735,735,
                     529,516,2872,527,1834,627,618,1039,2683,2959,614,2954,
                     612,1042,920,925,840,1684,834,635,1319,1318,1543,638,
                     655,873,1504,2039,733,1184,516,1762,4025,520,746,746,
                     583,726,1017,1417,4952,1233,2033,937,933,644,957,1215,
                     1833,1143,1566,1181,999,1387,655,1316,731,511,1227,
                     1659,518,1074,868,3448,1035,521,627,879,1031,766,530,
                     1514,744,1639,1149,617,1244,1333,1458,1205,824,1174,
                     1498,623,991,1008,2350,1031,2176,3142,978,1738,999,
                     670,1020,508,1269,1313,1491,823,951,2257,852,628,603,
                     635,917,873,989,809,1523,1504,584,584,1276,623,2043,
                     1065,603,895,1630,807,1470,838,545,647,653,550,887,
                     740,1249,646,1049,1106,1122,1029,707,668,1044,1055,
                     1364,1890,2473,990,1703,511,501,551,949,583,857,848,
                     817,700,828,1741,3952,557,663,538,2013,959,711,501,
                     1176,923,731,696,732,747,720,1581,892,842,1344,1356,
                     505,514,506,597,2074,814,628,588,575,1203,889,1073,
                     537,844,841,710,841,574,894,877,562,2234,511,751,601,
                     1149,636,787,511,1915,552,1458,628,1015,666,2002,3746,
                     3750,3744,857,535,1637,525,516,1254,1343,897,2212,907,
                     941,1265,1174,1278,1265,596,2414,1186,1036,1104,606,
                     839,665,800,878,1459,1384,1391,1374,901,874,657,915,
                     759,698,1095,1447,1046,1034,860,1134,1173,1093,556,
                     764,695,944,936,1179,1755,1422,1442,1485,521,882,850,
                     907,1026,2056,1134,953,2369,1951,1399,1043,695,1757,
                     1068,624,945,1286,802,1230,1206,1206,1161,1161,2565,
                     2664,2618,2447,2565,1090,1122,1052,994,818,809,903,
                     1650,1088,1078,1126,1290,919,1223,1072,1607,899,2228,
                     1494,1093,2229,2503,2762,897,1172,1176,739,1437,925,
                     628,992,994,625,527,783,1222,508,793,793,963,2610,530,
                     568,523,1326,1557,1557,501,837,545,1394,2234,927,969,
                     1295,947,752,501,1281,627,663,1703,678,515,594,955,
                     1821,589,508,1042,1042,1190,781,1224,1222,519,1108,
                     1215,1727,1420,582,716,889,1984,848,1275,870,1295,695,
                     811,824,1475,1231,1458,621,586,1116,633,1231,684,838,
                     1372,1372,798,1265,569,603,1497,537,1486,1018,685,532,
                     604,2661,522,725,714,2518,630,584,596,1038,612,1091,
                     2789,929,856,1070,1120,980,853,854,982,2945,709,577,
                     545,504,594,531,2198,771,646,513,725,1087,2028,1153,
                     522,649,588,918,976,855,861,879,965,2497,623,812,916,
                     1169,1863,571,695,672,714,520,723,820,838,1095,1075,
                     1488,1283,515,520,1114,940,739,777,622,619,740,748,
                     923,909,682,683,909,525,778,1065,536,532,633,1026,627,
                     1454,1303,852,1043,711,770,675,681,754,624,1001,738,
                     735,705,916,575,533,507,542,890,525,1878,599,664,1090,
                     708,579,631,547,1779,548,588,1216,1165,623,560,560,
                     516,781,501,885,622,558,564,820,636,583,2009,742,681,
                     510,656,810,995,1119,513,545,684,1055,583,782,575,768,
                     572,550,672,529,680,525,677,684,662,534,524,640,641,
                     592,592,869,769,1020,1478,1329,1020,797,1056,1023,905,
                     553,703,1145,849,1142,607,1278,1249,1199,538,1062,875,
                     1013,518,861,526,684,599,546,622,771,831,787,805,831,
                     528,1153,590,629,689,527,547,513,618,988,880,920,583,
                     937,690,516,578,526,799,909,1193,620,602,580,538,535,
                     630,718,1087,1066,690,776,992,1002,1002,1037,641,1369,
                     1369,714,516,561,765,815,831,941,2159,901,1260,504,
                     544,543,516,585,745,1093,847,665,1122,1070,1933,1949,
                     520,979,768,591,508,846,689,538,676,567,641,873,830,
                     619,983,965,644,595,748,688,535,740,845,635,516,566,
                     579,537,616,775,561,543,684,668,683,690,693,561,545,
                     640,713,669,503,631]
 
    item_concepts_list = [16031,1732,3517,1606,10605,11396,14119,5235,741,12103,
                     4221,5980,7552,732,1608,12078,68538,6285,3041,4937,
                     42832,3878,3392,4178,1513,71342,57766,14756,1270,1651,
                     114965,75560,11948,27678,17608,37772,5005,37724,1252,
                     5241,2163,13447,8824,5169,28730,1072,1195,16305,1830,
                     3671,4879,27514,27559,1243,1076,1649,55878,55323,3226,
                     38998,17412,2314,592,2792,13299,14503,3020,722,3754,
                     8509,12427,1077,15312,11059,15360,12349,9949,9684,6125,
                     34524,51321,15349,1339,887,1453,14220,13856,3158,2965,
                     2848,4133,20155,1375,1021,7912,630,2704,5983,9887,18419,
                     15409,1364,45649,17569,26498,6462,9495,16661,2270,2081,
                     1248,9084,709,5045,1750,4316,9269,18474,12183,1942,
                     12144,4948,23804,30720,14187,24583,32285,22154,4197,
                     5527,1030,2170,2105,4928,9179,842,759,10801,7770,614,
                     19123,4512,20909,8289,4585,1008,5339,1223,2287,2687,
                     2816,9652,13463,8625,11755,8048,4968,544,9723,14557,
                     27232,16971,14890,4359,4608,7582,4621,8700,1445,4539,
                     1955,552,2978,21521,713,742,617,7588,1206,1108,22415,
                     5790,7933,6267,8825,8772,3777,8375,4828,24783,2233,
                     3100,14240,2303,1618,7532,3599,539,2521,2429,3095,2455,
                     8991,1701,3757,1565,7174,10003,3687,1986,3621,914,2730,
                     596,9214,6983,9089,8507,6192,3132,1005,3567,6041,6180,
                     580,4605,7882,589,620,4501,21964,15232,2572,13655,3278,
                     2574,1897,843,4662,6718,7357,1574,6180,5333,2897,5111,
                     2371,5019,7141,3656,11972,3081,5226,905,873,8670,1958,
                     2206,3824,2280,3009,9037,5592,1110,1491,1584,883,2052,
                     1475,8773,633,810,3862,843,2256,1704,5670,4349,2588,
                     13244,1822,7112,912,2464,4690,16113,1309,2859,10688,
                     4900,4037,6545,1268,1108,12730,655,1552,1517,722,4183,
                     5481,1283,4221,9472,3562,10976,851,516,8044,1516,13657,
                     1628,751,2002,1886,8309,607,3734,840,780,3715,5176,
                     546,8525,5435,5048,7207,5823,2457,3552,6041,949,1407,
                     8675,5112,829,898,5127,6431,12817,12673,735,686,1195,
                     1047,2442,1258,9519,955,1993,1942,3843,946,2499,2746,
                     844,1727,3005,1835,2177,1999,937,8591,4213,1372,6854,
                     1172,6336,522,1708,854,541,2460,2635,775,1118,530,2982,
                     692,652,3704,2889,2245,2632,1183,2204,1022,724,639,
                     1328,1645,1301,12300,3666,4108,533,1259,1446,1207,1345,
                     605,1476,3836,4576,1466,4012,1166,2197,561,2870,6876,
                     7035,4677,2146,3982,6927,4164,1401,2175,6288,1060,8510,
                     688,638,12824,1410,1197,3181,1032,1927,1310,1797,3421,
                     2588,1510,6275,4358,2186,1513,2113,923,2964,586,5031,
                     1877,602,808,1057,1983,2215,1720,2491,3072,960,600,
                     7706,11601,721,1566,2515,1225,4787,2640,838,565,2099,
                     9372,1159,2642,2612,2021,3104,766,1196,1110,2321,1121,
                     6350,7381,677,633,541,10273,3853,6990,7688,7644,733,
                     2692,3676,4201,770,3285,942,705,1623,2317,3332,3228,
                     956,991,2282,5297,5300,748,1929,2775,522,623,799,1706,
                     7995,851,634,2663,1080,3453,1530,535,1799,972,743,2482,
                     1204,1136,1106,1339,3106,2762,2879,698,2712,6322,537,
                     2939,545,13091,2674,2843,857,726,590,2194,1926,1085,
                     2543,827,1027,928,913,2003,758,1112,1308,630,2434,850,
                     2461,548,4173,774,2522,622,673,3476,936,908,2188,631,
                     3313,863,767,871,925,2545,690,1093,2067,1086,2776,590,
                     615,559,7736,9992,2465,1966,6500,3036,635,4397,535,
                     940,1003,1076,1066,873,1894,928,1351,1521,791,1206,
                     592,799,1263,2316,1646,763,710,1489,792,2671,756,3573,
                     977,920,2836,3579,3200,725,1215,1341,920,2957,2095,
                     1901,1949,2069,2847,538,958,1587,2698,1287,1420,649,
                     628,1551,984,2818,3188,2453,759,3041,884,513,1211,1361,
                     1348,3177,843,733,4201,906,743,907,1052,3744,4428,632,
                     1007,1642,877,1884,692,1137,731,1529,1505,1325,1393,
                     1414,650,2210,2019,3609,1204,1744,1111,3638,1853,4368,
                     2797,3731,2819,1023,1039,1168,1880,2107,3828,841,1456,
                     820,738,767,1034,592,1428,2341,1149,4653,2142,1261,
                     998,1123,512,3838,2039,1854,1952,8777,974,826,865,1743,
                     1042,2333,756,4450,1070,1292,1198,1287,2156,2454,1403,
                     1400,3042,3112,1419,627,3204,2527,4313,809,1502,3582,
                     627,1380,1072,1764,1641,1651,976,1140,883,1695,1846,
                     729,621,902,5309,2116,885,628,832,663,1812,596,3975,
                     1525,1563,1573,739,1445,1270,624,988,830,908,822,581,
                     1761,1208,528,2257,2708,508,2557,511,787,1376,627,1013,
                     538,528,678,2201,1514,1293,1112,2854,965,973,964,978,
                     3385,2161,1974,756,1214,737,1424,1252,3171,576,571,
                     762,1373,1169,536,1468,1245,1128,1996,966,1132,794,
                     1452,504,2108,830,11852,1196,1590,967,2237,603,884,
                     933,3256,505,537,962,1287,773,869,855,912,1144,644,
                     2526,2309,2494,1415,1863,1207,1129,2552,1124,906,1530,
                     918,953,659,915,796,1243,722,1459,519,912,606,1488,
                     1639,699,777,1046,720,1697,766,825,1547,740,857,530,
                     520,870,723,691,1481,1721,903,1150,779,1781,1561,621,
                     945,898,1956,2360,591,3230,1217,535,638,743,1092,672,
                     608,856,1204,524,1157,628,1252,1224,2900,1249,984,995,
                     1470,1045,564,635,554,2216,2223,534,1544,1631,1213,
                     1211,763,1861,1360,1527,1264,693,1706,1028,613,754,
                     819,1158,628,862,1706,558,571,907,834,1093,1518,1160,
                     556,719,915,560,1360,554,2176,3116,618,605,518,1365,
                     673,1322,733,1058,2027,565,2977,919,923,781,552,924,
                     723,700,2689,1881,2450,899,918,582,1032,1067,661,783,
                     1317,510,966,564,1447,530,871,720,3117,1078,944,1109,
                     553,779,717,1504,1098,674,672,842,635,797,941,630,926,
                     526,638,538,875,760,568,654,562,570,863,1330,1086,734,
                     627,1099,504,1881,1202,509,644,981,716,811,527,543,
                     607,966,1615,883,1248,669,886,656,646,583,505,737,670,
                     863,851,658,1271,579,1006,698,633,988,604,2130,600,
                     539,1273,1179,1108,584,550,1356,719,767,681,932,567,
                     1863,1594,530,845,1115,881,699,846,967,589,841,844,
                     918,548,912,612,516,504,501,562,2055,503,1062,1008,
                     518,901,1564,1301,722,531,650,630,574,611,605,949,506,
                     842,778,855,782,817,900,636,587,643,717,906,660,544,
                     1356,1945,1153,865,632,809,729,614,642,1020,957,1667,
                     582,530,588,698,507,605,1410,523,717,1080,748,556,556,
                     865,523,879,822,587,657,504,624,593,715,570,564,1018,
                     510,549,514,519,584,529,542,676,682,510,501,922,530,
                     720,541,514,503,829,685]
 
    country = {"de": 0, "at": 1, "ch": 2, "non_dach": 3}

    lat_l = [52.5,48.2,None,53.6,50.1,47.4,48.8,50.9,51.2,48.1,51.5,49.5,
             52.4,51.1,51.4,49.0,48.7,51.3,50.8,47.6,50.0,48.4,51.0,53.5,53.1,
             52.3,50.7,48.0,52.0,47.2,47.1,48.3,47.8,46.9,48.9,47.5,47.7,49.9,
             48.5,47.0,49.2,50.6,49.8,47.3,49.4,52.1,51.7,49.1,52.2,48.6,51.6,
             47.9,51.8,49.3,50.2,50.4,49.6,53.7,51.9,54.3,50.3,53.9,54.1,53.2,
             49.7,46.8,53.8,52.6,53.3,53.4,50.5,53.0,52.7,46.6,52.8,52.9,46.2,
             54.8,54.2,46.7,46.5,54.5,54.0,54.4,46.3]
    lon_l = [13.4,11.6,None,8.7,10.0,8.5,9.2,7.0,6.8,9.7,8.8,8.4,7.6,8.6,8.3,
             16.4,7.2,11.1,7.5,13.1,7.1,12.4,7.9,7.4,9.5,10.1,11.0,9.9,11.4,12.1,
             8.2,8.1,9.1,13.8,8.9,7.3,10.9,9.0,9.3,9.4,10.2,7.8,9.8,8.0,10.3,
             10.5,11.7,6.9,13.0,9.6,10.8,6.1,6.6,10.7,12.9,14.3,13.7,12.2,7.7,
             11.5,11.3,12.0,11.9,10.4,6.7,11.8,10.6,12.5,16.2,12.6,13.3,11.2,
             16.3,13.5,12.8,6.4,15.4,12.3,12.7,13.9,14.0,14.6,13.6,13.2,6.5,
             14.4,15.6,6.3,14.2,6.2,15.5,14.1,14.5,15.0,15.7,15.3]
    lat = dict(zip(lat_l, range(len(lat_l))))
    lon = dict(zip(lon_l, range(len(lon_l))))
    user_concepts = dict(zip(user_concepts_list, range(len(user_concepts_list))))
    item_concepts = dict(zip(item_concepts_list, range(len(item_concepts_list))))

    return (country, lat, lon, user_concepts, item_concepts)
