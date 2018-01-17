from time import time
from ..baseline import xgb, model

def fold10(interactions, fold):
    """
    Fold Cross validation of the learning model
    """

    # Fold must be between 0 and 10
    assert fold > 0 and fold < 10

    # Times of interactions from first time to final event evem distribution
    fold_splits = [1478392842, 
                   1478981224, 
                   1479386595,
                   1483518634,
                   1483961181,
                   1484302454,
                   1484648610,
                   1485179035,
                   1485384558,
                   1485845069,
                   1486506722]
    fold_time = fold_splits[fold]

    (users, items, data_interactions, target_interactions, target_users, target_items) = build_validation_data(interactions, fold_time)
    result_name = "test" + str(fold) + str(time())[:10] + ".csv"
    xgb.baseline_learn(users, items,
                       data_interactions, 
                       target_users, target_items, result_name)
    score = calculate_score(result_name, target_interactions)
    print("Score of fold " + str(fold) + " is " + str(score))


def build_validation_data(interactions, fold_time):
    # Split target users and interactions based on that,
    target_interactions = {}
    data_interactions = {}
    users = {} 
    items = {} 
    target_users = set()
    target_items = set()

    def add_interaction(data, key, interaction, user, item):
        if key in data:
            data[key].interactions.append(interaction)
        else:
            data[key] = model.Interactions(user, item, [interaction])

    print("Creating Validation data")
    for key, value in interactions.items():
        for i in value.interactions:
            users[value.user.id] = value.user
            items[value.item.id] = value.item
            if i.time > fold_time: 
                if (len(target_items) < 15000 or value.item.id in target_items) and (len(target_users) < 15000 or value.user.id in target_users):
                    target_items.add(value.item.id)
                    target_users.add(value.user.id)
                    add_interaction(target_interactions, key, i, value.user, value.item)
            else:
                add_interaction(data_interactions, key, i, value.user, value.item)

    target_users = list(target_users)
    target_items = list(target_items)
    return (users, items, data_interactions, target_interactions, target_users, target_items)


def calculate_score(result_name, target_interactions):
    # Calculate Score
    total_score = 0
    for line in open(result_name):
        # Parse line into id's wiht suers as sets for quick compare
        result = line.strip().split("\t")
        if len(result) == 1:
            continue
        item = int(result[0])
        recommendations = result[1].split(",")
        for u in range(len(recommendations)):
            recommendations[u] = int(recommendations[u])

        recommendations = list(set(recommendations))
        user_scores = []
        item_score = 0
        paid = 1

        print("Calculating item scores for item: " + str(item))
        # User Success
        for user in recommendations:
            user_score = 0
            if tuple([user, item]) in target_interactions:
                for i in target_interactions[tuple([user, item])].interactions:
                    if i.i_type == 1:
                        user_score +=1
                    elif  i.i_type == 2 or i.i_type == 3:
                        user_score +=5
                    elif i.i_type == 5:
                        user_score += 20
                    elif i.i_type == 2:
                        user_score -= 10
                if target_interactions[tuple([user, item])].user.premium == 1:
                    user_score *= 2
                if target_interactions[tuple([user, item])].item.paid == 1:
                    paid *= 2

                user_scores.append(user_score)

        # Item Success
        item_scores = [item for item in user_scores if item > 0]
        if len(item_scores) > 0:
            item_score = 25 * paid

        # Score
        total_score += sum(user_scores) + item_score
    
    return total_score

