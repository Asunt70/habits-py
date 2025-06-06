import json
from functions import yes_no_prompt
path_user_habits = 'user/user_habits.json'

def load_user_habits():
    with open(path_user_habits, 'r') as f:
        return json.load(f)
    
def main():
    try: 
        data = load_user_habits()

        create_habit = input("please provide the name of the habit\n==> ")
        if create_habit in data:
            print("this habit already exists")
        else:
            validate = yes_no_prompt(f'"{create_habit}" habit will be added to ur habits, are you sure? (y/n)\n==> ')
            if 'y' in validate:
                data[create_habit] = {"enabled": "true"}
                with open(path_user_habits, 'w') as f:
                    json.dump(data,f, indent=4)
                print(f'"{create_habit}" habit added!')
            else:
                print('ok')
            
    except:
        print("there's no such file called user_habits, probably you didn't run first-setup go to advanced options to do this")
