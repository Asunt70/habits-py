import json 
from first_run import main as first

with open('config.json') as f:
    config = json.load(f)

first_run_flag = config['first-run']

if first_run_flag == 'false':
    first()

print('welcome!')
 