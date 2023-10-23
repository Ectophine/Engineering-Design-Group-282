import pandas as pd
import random
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


# Getting the data
def get_data():
    data = []
    for i in range(1, 121):
        random_int_1 = random.randint(90, 160)
        random_int_2 = random.randint(37, 43)
        data.append([i, random_int_1, random_int_2])
    return pd.DataFrame(data, columns=['Date', 'Water Usage', 'Temperature'])


def get_data_real():
    stored_data = 'storeddata.csv'
    df = pd.read_csv(stored_data)
    return df


last_update_time = datetime.now


class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global last_update_time
        current_time = datetime.now()

        if event.src_path == 'sensorlog':
            if (current_time - last_update_time) > timedelta(minutes=1):
                last_update_time = current_time
                update_data()


def parse_log_file(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    data = [line.strip().split(sep='|') for line in lines]

    df = pd.DataFrame(data, columns=['MS', 'Flow Rate', 'Temperature', 'Total Water Usage'])
    return df


def update_data():
    stored_data = 'storeddata.csv'
    new_data = 'sensorlog'
    current_date = datetime.now()
    old_df = pd.read_csv(stored_data)
    new_df = parse_log_file(new_data)
    avg_temp = new_df['Temperature'].mean()
    final_row = new_df.iloc[-1]
    final_row['Date'] = current_date
    updated_df = old_df.append(final_row, ignore_index=True)
    updated_df.to_csv(stored_data, index=False)
    return updated_df


def set_baseline(df):
    baseline_df = df.iloc[:6]
    water_usage_baseline = baseline_df['Water Usage'].mean()
    gas_usage_baseline = baseline_df['Gas Usage'].mean()
    water_cost_baseline = baseline_df['Water Cost'].mean()
    gas_cost_baseline = baseline_df['Gas Cost'].mean()
    return water_usage_baseline, gas_usage_baseline, water_cost_baseline, gas_cost_baseline


def change_timeline(df, timeline):
    if timeline == 'Weekly':
        weekly_df = pd.DataFrame(columns=['Date', 'Water Usage', 'Gas Usage', 'Water Cost', 'Gas Cost'])
        i = 1
        while len(df) > 6:
            week = df.iloc[0:6].copy()
            week_water_usage = week['Water Usage'].mean()
            week_gas_usage = week['Gas Usage'].mean()
            week_water_cost = week['Water Cost'].mean()
            week_gas_cost = week['Gas Cost'].mean()
            new_row = {'Date': i, 'Water Usage': week_water_usage, 'Gas Usage': week_gas_usage,
                       'Water Cost': week_water_cost, 'Gas Cost': week_gas_cost}
            weekly_df.loc[len(weekly_df)] = new_row
            i = i + 1
            df = df.drop(df.index[0:6])
            df = df.reset_index(drop=True)
        return weekly_df
    elif timeline == 'Monthly':
        monthly_df = pd.DataFrame(columns=['Date', 'Water Usage', 'Gas Usage', 'Water Cost', 'Gas Cost'])
        i = 1
        while len(df) > 29:
            month = df.iloc[0:29].copy()
            month_water_usage = month['Water Usage'].mean()
            month_gas_usage = month['Gas Usage'].mean()
            month_water_cost = month['Water Cost'].mean()
            month_gas_cost = month['Gas Cost'].mean()
            new_row = {'Date': i, 'Water Usage': month_water_usage, 'Gas Usage': month_gas_usage,
                       'Water Cost': month_water_cost, 'Gas Cost': month_gas_cost}
            monthly_df.loc[len(monthly_df)] = new_row
            i = i + 1
            df = df.drop(df.index[0:29])
            df = df.reset_index(drop=True)
        return monthly_df


def calculate_savings(df):
    water_usage, gas_usage, water_cost, gas_cost = set_baseline(df)
    df['Water Usage Savings'] = water_usage - df['Water Usage']
    df['Gas Usage Savings'] = gas_usage - df['Gas Usage']
    df['Water Cost Savings'] = water_cost - df['Water Cost']
    df['Gas Cost Savings'] = gas_cost - df['Gas Cost']
    return df
