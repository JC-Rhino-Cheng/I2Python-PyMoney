import sys

def initialise():
    wallet = 0
    init_wallet = 0
    recs = []

    try:
        with open('recs.txt', 'r') as fh:
            try:
                wallet = int(fh.readline())
                init_wallet = wallet
                for i in fh.readlines():
                    recs.append((i.split()[0], int(i.split()[1])))
                    wallet += int(i.split()[1])

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


def view(wallet, recs):
        init_str = '{:<25s}{:>6s}'.format('Description', 'Amount')
        division_line = '=' * 31

        print("Here's your expense and income records: ")
        print(init_str)
        print(division_line)
        for i in recs:
            print(f'{i[0]:<25s}{i[1]:>+6d}')
        print(division_line)
        print(f'Now you have {wallet} dollars.\n')

        return 


def delete(recs):
        goal = input('Which record do you want to delete? Give me the title.\n')

        count_matched = 0
        index = []
        deleted = 0
        for i, v in enumerate(recs):
            if(v[0] == goal):
                count_matched += 1
                index.append(i)

        if (count_matched == 0):#有防呆
            print(f"There's no matched record with title '{goal}'. Deletion failed.\n")
        elif (count_matched == 1):
            print(f"There's {count_matched} matched record with title '{goal}':")
            print(f"{goal} {recs[index[0]][1]:+d}")
            print("Deletion completed!\n")
            deleted = recs[index[0]][1]
            del(recs[index[0]])

        else:
            print(f"There're {count_matched} matched records with title '{goal}':")
            for i, v in enumerate(index, 1):
                print(f"{i:>3d}: {goal} {recs[v][1]:<10d}")
            goal_index = int(input("Which one do you want do delete? No. "))
            if goal_index <= len(index):
                print("Deletion completed!\n")
                deleted = recs[index[goal_index - 1]][1]
                del(recs[index[goal_index - 1]])
            else:#有防呆
                print('Wrong index! Please try again.\n')

        return deleted


def add(recs):
    io = input('Add an expense or income record with description and amount: \n')
    ret_val = 0
    try:
        recs += [(io.split()[0], int(io.split()[1]))]
        ret_val = int(io.split()[1])
    except ValueError:
        print("Your typed-in number isn't in correct form. Try again!\n")
        ret_val = 0
    except: 
        print("Can't parse the given str correctly! Please type in your command with the following syntax: 'itemName io'(w/o quotes)\n")
        ret_val = 0
    finally:
        print('')
        return ret_val

    


def save(init_wallet, recs):
    with open('recs.txt', 'w') as fh:
        fh.write(str(init_wallet) + '\n')
        L = [(i[0]+' '+str(i[1])+'\n') for i in recs]
        fh.writelines(L)

    return
############################
############################
############################
############################
############################
init_wallet, wallet, recs = initialise()

while True:
    cmd = input('What do you want to do (add/view/delete/exit)? ')
    if cmd[:len('exit')] == 'exit':
        save(init_wallet, recs)
        break
    elif cmd[:len('add')] == 'add': #有防呆
        wallet += add(recs) #我覺得不用recs = add(....)，因為本身Py的傳送就是call by reference.....，根本不用多此一舉
    elif cmd[:len('view')] == 'view':
        view(wallet, recs)
    elif cmd[:len('delete')] == 'delete':
        wallet -= delete(recs)
    else:
        sys.stderr.write("I don't know what you mean. Please try again.\n\n")#有防呆