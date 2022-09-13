import sys

def init_cat(): #定義categories分類
    return ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]


categories = init_cat() #先初始化categories分類
division_line = '=' * 56  #分割線統一設定長度


def initialise(): #這個跟week8基本一樣，只是因為檔案的欄位變成tuple(cat, des, amount)，相較week8，最左邊多了一個cat的字串，所以在try...with...try裡面的for的讀取的部分[0]、[1]、[2]有調整
    """
    By default, the program will carry out this function to read-in the saved records from your disk into memory.
    If carried out normally, it will say: "Welcome back!" and you can successfully treat this time's use as usual.
    If the records in disk go wrong accidentally, it will reset the 記帳本 to default, which is wallet(0) and recs(empty).
    """
    wallet = 0
    init_wallet = 0
    recs = []

    try:
        with open('recs.txt', 'r') as fh:
            try:
                wallet = int(fh.readline())
                init_wallet = wallet
                for i in fh.readlines():
                    recs.append((i.split()[0], i.split()[1], int(i.split()[2])))
                    wallet += int(i.split()[2])

                print('Welcome back!\n')
            except : 
                print('Since the file is partially or entirely broken, all things would be reset. Sorry!')
                recs = []
                try:
                    wallet = int(input('How much money do you have? '))
                    print('')
                except ValueError:
                    print('Invalid value. Set to 0 by default.\n')
                    wallet = 0
                init_wallet = wallet
    except FileNotFoundError as err:
        #file not found or not usable
        # print(str(err)) # It can be an err, but it can also be OK if the program is used the first time.
        try:
            wallet = int(input('How much money do you have? '))
            print('')

        except ValueError:
            print('Invalid value. Set to 0 by default.\n')
            wallet = 0
        init_wallet = wallet


    
    finally:
        return (init_wallet, wallet, recs)

    return #這個return完全是為了讓python能夠知道這個function在這邊一定會結束，相當於把這個scope的範圍在沒有執行時也寫得很清楚的意思。因為py雖然在執行時一定可以到finally那邊執行return，但是文字編輯器抓不到這個function的finally return，會導致文字編輯器無法正確收合這個function的code。


def view(wallet, recs): #這個跟week8基本一樣，只是相應地多出了Category欄位，然後for裡面的i[0]、i[1]、i[2]也相應調整
        """
        This function will print out a formatted table of the records.
        """

        init_str = '{:<25s}{:<25s}{:>6s}'.format('Category', 'Description', 'Amount')

        print("\nHere's your expense and income records: ")
        print(init_str)
        print(division_line)
        for i in recs:
            print(f'{i[0]:<25s}{i[1]:<25s}{i[2]:>+6d}')
        print(division_line)
        print(f'Now you have {wallet} dollars.\n')

        return 


def delete(recs): #這個跟week8基本一樣，只不過(1)emumerate時的v[xx]==goal從v[0]改成v[1]。(2)elif (count_matched == 1)裡面的{recs[index[0]][xx]:+d}和deleted = recs[index[0]][2]從[1]改成[2]。(3)else裡面的index的部分也都相應調整。(4)修正如果使用者錯誤地輸入了"0"作為欲刪除的編號的話的錯誤執行。
        """
        This function aims to provide to user the service of deleting description-specified record.
        """
        goal = input('Which record do you want to delete? Give me the DESCRIPTION.\n')

        count_matched = 0
        index = []
        deleted = 0
        for i, v in enumerate(recs):
            if(v[1] == goal):
                count_matched += 1
                index.append(i)

        if (count_matched == 0):#有防呆
            print(f"There's no matched record with description '{goal}'. Deletion failed.\n")
        elif (count_matched == 1):
            print(f"There's {count_matched} matched record with description '{goal}':")
            print(f"{goal} {recs[index[0]][2]:+d}")
            print("Deletion completed!\n")
            deleted = recs[index[0]][2]
            del(recs[index[0]])

        else:
            print(f"There're {count_matched} matched records with description '{goal}':")
            for i, v in enumerate(index, 1):
                print(f"{i:>3d}: {goal} {recs[v][2]:<10d}")
            goal_index = int(input("Which one do you want do delete? No. "))
            if 0 < goal_index <= len(index):
                print("Deletion completed!\n")
                deleted = recs[index[goal_index - 1]][2]
                del(recs[index[goal_index - 1]])
            else:#有防呆
                print('Wrong index! Please try again.\n')

        return deleted


