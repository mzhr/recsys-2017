"""
Modeling users, interactions and items from
the recsys challenge 2017.

by Daniel Kohlsdorf
"""

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
                 country, region, paid, etype, time):
        self.id = id
        self.title = title
        self.tags = tags
        self.disc = disc
        self.indus = indus
        self.clevel = clevel
        self.country = country
        self.region = region
        self.paid = paid
        self.etype = etype
        self.time = time

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

    def jobroles_match(self):
        return float(len(
            set(self.user.jobroles).intersection(set(self.item.title))))

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



    def features(self):
        return [
            self.jobroles_match(), self.clevel_match(), self.indus_match(),
            self.discipline_match(), self.country_match(), self.region_match()
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

        if deleted == True and clicked == False and bmR == False and RI == False:
            score = -10.0

        return score
