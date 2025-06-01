import json
import pandas as pd
import datetime

def load_habits():
    with open('user/user-habits.json') as f:
        data = json.load(f)
    return ['date'] + list(data.keys())

def get_time():
    x = datetime.datetime.now()
    return x.strftime("%x")

def main():
    columns = load_habits()
    try:
        df = pd.read_csv('user/daily_data.csv')
    except:    
        df = pd.DataFrame(columns=columns)
        df.to_csv("user/daily_data.csv", index=False)

    date = get_time()

    def daily():
        data = {'date': date}
        habits = columns[1:]
        for habit in habits:
            data[habit] = input(f'{habit} insert units\n==> ')
        return data

    final_data = daily()

    df = pd.concat([df, pd.DataFrame([final_data])], ignore_index=True)
    df.to_csv("user/daily_data.csv", index=False)
