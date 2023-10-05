import pandas as pd
import random

# Getting the data
def get_data():
    data = []
    for i in range(1, 121):
        random_int_1 = random.randint(1, 8)
        random_int_2 = random.randint(1, 8)
        data.append([i, random_int_1, random_int_2])
    return pd.DataFrame(data, columns=['Date', 'Water Usage', 'Power Usage'])

def set_baseline(df):
    baseline_df = df.iloc[:6]
    water_usage_baseline = baseline_df['Water Usage'].mean()
    power_usage_baseline = baseline_df['Power Usage'].mean()
    water_cost_baseline = baseline_df['Water Cost'].mean()
    power_cost_baseline = baseline_df['Power Cost'].mean()
    return water_usage_baseline, power_usage_baseline, water_cost_baseline, power_cost_baseline

def change_timeline(df, timeline):
    if timeline == 'Weekly':
        weekly_df = pd.DataFrame(columns=['Date', 'Water Usage', 'Power Usage', 'Water Cost', 'Power Cost'])
        i = 1
        while len(df) > 6:
            week = df.iloc[0:6].copy()
            week_water_usage = week['Water Usage'].mean()
            week_power_usage = week['Power Usage'].mean()
            week_water_cost = week['Water Cost'].mean()
            week_power_cost = week['Power Cost'].mean()
            new_row = {'Date': i, 'Water Usage': week_water_usage, 'Power Usage': week_power_usage,
                       'Water Cost': week_water_cost, 'Power Cost': week_power_cost}
            weekly_df.loc[len(weekly_df)] = new_row
            i = i + 1
            df = df.drop(df.index[0:6])
            df = df.reset_index(drop=True)
        return weekly_df
    elif timeline == 'Monthly':
        monthly_df = pd.DataFrame(columns=['Date', 'Water Usage', 'Power Usage', 'Water Cost', 'Power Cost'])
        i = 1
        while len(df)> 29:
            month = df.iloc[0:29].copy()
            month_water_usage = month['Water Usage'].mean()
            month_power_usage = month['Power Usage'].mean()
            month_water_cost = month['Water Cost'].mean()
            month_power_cost = month['Power Cost'].mean()
            new_row = {'Date': i, 'Water Usage': month_water_usage, 'Power Usage': month_power_usage,
                       'Water Cost': month_water_cost, 'Power Cost': month_power_cost}
            monthly_df.loc[len(monthly_df)] = new_row
            i = i + 1
            df = df.drop(df.index[0:29])
            df = df.reset_index(drop=True)
        return monthly_df

