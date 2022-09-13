import sys

division_line = '=' * 56  #分割線統一設定長度


class Rec:
    """
    A Rec object stores a tuple: (cat in str, description in str, amount in int)
    """
    #spec要求設計: init、getter(並且需要@property來防止亂改亂刪)
    def __init__(self, cat, description, amount): 
        """
        Called to create a Rec object.
        Usage: Rec('meal', 'lunch', -50)
        """
        self._category = cat
        self._description = description
        self._amount = amount

    @property
    def category(self):
        return self._category

    @property
    def description(self):
        return self._description

    @property
    def amount(self):
        return self._amount


class Rec_list:
    """
    A Rec_list object stores all the Rec objects in a list.
    """
    #spec要求設計: init、add、view、delete、find、save
    def __init__(self, file = 'recs.txt'):
        """
        Called to create a Rec_list object.
        Usage: Rec_list()
        """
        self._recs = []
        self._init_wallet = 0
        try:
            with open(file, 'r') as fh:
                try:
                    self._init_wallet = int(fh.readline())
                    for i in fh.readlines():
                        i = i.split()
                        temp = Rec(i[0], i[1], int(i[2]))
                        self._recs.append(temp)

                    print('Welcome back!\n')
                except : 
                    sys.stderr.write('Since the file is partially or entirely broken, all things would be reset. Sorry!\n\n')
                    self._recs = []
                    try:
                        self._init_wallet = int(input('How much money do you have? '))
                        print('')
                    except ValueError:
                        sys.stderr.write('Invalid value. Set to 0 by default.\n\n')
                        self._init_wallet = 0
        except FileNotFoundError as err:
            try:
                self._init_wallet = int(input('How much money do you have? '))
                print('')
            except ValueError:
                sys.stderr.write('Invalid value. Set to 0 by default.\n\n')
                self._init_wallet = 0

        return 


    def add(self, categories): #categories是Cat物件
        """
        Provide to user the service of adding record with cmd"catName itemName io".
        """
        ErrMsg = '\n' + division_line + '\n' \
            + 'The specified category is not in the category list.\n' \
            + 'U Can check the category list by cmd "view categories".\n' \
            + 'Program failed to add a record.\n' \
            + division_line + '\n'

        try:
            input_str = input('Add an expense or income record with category, description, and amount (separate by spaces): \n')
            input_str= input_str.split()
            assert categories.is_cat_valid(input_str[0]), ErrMsg
            temp = Rec(input_str[0], input_str[1], int(input_str[2]))
            self._recs.append(temp)
        except ValueError: 
            sys.stderr.write("Your typed-in number isn't in correct form. Try again!\n")
        except AssertionError as err: 
            sys.stderr.write(str(err))
        except: 
            sys.stderr.write("Can't parse the given str correctly! Please type in your command with the following syntax: 'catName itemName io'(w/o quotes)\n")
        finally:
            print('')

        return


    def view(self):
        """
        This function will print out a formatted table of the records.
        """

        init_str = '{:<25s}{:<25s}{:>6s}'.format('Category', 'Description', 'Amount')

        print("\nHere's your expense and income records: ")
        print(init_str)
        print(division_line)

        total = 0
        for i in self._recs:
            print(f'{i.category:<25s}{i.description:<25s}{i.amount:>+6d}')
            total += i.amount

        print(division_line)
        print(f'Now you have {total + self._init_wallet} dollars.\n')

        return 
        

    def delete(self):
        """
        This function aims to provide to user the service of deleting description-specified record.
        """
        goal = input('Which record do you want to delete? Give me the DESCRIPTION.\n')

        count_matched = 0
        index = []
        for i, v in enumerate(self._recs):
            if(v.description == goal):
                count_matched += 1
                index.append(i)

        if (count_matched == 0):#有防呆
            print(f"There's no matched record with description '{goal}'. Deletion failed.\n")
        elif (count_matched == 1):
            print(f"There's {count_matched} matched record with description '{goal}':")
            print(f"{goal} {self._recs[index[0]].amount:+d}")
            print("Deletion completed!\n")
            del(self._recs[index[0]])

        else:
            print(f"There're {count_matched} matched records with description '{goal}':")
            for i, v in enumerate(index, 1):
                print(f"{i:>3d}: {goal} {self._recs[v].amount:<10d}")
            goal_index = int(input("Which one do you want do delete? No. "))
            if 0 < goal_index <= len(index):
                print("Deletion completed!\n")
                del(self._recs[index[goal_index - 1]])
            else:#有防呆
                print('Wrong index! Please try again.\n')

        return 


    def find(self, categories):
        """
        This function prints a formatted table that lists out all the records under the category specified by user.
        """
        ErrMsg = '\n' + division_line + '\n' \
        + 'The specified category is not in the category list.\n' \
        + 'U Can check the category list by cmd "view categories".\n' \
        + division_line + '\n'


        goal_subcat_to_be_root_to_find = input() #先叫使用者輸入想找的cat

        try:
            assert categories.is_cat_valid(goal_subcat_to_be_root_to_find), ErrMsg #先確定使用者輸入的cat是可用的，如果可用執行else，如果不可用執行AssertionError就回去main function的while-loop裡面
        except AssertionError as err:
            sys.stderr.write(str(err))
            return
        else:#已確定使用者輸入的cat是可用的
            list_of_sub_cats = categories.find_subcat(goal_subcat_to_be_root_to_find)#先把所有下層級的category名字全部統整到一個list(名為list_of_sub_cats)裡面

            init_str = '{:<25s}{:<25s}{:>6s}'.format('Category', 'Description', 'Amount')

            total_amount = 0
            front_division_line_printed = back_division_line_printed = False
            for i in self._recs: #掃過recs裡的每一項
                if i.category in list_of_sub_cats: #如果這項目的cat是我們已經羅列的要印出的cat之一，我就印
                    if not front_division_line_printed:#這個if只是在做如果是第一次列印的初始格式而已
                        print(f"Here's you expense and income records under category \"{goal_subcat_to_be_root_to_find}\":")
                        print(init_str)
                        print(division_line)
                    
                        front_division_line_printed = True
                    print(f'{i.category:<25s}{i.description:<25s}{i.amount:>+6d}')
                    total_amount += i.amount

            #離開for迴圈後，代表所有項目都已經印完了，接下來印收尾動作
            if not back_division_line_printed and front_division_line_printed: #如果我至少有印一個項目，那就要做對稱性的收尾格式
                print(division_line)
                print(f"The total amount above is {total_amount}.\n")
                back_division_line_printed = True
            elif not back_division_line_printed and not front_division_line_printed: #如果我一個項目都沒印到，那就跟使用者說他要的東西什麼都沒有
                print(f"Ooooops! There's nothing under the specified category \"{goal_subcat_to_be_root_to_find}\"! Sorry!\n")
            return
        return


    def save(self, file = 'recs.txt'):
        """
        Save the records from memory to disk upon the program exiting, in order that next time the program would keep the recs when being opened.
        """
        with open(file, 'w') as fh:
            fh.write(str(self._init_wallet) + '\n')
            L = [(i.category+' '+i.description+' '+str(i.amount)+'\n') for i in self._recs]
            fh.writelines(L)

        return

