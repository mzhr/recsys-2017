"""
Parsing the ACM Recsys Challenge 2017 data into interactions,
items and user models.

by Daniel Kohlsdorf
"""

from baseline import model

def is_header(line):
    return "recsyschallenge" in line


def process_header(header):
    col = {}
    pos = 0
    for name in header:
        col[name.split(".")[1]] = pos
        pos += 1
    return col


def parse_interactions(from_file, users, items):
    interactions = {}
    lc = 0
    dicts = model.data_dicts()
    for line in open(from_file):
        line = [int(a.strip("(),")) for a in line.split()]
        #assert(len(line)%2 == 0)
        keys = tuple(line[:2])

        interactions[keys] = model.Interactions(users[keys[0]], items[keys[1]], [], dicts)
        for n in range(2, len(line), 2):
            interactions[keys].interactions.append(model.Interaction(line[n], line[n+1]))
            
        lc += 1
        if lc % 100000 == 0:
            print("... reading line " + str(lc) + " from file " + from_file)

    return(interactions)


def select(from_file, where, to_object, index):
    header = None
    data = {}
    i = 0
    for line in open(from_file):
        if is_header(line):
            header = process_header(line.strip().split("\t"))
        else:
            cmp = line.strip().split("\t")
            if where(cmp):
                obj = to_object(cmp, header)
                if obj != None:
                    data[index(cmp)] = obj
        i += 1
        if i % 100000 == 0:
            print("... reading line " + str(i) + " from file " + from_file)
    return(header, data)


def build_user(str_user, names):
    return model.User(
        int(str_user[names["id"]]),
        [int(x) for x in str_user[names["jobroles"]].split(",") if len(x) > 0],
        int(str_user[names["career_level"]]),
        int(str_user[names["industry_id"]]),
        int(str_user[names["discipline_id"]]),
        int(str_user[names["experience_n_entries_class"]]),
        int(str_user[names["experience_years_experience"]]),
        int(str_user[names["experience_years_in_current"]]),
        int(str_user[names["edu_degree"]]),
        [int(x) for x in str_user[names["edu_fieldofstudies"]].split(",") if len(x) > 0],
        str_user[names["country"]],
        int(str_user[names["region"]]),
        int(str_user[names["wtcj"]]),
        int(str_user[names["premium"]])
    )


def build_item(str_item, names):
    return model.Item(
        int(str_item[names["id"]]),
        [int(x) for x in str_item[names["title"]].split(",") if len(x) > 0],
        [int(x) for x in str_item[names["tags"]].split(",") if len(x) > 0],
        int(str_item[names["career_level"]]),
        int(str_item[names["industry_id"]]),
        int(str_item[names["discipline_id"]]),
        str_item[names["country"]],
        int(str_item[names["region"]]),
        int(str_item[names["is_payed"]]),
        float(str_item[names["latitude"]]) if str_item[names["latitude"]] != "null" else None,
        float(str_item[names["longitude"]]) if str_item[names["latitude"]] != "null" else None,
        int(str_item[names["employment"]]),
        int(str_item[names["created_at"]]) if (str_item[names["created_at"]] != "null" and str_item[names["created_at"]] != "None") else None,
    )


class InteractionBuilder:
    def __init__(self, user_dict, item_dict):
        self.user_dict = user_dict
        self.item_dict = item_dict
        self.user_item_pair = {}

    def build_interaction(self, str_inter, names):
        dicts = model.data_dicts()
        item_id = int(str_inter[names["item_id"]])
        user_id = int(str_inter[names["user_id"]])
        if (item_id in self.item_dict and user_id in self.user_dict):
            i = model.Interaction(
                int(str_inter[names["interaction_type"]]),
                int(str_inter[names["created_at"]]))
            if (user_id, item_id) in self.user_item_pair:
                self.user_item_pair[(user_id, item_id)].interactions.append(i)
            else:
                self.user_item_pair[(user_id, item_id)] = model.Interactions(self.user_dict[user_id], self.item_dict[item_id], [i], dicts)
            return i
        else:
            print("Interaction not in item or user set.")
            return None
