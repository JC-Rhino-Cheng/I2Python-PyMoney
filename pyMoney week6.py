wallet = int(input('How much money do you have? '))

recs = []

while True:
    cmd = input('What do you want to do (add/view/delete/exit)? ')
    if cmd[:len('exit')] == 'exit':
        break

    elif cmd[:len('add')] == 'add': #有防呆
        io = input('Add an expense or income record with description and amount: \n')
        recs += [(io.split()[0], int(io.split()[1]))]
        wallet += int(io.split()[1])
        print('')

    elif cmd[:len('view')] == 'view':
        init_str = '{:<25s}{:>6s}'.format('Description', 'Amount')
        division_line = '=' * 31

        print("Here's your expense and income records: ")
        print(init_str)
        print(division_line)
        for i in recs:
            print(f'{i[0]:<25s}{i[1]:>+6d}')
        print(division_line)
        print(f'Now you have {wallet} dollars.\n')

    elif cmd[:len('delete')] == 'delete':
        goal = input('Which record do you want to delete?\n')

        count_matched = 0
        index = []
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
            wallet -= recs[index[0]][1]
            del(recs[index[0]])

        else:
            print(f"There're {count_matched} matched records with title '{goal}':")
            for i, v in enumerate(index, 1):
                print(f"{i:>3d}: {goal} {recs[v][1]:<10d}")
            goal_index = int(input("Which one do you want do delete? No. "))
            if goal_index <= len(index):
                print("Deletion completed!\n")
                wallet -= recs[index[goal_index - 1]][1]
                del(recs[index[goal_index - 1]])
            else:#有防呆
                print('Wrong index! Please try again.\n')
    else:
        print("I don't know what you mean. Please try again.\n")#有防呆