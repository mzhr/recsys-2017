"""
Build recommendations based on trained XGBoost model

by Daniel Kohlsdorf
"""


from baseline import model

import xgboost as xgb
import numpy as np

def worker(item_ids, target_users, items, users, output_file, bst, user_cw, item_cw):
    with open(output_file, "w") as file_pointer:
        pos = 0
        average_score = 0.0
        num_evaluated = 0.0
        for item in item_ids:
            data = []
            ids = []

            # build all user-feature pairs based for this item
            for user in target_users:
                interaction = model.Interactions(users[user], items[item], [])
                data += [interaction.features(items, user_cw, float(len(users)), item_cw, float(len(items)))]
                ids += [user]

            # predictions from XGBoost
            test_matrix = xgb.DMatrix(np.array(data))
            pred = bst.predict(test_matrix)
            average_score += sum(pred)
            num_evaluated += float(len(pred))

            # use all items with a score above the given threshold and sort the result
            pred_ids = sorted([
                    (ids_p, pred_p) for pred_p, ids_p in zip(pred, ids) #if pred_p > 0
                    ], key=(lambda x: -x[1]))[0:99]

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
