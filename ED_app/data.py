import pandas as pd


# Getting the data
def get_data():
    data = [[1, 5, 5], [2, 2, 3], [3, 4, 1], [4, 3, 2], [5, 4, 1], [6, 4, 1], [7, 5, 2]]
    return pd.DataFrame(data, columns=['Date', 'Water Usage', 'Power Usage'])
