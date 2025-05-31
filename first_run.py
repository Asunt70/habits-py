import json
from functions import yes_no_prompt, multi_int_input


#with open(user_preferences) as f:
 #  f.write()
#user_preferences_zero = open('user/user-preferences.json', 'w')
#user_preferences = open('user/user-preferences.json', 'a')

#update first_run_flag
with open('config.json', 'r') as f:
   config = json.load(f)

#metadata
with open('metadata.json', 'r') as f:
   meta = json.load(f)

m_choose_habits = meta['choose-habits']['query']
m_welcome = meta['first-run']['welcome']
m_ask_name = meta['first-run']['ask-name']
m_ask_cheer = meta['first-run']['ask-cheer']
m_tell_max_phrases = meta['first-run']['tell-max-phrases']
m_ask_cheers = meta['first-run']['ask-cheers']
m_invalid_option = meta['errors']['invalid-option']
m_no_cheers = meta['first-run']['no-cheers']
m_confirm_cheers = meta['first-run']['confirm-cheers']

#variables
user_data = {}
name = ""

def get_name():
   name = str(input(f'{m_ask_name}'))
   user_data['name'] = name
   print(f'{name} {m_welcome}')
   print("--------------")
   return user_data

def strip_list(items):
    for i in items:
        return i.strip()
def confirm_cheers(value):
   confirm_cheers = yes_no_prompt(f'{m_confirm_cheers}')
   if 'y' in confirm_cheers:
      user_data['cheers'] = value
      return user_data
   else:
      pass

def create_cheers():
   while True:
      ask_cheer_message = yes_no_prompt(f'{m_ask_cheer}')
      if 'y' in ask_cheer_message:
         print(f'{m_tell_max_phrases}')
         cheers = str(input(f'{m_ask_cheers}'))
         cheer_list = cheers.split(", ")
         for cheer in cheer_list:
            print(cheer)
         if confirm_cheers(cheer_list):
            return
         else:
            print("Okay, we will re-run previous commands!")
      else:
         print(f'{m_no_cheers}')
         return
      
# Create habit, choosing unit, choosing type and name

with open('habits-template.json', 'r') as f:
    habits = json.load(f)
#if 'y' in ask_water:
 #   data['water']['enabled'] = 'yes'
#else:
  #  data['water']['enabled'] = 'no'

def f_choose_habits(): 
    choose_habits = multi_int_input(f'{m_choose_habits}')
    user_habits = {}
    for choice in choose_habits:
        if choice == 0:
           print('all selected')
           with open('user/user-habits.json', 'w') as f:
               json.dump(habits,f)
               break
        elif choice == 9:
            break
        else:
        #think of make it direct, example: update water: enabled true
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
                user_habits.update({"study": habits['study']})
            elif choice == 7:
                user_habits.update({"mod": habits['mod']})
            else:
                print('please enter a correct value')
                break
    
            with open('user/user-habits.json', 'w') as f:
                json.dump(user_habits,f)
            print('done!') #show user which options they've choosen

def main():
   get_name()  
   create_cheers()
   f_choose_habits()
   config['first-run'] = 'true'
   with open('user/user_data.json', 'w') as f:
      json.dump(user_data,f)
   with open('config.json', 'w') as f:
      json.dump(config,f)
      