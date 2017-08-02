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

        self.clicked = False
        self.bmR = False
        self.RI = False
        self.deleted = False
        for i in self.interactions:
            if i.i_type == 1: 
                self.clicked = True
            if i.i_type == 2 or i.i_type == 3: 
                bmR = True
            if i.i_type == 4:
                deleted = True
            if i.i_type == 5:
                RI = True

    ### BASELINE FEATURES
    def title_match(self):
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

    ### INTERACTION FEATURES
    def click(self):
        if self.clicked == True:
            return 1.0
        else:
            return 0.0
            
    def apply_bookmark(self):
        if self.bmR == True:
            return 1.0
        else:
            return 0.0

    def delete(self):
        if self.deleted == True:
            return 0.0
        else:
            return 1.0

    def r_interest(self):
        if self.RI == True:
            return 1.0
        else:
            return 0.0

    def positive_interact(self):
        if (self.click == True or
            self.bmR == True or
            self.RI == True):
            return 1.0
        else:
            return 0.0


    ### EXTENDED ATTRIBUTE FEATURES
    def tags_match(self):
        return float(len(
            set(self.user.jobroles).intersection(set(self.item.tags))))

    def clevel_shrink(self):
        if self.user.clevel > 0 and self.user.clevel == self.item.clevel-1:
            return 1.0
        else:
            return 0.0

    def clevel_shrink2(self):
        if self.user.clevel > 1 and self.user.clevel == self.item.clevel-2:
            return 1.0
        else:
            return 0.0

    def clevel_growth(self):
        if self.user.clevel < 6 and self.user.clevel == self.item.clevel+1:
            return 1.0
        else:
            return 0.0

    def clevel_growth2(self):
        if self.user.clevel < 5 and self.user.clevel == self.item.clevel-2:
            return 1.0
        else:
            return 0.0

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

    def user_expy(self):
        return self.user.expy

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

    # FOr now, disc/indus/clevel, country/region
    def paid_true(self):
        return self.item.paid == 1:
            return 1.0
        else:
            return 0.0

    def xtcj_true(self):
        if self.user.xtcj == 1:
            return 1.0
        else:
            return 0.0

    def paid_false(self):
        if self.item.paid == 1:
            return 1.0
        else:
            return 0.0

    def xtcj_false(self):
        if self.user.xtcj == 1:
            return 1.0
        else:
            return 0.0
    
    # Negation Features
    def clevel_change(self):
        if self.user.clevel != self.item.clevel:
            return 1.0
        else:
            return 0.0

    def indus_change(self):
        if self.user.indus != self.item.indus:
            return 1.0
        else:
            return 0.0

    def discipline_change(self):
        if self.user.disc != self.item.disc:
            return 1.0
        else:
            return 0.0

    def country_change(self):
        if self.user.country != self.item.country:
            return 1.0
        else:
            return 0.0

    def region_change(self):
        if self.user.region != self.item.region:
            return 1.0
        else:
            return 0.0
    

    # TFIDF title-title job-job titlejob-titlejob
    # Actuall CBF built on interactions
    # Popular Items
    # New Items
    # KNN CF
    # Clustered CF
    # Tag statistics, Interaciton stattistics, CBF statistics

    def features(self):
        return [
            self.title_match(), self.clevel_match(), self.indus_match(),
            self.discipline_match(), self.country_match(), self.region_match(),

            self.tags_match(),

            self.user_clevel(),self.user_disc(),
            self.user_indus(),self.user_expy(),
            self.user_expn(),self.user_expy(),
            self.user_expyc(),self.user_edud(),
            self.user_country(),self.user_region(),

            self.item_disc(),
            self.item_indus(),self.item_clevel(),
            self.item_country(),self.item_region(),
            self.item_etype(),self.item_time(),

            self.click(), self.apply_bookmark(), self.delete(),
            self.r_interest(), self.positive_interact(),

            self.clevel_growth(), self.clevel_growth2(),
            self.clevel_shrink(), self.clevel_shrink2(),

            self.xtcj_true(), self.xtcj_false(), 
            self.paid_true(), self.paid_false(),

            self.clevel_change(), self.indus_change() self.discipline_change(), 
            self.country_change(), self.region_change(),
        ]

    def label(self): 
        score = 0.0
        if self.clicked == True:
            score+=1
        if self.bmR == True:
            score+=5
        if self.RI == True:
            score+=20

        if self.user.premium == 1:
            score = score*2

        if (self.deleted == True and 
            self.clicked == False and 
            self.bmR == False and 
            self.RI == False):
            score = -10.0

        return score
