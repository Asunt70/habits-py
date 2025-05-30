# Create habit, choosing unit, choosing type and name
import json
from functions import multi_int_input

with open('metadata.json', 'r') as f:
    meta = json.load(f)

m_choose_habits = meta['choose-habits']['query']

with open('habits-template.json', 'r') as f:
    habits = json.load(f)

#if 'y' in ask_water:
 #   data['water']['enabled'] = 'yes'
#else:
  #  data['water']['enabled'] = 'no'

choose_habits = multi_int_input(f'{m_choose_habits}')
user_habits = {}
if choose_habits == 0:
    print('all selected')
else:
    #think of make it direct, example: update water: enabled true
    for choice in choose_habits:
        if choice == 1:
            user_habits.update({"water": habits['water']})
        elif choice == 2:
            user_habits.update({"weight": habits['weight']})
        elif choice == 3:
            user_habits.update({"exercise": habits['exercise']})
        elif choice == 4:
            user_habits.update({"meditation": habits['meditation']})
        elif choice == 5:
            user_habits.update({"reading": habits['reading']})
        elif choice == 6:
            user_habits.update({"studying": habits['studying']})
        elif choice == 7:
            user_habits.update({"mod": habits['mod']})
        else:
            print('please enter a correct value')
            break


with open('user/user-habits.json', 'w') as f:
    json.dump(user_habits,f)
#with open('habits-template.json', 'w') as f:
 #   json.dump(data,f)