def add(recs): #這個跟week8基本一樣，但因為使用者會要多打想要的category，所以會在try裡面先使用assert偵測該cat是否可用，而assert需要跳出的訊息定義在try前面的ErrMsg。至於recs，就和前面的幾個function做一樣的調整。
    """
    Provide to user the service of adding record with cmd"catName itemName io".
    """

    io = input('Add an expense or income record with category, description, and amount (separate by spaces): \n')
    ret_val = 0

    ErrMsg = '\n' + division_line + '\n' \
        + 'The specified category is not in the category list.\n' \
        + 'U Can check the category list by cmd "view categories".\n' \
        + 'Program failed to add a record.\n' \
        + division_line
    try:
        input_splitted = io.split()
        assert is_category_valid(categories, input_splitted[0]), ErrMsg
        recs += [(input_splitted[0], input_splitted[1], int(input_splitted[2]))]
        ret_val = int(input_splitted[2])
    except ValueError: #split可能出錯，歸類到這裡
        print("Your typed-in number isn't in correct form. Try again!\n")
        ret_val = 0
    except AssertionError as err: #使用者輸入的category不存在
        print(str(err))
        ret_val = 0
    except: 
        print("Can't parse the given str correctly! Please type in your command with the following syntax: 'catName itemName io'(w/o quotes)\n")
        ret_val = 0
    finally:
        print('')
        return ret_val

    return


def save(init_wallet, recs): #這個跟week8基本一樣，就是L=[...]的部分index一樣做調整
    """
    Save the records from memory to disk upon the program exiting, in order that next time the program would keep the recs when being opened.
    """

    with open('recs.txt', 'w') as fh:
        fh.write(str(init_wallet) + '\n')
        L = [(i[0]+' '+i[1]+' '+str(i[2])+'\n') for i in recs]
        fh.writelines(L)

    return


def view_categories(L, level = 0): #就是用大綱的方式印出cat和subcat之間的關係。兩個if level == 0:用來格式化。而根據層次的不同，每個項目前面的項目編號(a.k.a.箭頭)的長度也不同
    ##['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]##
    if type(L) == str:
        arrow = '-' * level + '>'
        print(' ' * 6 * level + arrow + L)

    else:
        if level == 0:
            print('\n' + division_line)
        for item in L:
            view_categories(item, level + 1)
        if level == 0:
            print(division_line + '\n')

    return


def is_category_valid(L, cat_name):
    ##['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]##
    if type(L) == str:
        return L == cat_name

    else:
        for item in L:
            cat_name_found = is_category_valid(item, cat_name) #針對list中的每個item呼叫，如果item是list就會開啟新一輪的遞迴，如果item是str，就回傳比對結果是否找到。
            if cat_name_found == True: #根據上一行，如果在這層(L是str，且L==cat_name)subcat找到，就要一路每一層全部return True回去
                return True
        return False #如果不寫這行也可以，這樣上面的cat_name_found = is_category_valid(item, cat_name)就會接收到None，這樣不會導致if cat_name_found == True:出現bug


def find_sub_cat(categories, goal): #需要回傳一個flatten list
    ##['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]##
    if type(categories) == str:
        return goal if categories == goal else None

    else:
        temp = []
        for i in range(0, len(categories)): #為了直接抓取goal的subcat(subcat如果存在，會剛好在goal的右邊第一個人)，所以採用編號法的for
            item = categories[i]
            result = find_sub_cat(item, goal) #item如果是str，那result會是goal字串或者None。item如果是list，那就會開啟新一輪遞迴，查找該list中有沒有str。
            if result == goal: #item如果是str且有找到，就把item先弄進temp裡面，然後再針對他右邊index的那個人看看如果是list，就把所有內容flatten並加到temp裡面
                temp.append(goal)
                if i + 1 < len(categories) and type(categories[i + 1]) == list: #如果item右邊的人是list，就把這個list裡面所有層層疊疊的str全部弄在list的第一層
                    temp[1:] = flatten(categories[i + 1])[:] #針對categories[i + 1]把所有層層疊疊的str全部弄在list的第一層，所以flatten(...)回傳是一個list。針對回傳回來的這個list，把所有內容shallow copy給temp的從index1開始的位置。
                break #不管item右邊有沒有subcat，反正我就是找到了，代表我的temp已經完成了，他要找的list我已經全部做好了，所以break。這樣就會離開for迴圈，到return temp，就會把找到的list回傳給result = find_sub_cat(item, goal)。
            elif type(result) == list and result: #如果我已經找到了，而且找到的不是第一步的str而已，而是已經把str和後面可能有的subcat都找到了，那這裡的result就會是個list。
                #!!!如果result不是空的，代表確實找到所有我要的東西了，所以我就一路return這個list回去。
                #為何需要判斷result非空，是因為result有可能是list而且空的。假設你要找transportation，在這之前會先把[meal, snack, drink]每個項目都遞迴過一遍，
                #當drink也return None時，[meal, s, drink]這層的list的!!!for i in range(0, len(categories))!!!會跑完，到下面return temp的時候，temp會是空字串!!!這樣的話，在找transportation前就會result=[]一路return回去了，這樣不對
                #所以如果result是空字串，代表的是前面那個list都我沒有找到第一步的str，我連第一步的str都沒找到!那當然這需要把for進行下去，不可以結束迴圈，所以就不return，就可以正確把for進行下去了
                return result
        return temp

    return #這個return完全是為了讓python能夠知道這個function在這邊一定會結束，相當於把這個scope的範圍在沒有執行時也寫得很清楚的意思。因為py雖然在執行時一定可以到finally那邊執行return，但是文字編輯器抓不到這個function的finally return，會導致文字編輯器無法正確收合這個function的code。


