import pickle
import numpy as np

def get_data_input(dict_input):
    input_X = []
    for key, value in dict_input.items():
        input_X.append(int(value))
    return np.array(input_X).reshape(1,-1)

def calculating_price(input_data):
    # Use the model to make a prediction
    with open('C:\\zqhome\\NYU Course\\DBS\\FinalProject\\code\\xgb_reg.pkl', 'rb') as f:
        data = pickle.load(f)
    return data.predict(input_data)