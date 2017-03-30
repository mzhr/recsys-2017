"""
Modeling users, interactions and items from
the recsys challenge 2017.

by Daniel Kohlsdorf
"""

class User:
    """
    Model of the user hosting all data found in the dataset given in the csv.

    Parameters
    ----------
    jobroles: a list of tags of revelent skills in int form
    clevel: career level from 0-6
        0: Unkown
        1: Student/Intern
        2: Beginner
        3: Experienced
        4: Management
        5: Executive
        6: Senior Experience
    disc: id of of discipline eg HR in int form
    indus: industry eg finance in int form
    expn: number of expereinces from 0-6
        0: none
        1: 1-2 entries
        2: 3-4 entries
        3: 5 or more
    expy: number of years of experience from 0-6
        0: unkown
        1: <1 year
        2: 1-3 years
        3: 3-5 years
        4: 5-10 years
        5: 10-20 years
        6: 20+ years
    expyc: number of years in current job, from 0-6
        Same representation as expy
    edud: level of education from 0-3:
        0 or NULL = unknown
        1: bachelor
        2: masters
        3: phd
    edufos: list of fields in education based on int ids
    country: Country of user in string
        de: germany
        at: austraia
        ch: switzerland
        non dach = Other
    region: region if users country code is de, string format
    xtcj: xings estimation of 0 or 1 of willingness to change job
    """

    def __init__(self, jobroles, clevel, disc, indus, expn, expy,
                 expyc, edud, edufos, country, region, xtcj):
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


class Item:
    """
    Model of the item hosting all data found in the dataset given in the csv.

    Parameters
    ----------
    title: a list of id concepts in title
    tags: a list of id concepts in tags
    disc: id of of discipline eg HR in int form
    indus: industry eg finance in int form
    clevel: career level from 0-6
        0: Unkown
        1: Student/Intern
        2: Beginner
        3: Experienced
        4: Management
        5: Executive
        6: Senior Experience
    country: Country of item in string
        de: germany
        at: austraia
        ch: switzerland
        non dach = Other
    region: region if item country code is de, string format
    paid: if job is a paid role or not, 0-1
    etype: employment type ranging from 0-5
        0: unkown
        1: full-time
        2: part-time
        3: freelancer
        4: intern
        5: voluntary
    time: python time class of time created
    """

    def __init__(self, title, tags, clevel, indus, disc,
                 country, region, paid, etype, time):
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


class Interaction:
    """
    Model of the interactions hosting all data found in the dataset given in
    the csv. Also contains features to be used in the learning system.

    Parameters
    ----------
    user: class of user
    item: class of item
    interaction_type: type of implicit interaction 0-5
        0: impression
        1: click
        2: bookmark
        3: apply or reply
        4: delete
        5: recruiter click/interest
    time: python time class of interation
    """

    def __init__(self, user, item, interaction_type, time):
        self.user = user
        self.item = item
        self.interaction_type = interaction_type
        self.time = time


    def jobroles_match(self):
        """
        Feature: [0..1] value of concepts of users jobroles intersection
                 precentage with item title concepts.
        """
        return float(len(
            set(self.user.jobroles).intersection(set(self.item.title))))


    def clevel_match(self):
        """
        Feature: matching user and item career level
        """
        if self.user.clevel == self.item.clevel:
            return 1.0
        else:
            return 0.0


    def indus_match(self):
        """
        Feature: matching user and item industry
        """
        if self.user.indus == self.item.indus:
            return 1.0
        else:
            return 0.0


    def discipline_match(self):
        """
        Feature: matching user and item discipline
        """
        if self.user.disc == self.item.disc:
            return 2.0
        else:
            return 0.0


    def country_match(self):
        """
        Feature: matching user and item country position
        """
        if self.user.country == self.item.country:
            return 1.0
        else:
            return 0.0


    def region_match(self):
        """
        Feature: matching user and item country position and if region is
                 stated as would be with country de, then match region aswell.
        """
        if self.country_match() == 1.0 and self.user.country == "de":
            if self.user.region == self.item.region:
                return 1.0
            else:
                return 0.75
        elif self.country_match() == 1.0:
            return 0.5
        else:
            return 0


    def payed_experienced(self):
        """
        Feature: match unpayed jobs with beginner career level users.
        """
        if self.item.paid == 1:
            if self.user.clevel > 1:
                return 1.0
            else:
                return 0.5
        else:
            if self.user.clevel > 1:
                return 0.0
            else:
                return 0.5


    def jobroles_tag_match(self):
        """
        Feature: Jaccard similarity of user job roles and item title/tag
                 features.
        """
        jobroles = set(self.user.jobroles)
        tags = set(self.item.title).union(set(self.item.tags))
        return float(len(jobroles.intersection(tags)))/float(len(jobroles.union(tags)))


    def features(self):
        """
        Returns score of the feature values for the user item pair.
        """
        return [
            self.jobroles_match(), self.clevel_match(), self.indus_match(),
            self.discipline_match(), self.country_match(), self.region_match(),
            self.payed_experienced(), self.jobroles_tag_match()
        ]

    def label(self):
        if self.interaction_type == 4:
            return 0.0
        else:
            return 1.0
