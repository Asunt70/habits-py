import json
from functions import yes_no_prompt

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

def main():
   get_name()  
   create_cheers()
   config['first-run'] = 'true'
   with open('config.json', 'w') as f:
      json.dump(config,f)
      
