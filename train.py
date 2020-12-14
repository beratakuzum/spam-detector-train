import os
import logging
import pickle

import numpy as np

from dotenv import load_dotenv
from pymongo import MongoClient

from mongo import get_train_data_from_mongo, insert_data_into_mongo
from labelling import label_data
from preprocess import encode_country_values, split_features_and_labels, binarize_columns

from sklearn import tree

logging.basicConfig(level=logging.INFO)

load_dotenv()
logging.info("mongo connection string: " + os.getenv('MONGO_CONN_STR'))

db = MongoClient(os.getenv('MONGO_CONN_STR')).get_database()

# insert_data_into_mongo(db, 'users')

"""Retrive train data from mongodb"""
call_data = get_train_data_from_mongo(db=db, collection_name='users')

"""
Train data is unlabeled. We label train data with an additional 'is_spam'
column by applying pre-determined conditions  and retrieve it as a DataFrame
"""
labeled_call_data = label_data(call_data=call_data)

"""
We binarize the 'registered_user' and 'is_spam' columns that have boolean values True and False
and retrive the labeled_call_data again as a dataframe
"""
labeled_call_data = binarize_columns(labeled_call_data, ['registered_user', 'is_spam'])

""""We split labeled_call_data into two dataframes as labels and features"""
labels, features = split_features_and_labels(labeled_call_data)

""" Since the 'country' column is of string type, we one-hot encode it """
features = encode_country_values(features)

"""Convert the features and labels dataframes to numpy arrays"""
X = features.to_numpy()
y = np.array([label[0] for label in labels.to_numpy()])

logging.info("Started training...")
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y)

logging.info("Training finished. Now dumping the model...")
pickle.dump(clf, open('spam-detector-model.pickle', 'wb'))

logging.info("Printing out some predictions...")

for i in range(5):
    if clf.predict([X[i]])[0] == 1:
        print("user ", i, " is spam")

    else:
        print("user ", i, " is not spam")
