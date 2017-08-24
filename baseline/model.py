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
        self.interacted_with = []

    def to_vector(self):
        c = {"de": 0, "at": 1, "ch": 2, "non_dach": 3}
        return [
        self.clevel,
        self.disc,
        self.indus,
        self.expn,
        self.expy,
        self.expyc,
        self.edud,
        c[self.country],
        self.region,
        self.xtcj,
        self.premium]

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
        self.interacted_with = []

    def to_vector(self):
        c = {"de": 0, "at": 1, "ch": 2, "non_dach": 3}
        return [
        self.disc,
        self.indus,
        self.clevel,
        c[self.country],
        self.region,
        self.paid,
        self.etype,
        self.time]


class Interaction:
    def __init__(self, i_type, time):
        self.i_type = i_type
        self.time = time


class Interactions:
    def __init__(self, user, item, interactions):
        self.user = user
        self.item = item
        self.interactions = interactions

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

    def interaction_titletags(self, items):
        intersect = set(self.item.title)
        sim = 0.0
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            for i in self.user.interacted_with:
                sim += len(intersect.intersection(items[i].tags))/len(intersect.union(items[i].tags))
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction_tagstitle(self, items):
        intersect = set(self.item.tags)
        sim = 0.0
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            for i in self.user.interacted_with:
                sim += len(intersect.intersection(items[i].title))/len(intersect.union(items[i].title))
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction_titletitle(self, items):
        intersect = set(self.item.title)
        sim = 0.0
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            for i in self.user.interacted_with:
                sim += len(intersect.intersection(items[i].title))/len(intersect.union(items[i].title))
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction_tagstags(self, items):
        intersect = set(self.item.tags)
        sim = 0.0
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            for i in self.user.interacted_with:
                sim += len(intersect.intersection(items[i].tags))/len(intersect.union(items[i].tags))
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction_clevel(self, items):
        sim = 0.0
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            for i in self.user.interacted_with:
                if items[i].clevel == self.item.clevel:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction_disc(self, items):
        sim = 0.0
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            for i in self.user.interacted_with:
                if items[i].disc == self.item.disc:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction_indus(self, items):
        sim = 0.0
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            for i in self.user.interacted_with:
                if items[i].indus == self.item.indus:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction_region(self, items):
        sim = 0.0
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            for i in self.user.interacted_with:
                if items[i].region == self.item.region:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction_country(self, items):
        sim = 0.0
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            for i in self.user.interacted_with:
                if items[i].country == self.item.country:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction_etype(self, items):
        sim = 0.0
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        length = len(interacted_with)
        if length != 0:
            for i in self.user.interacted_with:
                if items[i].etype == self.item.etype:
                    sim += 1
            return sim/len(interacted_with)
        else:
            return 0.0

    def interaction_distance(self, items):
        sim = 0.0
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
        length = len(interacted_with)
        if length != 0 and self.item.lat is not None and self.item.lon is not None:
            (lat1, lon1) = (self.item.lat, self.item.lon)
            radius = 6371
            for i in self.user.interacted_with:
                (lat2, lon2) = (items[i].lat, items[i].lon)
                dlat = math.radians(lat2-lat1)
                dlon = math.radians(lon2-lon1)
                a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
                sim += radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))
            return sim
        else:
            return 10000.0

    ### Temporal interactions #################################################

    def recent_titletags(self, items):
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/len(intersect.union(interact.tags))
        return 0.0

    def recent_tagstitle(self, items):
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.title))/len(intersect.union(interact.title))
        else:
            return 0.0

    def recent_titletitle(self, items):
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.title)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/len(intersect.union(interact.tags))
        return 0.0

    def recent_tagstags(self, items):
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        if len(interacted_with) != 0:
            intersect = set(self.item.tags)
            interact = items[interacted_with[0]]
            return len(intersect.intersection(interact.tags))/len(intersect.union(interact.tags))
        else:
            return 0.0

    def recent_clevel(self, items):
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].clevel == self.item.clevel:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent_disc(self, items):
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].disc == self.item.disc:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent_indus(self, items):
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].indus == self.item.indus:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent_region(self, items):
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].region == self.item.region:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent_country(self, items):
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].country == self.item.country:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent_etype(self, items):
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id]
        if len(interacted_with) != 0:
            if items[interacted_with[0]].etype == self.item.etype:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0

    def recent_distance(self, items):
        interacted_with = [x for x in self.user.interacted_with if x != self.item.id and items[x].lat is not None and items[x].lon is not None]
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
            return 10000.0

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

    def features(self, items, user_cw, user_N, item_cw, item_N):
        return [
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

            self.interaction_titletags(items),
            self.interaction_tagstitle(items),
            self.interaction_titletitle(items),
            self.interaction_tagstags(items),
            self.interaction_distance(items),
            self.interaction_clevel(items),
            self.interaction_disc(items),
            self.interaction_indus(items),
            self.interaction_region(items),
            self.interaction_country(items),
            self.interaction_etype(items),

            self.recent_titletags(items),
            self.recent_tagstitle(items),
            self.recent_titletitle(items),
            self.recent_tagstags(items),
            self.recent_distance(items),
            self.recent_clevel(items),
            self.recent_disc(items),
            self.recent_indus(items),
            self.recent_region(items),
            self.recent_country(items),
            self.recent_etype(items),
        ]


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