def flatten(L):
    if type(L) == str:
        return L

    else:
        temp = []
        for item in L:
            temp.append(flatten(item))
        return temp


def find(recs, categories):
    ErrMsg = '\n' + division_line + '\n' \
        + 'The specified category is not in the category list.\n' \
        + 'U Can check the category list by cmd "view categories".\n' \
        + division_line + '\n'


    goal_subcat_to_be_root_to_find = input() #先叫使用者輸入想找的cat

    try:
        assert is_category_valid(categories, goal_subcat_to_be_root_to_find), ErrMsg #先確定使用者輸入的cat是可用的，如果可用執行else，如果不可用執行AssertionError就回去main function的while-loop裡面
    except AssertionError as err:
        print(str(err))
        return
    else:#已確定使用者輸入的cat是可用的
        list_of_sub_cats = find_sub_cat(categories, goal_subcat_to_be_root_to_find)#先把所有下層級的category名字全部統整到一個list(名為list_of_sub_cats)裡面

        init_str = '{:<25s}{:<25s}{:>6s}'.format('Category', 'Description', 'Amount')

        total_amount = 0
        front_division_line_printed = back_division_line_printed = False
        for i in recs: #掃過recs裡的每一項
            if i[0] in list_of_sub_cats: #如果這項目的cat是我們已經羅列的要印出的cat之一，我就印
                if not front_division_line_printed:#這個if只是在做如果是第一次列印的初始格式而已
                    print(f"Here's you expense and income records under category \"{goal_subcat_to_be_root_to_find}\":")
                    print(init_str)
                    print(division_line)
                    
                    front_division_line_printed = True
                print(f'{i[0]:<25s}{i[1]:<25s}{i[2]:>+6d}')
                total_amount += i[2]

        #離開for迴圈後，代表所有項目都已經印完了，接下來印收尾動作
        if not back_division_line_printed and front_division_line_printed: #如果我至少有印一個項目，那就要做對稱性的收尾格式
            print(division_line)
            print(f"The total amount above is {total_amount}.\n")
            back_division_line_printed = True
        elif not back_division_line_printed and not front_division_line_printed: #如果我一個項目都沒印到，那就跟使用者說他要的東西什麼都沒有
            print(f"Ooooops! There's nothing under the specified category \"{goal_subcat_to_be_root_to_find}\"! Sorry!\n")
        return
    return #這個return完全是為了讓python能夠知道這個function在這邊一定會結束，相當於把這個scope的範圍在沒有執行時也寫得很清楚的意思。因為py雖然在執行時一定可以到finally那邊執行return，但是文字編輯器抓不到這個function的finally return，會導致文字編輯器無法正確收合這個function的code








############################
############################
############################
############################
############################
init_wallet, wallet, recs = initialise()

while True:
    cmd = input('What do you want to do (add/view/delete/view categories/find/exit)? ')
    if cmd[:len('exit')] == 'exit':
        save(init_wallet, recs)
        break
    elif cmd[:len('add')] == 'add': #有防呆
        wallet += add(recs) #我覺得不用recs = add(....)，因為本身Py的傳送就是call by reference.....，根本不用多此一舉
    elif cmd[:len('delete')] == 'delete':
        wallet -= delete(recs)
    elif cmd[:len('view categories')] == 'view categories': #view categories調整到view前面，不然view categories會被cmd[:len('view')]的方法歸類到view裡面，就不是正確分流
        view_categories(categories)
    elif cmd[:len('view')] == 'view':
        view(wallet, recs)
    elif cmd[:len('find')] == 'find':
        find(recs, categories)
    else:
        sys.stderr.write("I don't know what you mean. Please try again.\n\n")#有防呆


#後記: 後來才發現原來助教有給code......find_sub_categories和flatten都有給......不過沒差，反正很簡單我隨便寫隨便對
