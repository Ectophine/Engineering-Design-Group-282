import pandas as pd


# Getting the data
def get_data():
    data = [[1, 5, 5], [2, 2, 3], [3, 4, 1]]
    return pd.DataFrame(data, columns=['Date', 'Water Usage', 'Power Usage'])
