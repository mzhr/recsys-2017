from baseline import learner, model, parser 

import csv
import time
from collections import Counter
import matplotlib.pyplot as plt

def build_visualisations3(directory):
    users_file = directory + "/users.csv"
    items_file = directory + "/items.csv"
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))

    user_cold = []
    item_cold = []

    print("Added Users Values")
    for user, value in users.items():
        cold = 0
        l = [value.clevel, value.disc, value.indus, value.country, value.region, value.expn, value.expy, value.expyc, value.edud]
        for i in l:
            if i == 0 or i is None or i == "non_dach":
                cold += 1
        user_cold += [cold]

    print("Added Items Values")
    for item, value in items.items():
        cold = 0
        l = [value.clevel, value.disc, value.indus, value.country, value.region, value.etype,
        value.lat, value.lon]
        for i in l:
            if i == 0 or i is None or i == "non_dach":
                cold += 1
        item_cold += [cold]

    u_stats = Counter(user_cold).most_common(6)
    u_stats.append(("Other", len(users)-sum(row[1] for row in u_stats)))
    i_stats = Counter(item_cold).most_common(6)
    i_stats.append(("Other", len(users)-sum(row[1] for row in i_stats)))

    bargraph_single([k for l, k in u_stats], [l for l, k in u_stats], "Most Common Count of Missing Attributes in Users")
    bargraph_single([k for l, k in i_stats], [l for l, k in i_stats], "Most Common Count of Missing Attributes in Items")


def build_visualisations2(directory):
    # Set directory strings
    users_file = directory + "/users.csv"
    items_file = directory + "/items.csv"
    interactions_file = directory + "/minified_interactions.csv"

    # Parse users and items into a dictionary each
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))

    interactions = parser.parse_interactions(interactions_file, users, items)

    user_stats = {"clevel": [], 
                  "disc": [],
                  "indus": [],
                  "country": [],
                  "region": []}

    item_stats = {"disc": [],
                  "indus": [],
                  "clevel": [],
                  "country": [],
                  "region": []}

    interaction_time = []
    interaction_type = []
    interaction_count = []

    print("Added Users Values")
    for user, value in users.items():
        user_stats["clevel"] += [value.clevel]
        user_stats["disc"] += [value.disc]
        user_stats["indus"] += [value.indus]
        user_stats["country"] += [value.country]
        user_stats["region"] += [value.region]

    print("Added Items Values")
    for item, value in items.items():
        item_stats["disc"] += [value.disc]
        item_stats["indus"] += [value.indus]
        item_stats["clevel"] += [value.clevel]
        item_stats["country"] += [value.country]
        item_stats["region"] += [value.region]

    print("Added Interactions Values")
    for key, value in interactions.items():
        interaction_count += [len(value.interactions)]
        for i in value.interactions:
            interaction_type += [i.i_type]
            interaction_time += [i.time]

    u_stats = {}
    i_stats = {}

    for key, value in user_stats.items():
        u_stats[key] = Counter(value)
    for key, value in item_stats.items():
        i_stats[key] = Counter(value)

    interaction_type = Counter(interaction_type)
    interaction_count = Counter(interaction_count)
    
    i_lables = {0: "Impression", 1: "Click", 2: "Bookmark", 3: "Reply/Apply", 4: "Delete", 5: "Recruiter Click"}
    c_lables = {0: "Unknown", 1: "Intern", 2: "Beginner", 3: "Experienced", 4: "Manager", 5: "Executive", 6: "S. Executive"}

    bargraph_single(interaction_type.values(), ([i_lables[x] for x in list(interaction_type.keys())]), "Frequency of Interaction Types")
    bargraph_single(interaction_count.values(), [str(x) for x in list(interaction_count.keys())], "Frequency of Interactions")

    for i in u_stats["clevel"].keys():
        if i_stats["clevel"][i] == 0:
            i_stats["clevel"][i] = 0
    for i in i_stats["clevel"].keys():
        if u_stats["clevel"][i] == 0:
            u_stats["clevel"][i] = 0

    for i in u_stats["country"].keys():
        if i_stats["country"][i] == 0:
            i_stats["country"][i] = 0
    for i in i_stats["country"].keys():
        if u_stats["country"][i] == 0:
            u_stats["country"][i] = 0

    for i in u_stats["region"].keys():
        if i_stats["region"][i] == 0:
            i_stats["region"][i] = 0
    for i in i_stats["region"].keys():
        if u_stats["region"][i] == 0:
            u_stats["region"][i] = 0

    for i in u_stats["indus"].keys():
        if i_stats["indus"][i] == 0:
            i_stats["indus"][i] = 0
    for i in i_stats["indus"].keys():
        if u_stats["indus"][i] == 0:
            u_stats["indus"][i] = 0

    for i in u_stats["disc"].keys():
        if i_stats["disc"][i] == 0:
            i_stats["disc"][i] = 0
    for i in i_stats["disc"].keys():
        if u_stats["disc"][i] == 0:
            u_stats["disc"][i] = 0


    timeseries(interaction_time, "Interaction by Time")
    bargraph_double(u_stats["country"].values(), i_stats["country"].values(), u_stats["country"].keys(), "User Item Country Frequency")
    bargraph_double(u_stats["disc"].values(), i_stats["disc"].values(), u_stats["disc"].keys(), "User Item Discipline Frequency")
    bargraph_double(u_stats["indus"].values(), i_stats["indus"].values(), u_stats["indus"].keys(), "User Item Industry Frequency")
    bargraph_double(u_stats["clevel"].values(), i_stats["clevel"].values(), [c_lables[x] for x in list(u_stats["clevel"].keys())], "User Item Career Level Frequency")
    bargraph_double(u_stats["region"].values(), i_stats["region"].values(), u_stats["region"].keys(), "User Item Region Frequency")