class Cat:
    """
    Stores a nested list with categories and their subcategories (if any) inside.
    """
    #init、view、is_cat_valid、find_subcat、flatten
    def __init__(self):
        """
        Initialises a nested list object in Cat obj.
        """
        self._cat_list = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]


    def view(self, level = 0):
        """
        View categories and subcategories that are represented in schemed indentation form.
        """
        def inner_view(L, level = 0): 
            if type(L) == str:
                arrow = '-' * level + '>'
                print(' ' * 6 * level + arrow + L)

            else:
                if level == 0:
                    print('\n' + division_line)
                for item in L:
                    inner_view(item, level + 1)
                if level == 0:
                    print(division_line + '\n')

            return

        return inner_view(self._cat_list)


    def is_cat_valid(self, cat_name):
        """
        Checks if name of the to-be-searched category is in the list of Cat obj.
        """
        def inner_is_cat_valid(L, cat_name):
            if type(L) == str:
                return L == cat_name

            else:
                for item in L:
                    cat_name_found = inner_is_cat_valid(item, cat_name) 
                    if cat_name_found == True: 
                        return True
                return False

        return inner_is_cat_valid(self._cat_list, cat_name)


    def find_subcat(self, goal):
        """
        Returns a list containing all atoms in a subcategory of a category.
        """
        def inner_find_subcat(cat_list, goal): 
            if type(cat_list) == str:
                return goal if cat_list == goal else None

            else:
                temp = []
                for i in range(0, len(cat_list)): 
                    item = cat_list[i]
                    result = inner_find_subcat(item, goal) 
                    if result == goal: 
                        temp.append(goal)
                        if i + 1 < len(cat_list) and type(cat_list[i + 1]) == list: 
                            atoms_in_subcat = [i for i in self.flatten_generator(cat_list[i + 1])]
                            temp[1:] = atoms_in_subcat[:] 
                        break 
                    elif type(result) == list and result: 
                        return result
                return temp


        return inner_find_subcat(self._cat_list, goal)

    def flatten_generator(self, nested_list):
        """
        Transforms a nested list into a plane list.
        """
        if type(nested_list) == list:
            for child in nested_list:
                for atom in self.flatten_generator(child):
                    yield atom

        else:
            yield nested_list



categories = Cat()
recs = Rec_list()

while True:
    cmd = input('What do you want to do (add/view/delete/view categories/find/exit)? ')
    if cmd[:len('exit')] == 'exit':
        recs.save()
        break
    elif cmd[:len('add')] == 'add': #有防呆
        recs.add(categories)
    elif cmd[:len('delete')] == 'delete':
        recs.delete()
    elif cmd[:len('view categories')] == 'view categories': 
        categories.view()
    elif cmd[:len('view')] == 'view':
        recs.view()
    elif cmd[:len('find')] == 'find':
        recs.find(categories)
    else:
        sys.stderr.write("I don't know what you mean. Please try again.\n\n")
