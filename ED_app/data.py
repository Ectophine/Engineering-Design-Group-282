import pandas as pd
from datetime import datetime, timedelta
from watchdog.events import FileSystemEventHandler
import ED_app.config


def get_data():
    df = pd.read_csv('ED_app/data/storeddata.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df


class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print('File was modified!')
        current_time = datetime.now()
        if (current_time - ED_app.config.last_update_time) > timedelta(seconds=10):
            ED_app.config.last_update_time = current_time
            update_data()


def parse_log_file(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    data = [line.strip().split(sep=' | ') for line in lines]
    for line in data:
        line[0] = float(line[0][:-3])
        line[1] = float(line[1][:-6])
        line[2] = float(line[2][12:-2])
        line[3] = float(line[3][:-3])

    df = pd.DataFrame(data, columns=['MS', 'Flow Rate', 'Temperature', 'Total Water Usage'])

    return df


def update_data():
    current_date = pd.to_datetime('now')
    old_df = get_data()
    new_df = parse_log_file('ED_app/data/log/sensorlog')
    avg_temp = new_df['Temperature'].mean()
    water_usage = new_df.iloc[-1]['Total Water Usage']
    new_row = pd.DataFrame([[current_date, water_usage, avg_temp]], columns=['Date', 'Water Usage', 'Temperature'])
    updated_df = pd.concat([old_df, new_row], ignore_index=True)
    updated_df.to_csv('ED_app/data/storeddata.csv', index=False)
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
        while len(df) > 6:
            week = df.iloc[0]['Date'].week
            year = df.iloc[0]['Date'].year
            filtered_week = df[df['Date'].dt.isocalendar().week == week]
            filtered = filtered_week[filtered_week['Date'].dt.year == year]
            entry_count = len(filtered)
            week_water_usage = filtered['Water Usage'].mean()
            week_gas_usage = filtered['Gas Usage'].mean()
            week_water_cost = filtered['Water Cost'].mean()
            week_gas_cost = filtered['Gas Cost'].mean()
            new_row = {'Date': filtered.iloc[0]['Date'], 'Water Usage': week_water_usage, 'Gas Usage': week_gas_usage,
                       'Water Cost': week_water_cost, 'Gas Cost': week_gas_cost}
            weekly_df.loc[len(weekly_df)] = new_row
            df = df.drop(df.index[0:entry_count])
            df = df.reset_index(drop=True)
        return weekly_df
    elif timeline == 'Monthly':
        monthly_df = pd.DataFrame(columns=['Date', 'Water Usage', 'Gas Usage', 'Water Cost', 'Gas Cost'])
        while len(df) > 15:
            target = df.iloc[0]['Date'].strftime('%Y-%m')
            filtered = df[df['Date'].dt.strftime('%Y-%m') == target]
            entry_count = len(filtered)
            month_water_usage = filtered['Water Usage'].mean()
            month_gas_usage = filtered['Gas Usage'].mean()
            month_water_cost = filtered['Water Cost'].mean()
            month_gas_cost = filtered['Gas Cost'].mean()
            new_row = {'Date': target, 'Water Usage': month_water_usage, 'Gas Usage': month_gas_usage,
                       'Water Cost': month_water_cost, 'Gas Cost': month_gas_cost}
            monthly_df.loc[len(monthly_df)] = new_row

            df = df.drop(df.index[0:entry_count])
            df = df.reset_index(drop=True)
        return monthly_df


def calculate_savings(df):
    water_usage, gas_usage, water_cost, gas_cost = set_baseline(df)
    df['Water Usage Savings'] = water_usage - df['Water Usage']
    df['Gas Usage Savings'] = gas_usage - df['Gas Usage']
    df['Water Cost Savings'] = water_cost - df['Water Cost']
    df['Gas Cost Savings'] = gas_cost - df['Gas Cost']
    return df
