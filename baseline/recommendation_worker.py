"""
Build recommendations based on trained XGBoost model

by Daniel Kohlsdorf
"""

from time import time, gmtime
from baseline.model import Interaction, Interactions
import xgboost as xgb
import numpy as np


TH = 0.8

def classify_worker(item_ids, target_users, items, users, output_file, model):
    """
    Method for taking in targets, training data, the data set, the model to
    split the output of predicitions.
    """
    with open(output_file, "w") as file_pointer:
        pos = 0
        average_score = 0.0
        num_evaluated = 0.0
        for item in item_ids:
            data = []
            ids = []

            # build all (user, item) pair features based for this item
            for user in target_users:
                interaction = Interactions(users[user], items[item], [])
                if interaction.jobroles_match() > 0:
                    features = interaction.features()
                    data += [features]
                    ids += [user]

            if len(data) > 0:
                # predictions from XGBoost
                test_matrix = xgb.DMatrix(np.array(data))
                pred = model.predict(test_matrix)

                # compute average score
                average_score += sum(pred)
                num_evaluated += float(len(pred))

                # use all items with a score above the given threshold and sort the result
                pred_ids = sorted(
                    [
                        (ids_p, pred_p) for pred_p, ids_p in zip(pred, ids) if pred_p > TH
                    ],
                    key=(lambda x: -x[1])
                )[0:99]

                # write the results to file
                if len(pred_ids) > 0:
                    item_id = str(item) + "\t"
                    file_pointer.write(item_id)
                    for j in range(0, len(pred_ids)):
                        user_id = str(pred_ids[j][0]) + ","
                        file_pointer.write(user_id)
                    user_id = str(pred_ids[-1][0]) + "\n"
                    file_pointer.write(user_id)
                    file_pointer.flush()

            # Every 100 iterations print some stats
            if pos % 100 == 0:
                try:
                    score = str(average_score / num_evaluated)
                except ZeroDivisionError:
                    score = str(0)
                percentage_down = str(pos / float(len(item_ids)))
                print(output_file + " " + percentage_down + " " + score)
            pos += 1
