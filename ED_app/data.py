import pandas as pd


# Getting the data
def get_data():
    data = [[1, 5, 5], [2, 2, 3], [3, 4, 1], [4, 3, 2], [5, 4, 1], [6, 2, 1], [7, 2, 4]]
    return pd.DataFrame(data, columns=['Date', 'Water Usage', 'Power Usage'])

def set_baseline(df):
    baseline_df = df.iloc[:6]
    water_usage_baseline = baseline_df['Water Usage'].mean()
    power_usage_baseline = baseline_df['Power Usage'].mean()
    water_cost_baseline = baseline_df['Water Cost'].mean()
    power_cost_baseline = baseline_df['Power Cost'].mean()
    return water_usage_baseline, power_usage_baseline, water_cost_baseline, power_cost_baseline
