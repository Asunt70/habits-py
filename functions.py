def yes_no_prompt(prompt):
   while True:
      user_input = input(prompt).strip().lower()
      if user_input in ['y', 'n']:
         return user_input
      else:
         print("please enter 'y' for yes or 'n' for no")

def int_input(prompt):
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except:
            print('please enter a number')

def multi_int_input(prompt):
    while True:
        user_input_str = input(prompt).strip()

        if not user_input_str:
            print("Input cannot be empty. Please enter numbers separated by spaces.")
            continue

        user_input_list = user_input_str.split(" ")
        valid_integers = []
        all_valid = True

        for i in user_input_list:
            if not i:
                continue
            try:
                valid_integers.append(int(i))
            except:
                print('please enter only numbers')
                all_valid = False
                break

        if all_valid == True:
            return valid_integers