def build_visualisations(directory):
    (users, items, interactions, 
     target_users, target_items) = learner.baseline_parse(directory)

    user_stats = {"clevel": [], 
                  "disc": [],
                  "indus": [],
                  "expn": [],
                  "expy": [],
                  "expyc": [],
                  "edud": [],
                  "country": [],
                  "region": [],
                  "xtcj": [],
                  "jobroles_values": [],
                  "jobroles_count": [],
                  "edufos_values": [],
                  "edufos_count": [],
                  "premium": []} 

    item_stats = {"title_values": [],
                  "title_count": [],
                  "tags_values": [],
                  "tags_count": [],
                  "disc": [],
                  "indus": [],
                  "latlon": [],
                  "clevel": [],
                  "country": [],
                  "region": [],
                  "paid": [],
                  "time": [],
                  "etype": []}
                  
    target_items_intersect = 0
    target_users_intersect = 0
    users_length = len(users)
    items_length = len(items)
    target_items_length = len(target_items)
    target_users_length = len(target_users)
    target_items_not_in_set = 0
    target_users_not_in_set = 0
    interaction_time = []
    interaction_type = []
    interaction_count = []
    target_users_interactions = set()
    target_items_interactions = set()
    user_interactions = set()
    item_interactions = set()
    
    for user, value in users.items():
        for c in value.jobroles:
            user_stats["jobroles_values"] += [c]
        user_stats["jobroles_count"] += [len(value.jobroles)]
        for c in value.edufos:
            user_stats["edufos_values"] += [c]
        user_stats["edufos_count"] += [len(value.edufos)]
        user_stats["clevel"] += [value.clevel]
        user_stats["disc"] += [value.disc]
        user_stats["indus"] += [value.indus]
        user_stats["expn"] += [value.expn]
        user_stats["expy"] += [value.expy]
        user_stats["expyc"] += [value.expyc]
        user_stats["edud"] += [value.edud]
        user_stats["country"] += [value.country]
        user_stats["region"] += [value.region]
        user_stats["xtcj"] += [value.xtcj]
        user_stats["premium"] += [value.premium]
        if user in target_users:
            target_users_intersect += 1

    for u in target_users:
        if u not in users:
            target_users_not_in_set += 1

    for item, value in items.items():
        for c in value.title:
            item_stats["title_values"] += [c]
        item_stats["title_count"] += [len(value.title)]
        for c in value.tags:
            item_stats["tags_values"] += [c]
        item_stats["tags_count"] += [len(value.tags)]
        item_stats["disc"] += [value.disc]
        item_stats["indus"] += [value.indus]
        item_stats["clevel"] += [value.clevel]
        item_stats["country"] += [value.country]
        item_stats["region"] += [value.region]
        item_stats["paid"] += [value.paid]
        item_stats["etype"] += [value.etype]
        item_stats["time"] += [value.time]
        item_stats["latlon"] += [(value.lat, value.lon)]
        if item in target_items:
            target_items_intersect += 1

    for i in target_items:
        if i not in items:
            target_items_not_in_set += 1

    for key, value in interactions.items():
        interaction_count += [len(value.interactions)]
        for i in value.interactions:
            interaction_type += [i.i_type]
            interaction_time += [i.time]
        if value.user.id in target_users:
            target_users_interactions.add(value.user.id)
        if value.item.id in target_items:
            target_items_interactions.add(value.item.id)
        if value.item.id in items:
            item_interactions.add(value.item.id)
        if value.user.id in users:
            user_interactions.add(value.user.id)

    for key, value in user_stats.items():
        user_stats[key] = Counter(value)
    for key, value in item_stats.items():
        item_stats[key] = Counter(value)

    interaction_type = Counter(interaction_type)
    interaction_count = Counter(interaction_count)
    target_users_interactions = len(target_users_interactions)
    target_items_interactions = len(target_items_interactions)
    user_interactions = len(user_interactions)
    item_interactions = len(item_interactions)
    
    i_lables = {0: "Impression", 1: "Click", 2: "Bookmark", 3: "Reply/Apply", 4: "Delete", 5: "Recruiter Click"}
    c_lables = {0: "Unknown", 1: "Intern", 2: "Beginner", 3: "Experienced", 4: "Manager", 5: "Executive", 6: "S. Executive"}

    bargraph_single(interaction_type.values(), ([i_lables[x] for x in list(interaction_type.keys())]), "Frequency of Interaction Types")
    bargraph_single(interaction_count.values(), [str(x) for x in list(interaction_count.keys())], "Frequency of Interactions")

    for i in user_stats["clevel"].keys():
        if item_stats["clevel"][i] == 0:
            item_stats["clevel"][i] = 0
    for i in item_stats["clevel"].keys():
        if user_stats["clevel"][i] == 0:
            user_stats["clevel"][i] = 0

    for i in user_stats["country"].keys():
        if item_stats["country"][i] == 0:
            item_stats["country"][i] = 0
    for i in item_stats["country"].keys():
        if user_stats["country"][i] == 0:
            user_stats["country"][i] = 0

    for i in user_stats["region"].keys():
        if item_stats["region"][i] == 0:
            item_stats["region"][i] = 0
    for i in item_stats["region"].keys():
        if user_stats["region"][i] == 0:
            user_stats["region"][i] = 0

    for i in user_stats["indus"].keys():
        if item_stats["indus"][i] == 0:
            item_stats["indus"][i] = 0
    for i in item_stats["indus"].keys():
        if user_stats["indus"][i] == 0:
            user_stats["indus"][i] = 0

    for i in user_stats["disc"].keys():
        if item_stats["disc"][i] == 0:
            item_stats["disc"][i] = 0
    for i in item_stats["disc"].keys():
        if user_stats["disc"][i] == 0:
            user_stats["disc"][i] = 0


    timeseries(interaction_time, "Interaction by Time")

    bargraph_double(user_stats["country"].values(), item_stats["country"].values(), user_stats["country"].keys(), "User Item Country Frequency")
    bargraph_double(user_stats["disc"].values(), item_stats["disc"].values(), user_stats["disc"].keys(), "User Item Discipline Frequency")
    bargraph_double(user_stats["indus"].values(), item_stats["indus"].values(), user_stats["indus"].keys(), "User Item Industry Frequency")
    bargraph_double(user_stats["clevel"].values(), item_stats["clevel"].values(), [c_lables[x] for x in list(user_stats["clevel"].keys())], "User Item Career Level Frequency")
    bargraph_double(user_stats["region"].values(), item_stats["region"].values(), user_stats["region"].keys(), "User Item Region Frequency")

    with open("somestats.txt", "w") as f:
        for key, value in user_stats.items():
            f.write("user " + key + str(user_stats[key]) + "\n")
        for key, value in item_stats.items():
            f.write("item " + key + str(item_stats[key]) + "\n")
        f.write("uniquejobroles"+str(len(user_stats["jobroles_values"])) + "\n")
        f.write("uniquetitle"+str(len(item_stats["title_values"])) + "\n")
        f.write("uniquetags"+str(len(item_stats["tags_values"])) + "\n")
        f.write("jobrolescount"+str(user_stats["jobroles_count"]) + "\n")
        f.write("titlecount"+str(item_stats["title_count"]) + "\n")
        f.write("tagscount"+str(item_stats["tags_count"]) + "\n")
        f.write("targetuserinteractions"+str(target_users_interactions) + "\n")
        f.write("targetiteminteractions"+str(target_items_interactions) + "\n")
        f.write("userinteractions"+str(user_interactions) + "\n")
        f.write("iteminteractions"+str(item_interactions) + "\n")
        f.write("targetitemsinterset"+str(target_items_intersect) + "\n")
        f.write("targetuserintersect"+str(target_users_intersect) + "\n")
        f.write("userlength"+str(users_length) + "\n")
        f.write("itemlength"+str(items_length) + "\n")
        f.write("targetitemlength"+str(target_items_length) + "\n")
        f.write("targetuserlength"+str(target_users_length) + "\n")
        f.write("targetitemsnotinuset"+str(target_items_not_in_set) + "\n")
        f.write("targetusersnotinset"+str(target_users_not_in_set) + "\n")

