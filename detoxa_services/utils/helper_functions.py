import uuid
from rest_framework import exceptions


def unique_s3_key():
    unique = str(uuid.uuid4())
    key = "detoxa" + unique
    return key


def mandatory_params(**kwargs):
    for key, value in kwargs.items():
        if value is None or value == '':
            raise exceptions.ValidationError("{} is required.".format(key))


def mandatory_key_exist(data, test_name, test_question_answer):
    keys = ['child', 'gender', 'light_on_time', 'reaction_time']
    keys2 = ['actual_box_with_red_light', 'box_choose_by_child']
    if test_name == 'hand_and_eye_test_1':
        keys = keys
    else:
        keys.extend(keys2)
    for key in keys:
        if key not in data and key not in test_question_answer:
            raise exceptions.ValidationError("{} key is required.".format(key))


def check_length_of_params(data, test_name):
    params = ['light_on_time', 'reaction_time']
    params2 = ['actual_box_with_red_light', 'box_choose_by_child']
    if test_name == 'hand_and_eye_test_1':
        params = params
    else:
        params.extend(params2)
    for key in params:
        if len(data[key]) < 5:
            raise exceptions.ValidationError("Please answer all of the questions key {} having missing data".format(key))



