import pandas as pd
import logging


def get_train_data_from_mongo(db, collection_name) -> list:
    logging.info("Retrieving call data from mongo...")

    # user_id'yi almıyoruz çünkü train ederken bize lazım değil
    call_data = db[collection_name].find({}, {"user_id": 0})
    call_data = list(call_data)

    for data in call_data:
        del data['_id']

    return call_data


# read call data from call_history.csv and insert it into mongo
def insert_data_into_mongo(db, collection_name):
    logging.info("inserting csv data into mongo")
    df = pd.read_csv('call_history .csv', sep=';')
    df_as_list_of_dicts = df.to_dict('records')

    # first delete old docs
    db[collection_name].remove()

    # insert calls
    db[collection_name].insert_many(df_as_list_of_dicts)
