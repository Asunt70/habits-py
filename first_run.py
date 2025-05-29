import json
#get metadata
with open('metadata.json', 'r') as f:
   data = json.load(f)

#user_preferences_zero = open('user/user-preferences.json', 'w')
#user_preferences = open('user/user-preferences.json', 'a')

#RECCOMENDATION add a prefix to this variable example m_welcome
welcome = data['first-run']['welcome']
ask_name = data['first-run']['ask-name']
ask_cheer = data['first-run']['ask-cheer']
tell_max_phrases = data['first-run']['tell-max-phrases']
ask_cheers = data['first-run']['ask-cheers']
invalid_option = data['errors']['invalid-option']
no_cheers = data['first-run']['no-cheers']
m_confirm_cheers = data['first-run']['confirm-cheers']

#with open(user_preferences) as f:
 #  f.write()

#variables
user_data = {}
name = ""
def yes_no_prompt(prompt):
   while True:
      user_input = input(prompt).strip().lower()
      if user_input in ['y', 'n']:
         return user_input
      else:
         print("please enter 'y' for yes or 'n' for no")

def get_name():
   name = str(input(f'{ask_name}'))
   user_data['name'] = name
   print(f'{name} {welcome}')
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
      ask_cheer_message = yes_no_prompt(f'{ask_cheer}')
      if 'y' in ask_cheer_message:
         print(f'{tell_max_phrases}')
         cheers = str(input(f'{ask_cheers}'))
         cheer_list = cheers.split(", ")
         for cheer in cheer_list:
            print(cheer)
         if confirm_cheers(cheer_list):
            return
         else:
            print("Okay, we will re-run previous commands!")
      else:
         print(f'{no_cheers}')
         return

def main():
   get_name()  
   create_cheers()
   print(user_data)
