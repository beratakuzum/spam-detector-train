import logging
import pandas as pd

"""
User başına aramaların spam olarak etiketlenebilmesi 
için ön koşul olarak call_count  en az 5 belirlenmiştir;
Eğer bu koşul, aşağıdakilerden biri ile birlikte sağlanıyorsa
user spam olarak etiketlenmelidir.

1. call_count'un yuzde 50'sinden azı answered ise;
2. answered başına 5 saniyeden az konuşulmuş ise;

"""


def label_data(call_data: list) -> pd.DataFrame:
    logging.info("Labelling data...")

    for data in call_data:
        if data['call_count'] > 4:
            if data['answered_call'] < (data['call_count'] / 2):
                data['is_spam'] = True

            elif data['answered_call'] > 0 and (data['total_duration (second)'] / data['answered_call']) < 5:
                print(data['user_id'], "  ", data['total_duration (second)'] / data['answered_call'])
                data['is_spam'] = True

            else:
                data['is_spam'] = False

        else:
            data['is_spam'] = False

    return pd.DataFrame(call_data)
