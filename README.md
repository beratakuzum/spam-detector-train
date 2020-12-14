# spam-detector-train
#### Dependencies
- python 3.8
- mongodb
- scikit-learn

### How to run?

If the data is not in mongodb, you can insert it by uncommenting '# insert_data_into_mongo(db, 'users')' line in train.py. You can
create a virtual environment, install the requierements.txt and execute the command:
```sh
$ python train.py
```
After the training, a model is going to be created as spam-detector-model.pickle in the project's root folder.