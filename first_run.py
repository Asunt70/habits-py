import json
with open('metadata.json', 'r') as f:
   data = json.load(f)

#reccomendation add a prefix to this variable example m_welcome
welcome = data['first-run']['welcome']
ask_name = data['first-run']['ask-name']
ask_cheer = data['first-run']['ask-cheer']
tell_max_phrases = data['first-run']['tell-max-phrases']
ask_cheers = data['first-run']['ask-cheers']
invalid_option = data['errors']['invalid-option']
def user_data():
   name = str(input(f'{ask_name}'))
   print(f'{name} {welcome}')
   print("--------------")

def strip_list(items):
    for i in items:
        return i.strip()

def main():
   user_data()
   #cheer message
   trigger = True
   while trigger is True:
       ask_cheer_message = input(f'{ask_cheer}')
       try:
           ask_cheer_message = int(ask_cheer_message)
           trigger = False
       except:
           print(f'{invalid_option}')
   if ask_cheer_message == 1:
       print(f'{tell_max_phrases}')
       get_cheers =  str(input(f'{ask_cheers}'))
       if len(get_cheers) <= 20:
        strip_list(get_cheers)
       else:
        print("")
               
           
    

