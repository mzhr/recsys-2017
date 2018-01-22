from baseline import learner, model, parser 
import random

import csv
import time

def minify_interactions(directory):
    # Set directory strings
    users_file = directory + "/users.csv"
    items_file = directory + "/items.csv"
    interactions_file = directory + "/interactions.csv"

    # Parse users and items into a dictionary each
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))

    interactions = {}

    with open(directory + "/interactions.csv") as fo:
        next(fo)
        for line in fo:
            newline = line.strip().split()
            if (int(newline[0]), int(newline[1])) not in interactions:
                interactions[(int(newline[0]), int(newline[1]))] = [(int(newline[2]), int(newline[3]))]
            else:
                interactions[(int(newline[0]), int(newline[1]))].append(
                        (int(newline[2]), int(newline[3]))) 

    with open("minified_interactions.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        for key, value in interactions.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            writeline = []
            writeline.extend([key[0], key[1]])
            for i in sort:
                writeline.extend([i[0], i[1]])
            csvwriter.writerow(writeline)


def interacted_with(directory):
    # Set directory strings
    users_file = directory + "/users.csv"
    items_file = directory + "/items.csv"
    interactions_file = directory + "/minified_interactions.csv"

    # Parse users and items into a dictionary each
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))

    interactions = parser.parse_interactions(interactions_file, users, items)

    item_interactions = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
    user_interactions = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}}

    # For each user-item pair, get the latest of that interaction type and add in
    for key, value in interactions.items():
        most_recent = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for i in value.interactions:
            if i.time > most_recent[i.i_type]:
                most_recent[i.i_type] = i.time
        
        added_user = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False}
        added_item = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False}
        for i in value.interactions:
            if added_user[i.i_type] == False:
                if key[0] in user_interactions[i.i_type]:
                    user_interactions[i.i_type][key[0]] += [(key[1], most_recent[i.i_type])]
                    added_user[i.i_type] = True
                else: 
                    user_interactions[i.i_type][key[0]] = [(key[1], most_recent[i.i_type])]
                    added_user[i.i_type] = True

            if added_item[i.i_type] == False:
                if key[1] in item_interactions[i.i_type]:
                    item_interactions[i.i_type][key[1]] += [(key[0], most_recent[i.i_type])]
                    added_item[i.i_type] = True
                else: 
                    item_interactions[i.i_type][key[1]] = [(key[0], most_recent[i.i_type])]
                    added_item[i.i_type] = True

    for inter_type in range(6):
        for key, value in user_interactions[inter_type].items():
                sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
                user_interactions[inter_type][key] = [item for item, time in sort]

        for key, value in item_interactions[inter_type].items():
                sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
                item_interactions[inter_type][key] = [item for item, time in sort]

    for inter_type in range(6):
        with open("user_interactions" + str(inter_type) + ".csv", "w") as userf:
            for key, value in user_interactions[inter_type].items():
                string = str(key)
                for v in value:
                    string += " " + str(v)
                string += "\n"
                userf.write(string)

                
        with open("item_interactions" + str(inter_type) + ".csv", "w") as itemf:
            for key, value in item_interactions[inter_type].items():
                string = str(key)
                for v in value:
                    string += " " + str(v)
                string += "\n"
                itemf.write(string)

        userf.close()
        itemf.close()



def sampled_interactions(directory, p_count, n_count):
    # Set directory strings
    users_file = directory + "/users.csv"
    items_file = directory + "/items.csv"
    interactions_file = directory + "/minified_interactions.csv"
    user_interactions_file = directory + "/user_interactions"
    item_interactions_file = directory + "/item_interactions"

    # Parse users and items into a dictionary each

    print("Parsing Items and Users...")
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))

    # Parse interacted data
    print("Parsing interacted with items...")
    for itype in range(6):
        for line in open(user_interactions_file + str(itype) + ".csv"):
            newline = line.split()
            user = int(newline[0])
            users[user].interacted_with[itype] = []
            for i in newline[1:]:
                users[user].interacted_with[itype] += [int(i)]

    print("Parsing interacted with users...")
    for itype in range(6):
        for line in open(item_interactions_file + str(itype) + ".csv"):
            newline = line.split()
            item = int(newline[0])
            items[item].interacted_with[itype] = []
            for i in newline[1:]:
                items[item].interacted_with[itype] += [int(i)]

    print("Building unbuilt interaction lists...")
    for key, value in users.items():
        for i in range(6):
            if i not in users[key].interacted_with:
                users[key].interacted_with[i] = []

    for key, value in items.items():
        for i in range(6):
            if i not in items[key].interacted_with:
                items[key].interacted_with[i] = []

    interactions = parser.parse_interactions(interactions_file, users, items)

    sample = {}
    item_statistics = {}
    for key, i in items.items():
        item_statistics[key] = [0,0, []]

    print("Adding recruited and deleted users to set")
    for key, value in interactions.items():
        if value.interaction_weight() == -1.0 and item_statistics[key[1]][1] < n_count and key[0] not in item_statistics[key[1]][2]:
            sample[key] = value
            item_statistics[key[1]][1] += 1
            item_statistics[key[1]][2] += [key[0]]

        if value.interaction_weight() == 4.0 and item_statistics[key[1]][0] < p_count and key[0] not in item_statistics[key[1]][2]:
            sample[key] = value
            item_statistics[key[1]][0] += 1
            item_statistics[key[1]][2] += [key[0]]

        if value.interaction_weight() == 3.0 and item_statistics[key[1]][0] < p_count and key[0] not in item_statistics[key[1]][2]:
            sample[key] = value
            item_statistics[key[1]][0] += 1
            item_statistics[key[1]][2] += [key[0]]

        if value.interaction_weight() == 2.0 and item_statistics[key[1]][0] < p_count and key[0] not in item_statistics[key[1]][2]:
            sample[key] = value
            item_statistics[key[1]][0] += 1
            item_statistics[key[1]][2] += [key[0]]

        if value.interaction_weight() == 1.0 and item_statistics[key[1]][0] < p_count and key[0] not in item_statistics[key[1]][2]:
            sample[key] = value
            item_statistics[key[1]][0] += 1
            item_statistics[key[1]][2] += [key[0]]

    data_dicts = model.data_dicts()
 
    print("Negative random sampling")
    list_set = list(users.keys())
    for key, value in items.items():
        print(value.interacted_with)
        if not [len(l) for k, l in value.interacted_with.items() if len(l) > 0]:
            continue
        while item_statistics[key][1] < n_count:
            u = random.choice(list_set)
            if u not in item_statistics[key][2] and (u, key) not in sample and not not [len(l) for k, l in users[u].interacted_with.items() if len(l) > 0]:
                sample[(u, key)] = model.Interactions(users[u], items[key], [model.Interaction(4, int(time.time()))], data_dicts)
                item_statistics[key][1] += 1
                item_statistics[key][2] += [u]

    with open("sampled_interactions.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for key, value in sample.items():
            sort = sorted(value.interactions, key=(lambda x: -x.time))
            writeline = []
            writeline.append(str(key[0]))
            writeline.append(str(key[1]))
            for i in sort:
                writeline.append(str(i.i_type))
                writeline.append(str(i.time))
            csvwriter.writerow(writeline)