def timeseries(values, title):
    n, bins = np.histogram(values, 50)
    bincenters = 0.5*(bins[1:]+bins[:-1])
    plt.plot(bincenters,n,'-')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(title)

def pigraph(values, labels, title):
    m = max(enumerate(values), key=lambda x: x[1])[0]
    explode = [0]*len(values)
    explode[m] = 0.1

    fig1, ax1 = plt.subplots()
    ax1.pie(values, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(title)

    plt.tight_layout()
    plt.savefig(title)

def bargraph_double(values1, values2, labels, title):
    ind = np.arange(len(labels))
    width = 1/(len(labels))
    fix, ax = plt.subplots()

    if len(labels) > 12:
        width = 0.3
        fig, ax = plt.subplots(figsize=(12.5, 4.75))

    rects1 = ax.bar(ind, values1, width, color='b')
    rects2 = ax.bar(ind+width, values2, width, color='r')

    ax.set_ylabel("Count")
    ax.set_title(title)
    ax.set_xticks(ind + (width-0.03)/2)
    ax.set_xticklabels(labels)

    ax.legend((rects1[0], rects2[0]), ('Users', 'Items'))

    """
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.00*height,
                    '%d' % int(height),
                    ha='center', va='bottom')



    if len(labels) < 12:
        autolabel(rects1)
        autolabel(rects2)
    """

    plt.tight_layout()
    plt.savefig(title)

def bargraph_single(values, labels, title):
    ind = np.arange(len(values))
    width = 3/len(values)

    fix, ax = plt.subplots()
    rects = ax.bar(ind, values, width, color='b')

    ax.set_ylabel("Count")
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.00*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(rects)

    plt.tight_layout()
    plt.savefig(title)
