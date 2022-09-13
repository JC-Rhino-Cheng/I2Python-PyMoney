wallet = int(input('How much money do you have? '))

while True:
    user_io_L = input('Add some expense or income records \
with description and amount:\ndesc1 amt1, desc2 amt2, desc3 amt3, ...\n')
    if user_io_L == '':
        break

    L_of_str = user_io_L.split(', ') #原本是字串，依據", "來切割成list of str，list中的每個元素都長這樣(單純str): 'breakfast -50'
    L_final = [(t.split()[0], int(t.split()[1])) for t in L_of_str]

    print("Here's your expense and income records:")
    for i in L_final:
        print(f'{i[0]:s} {i[1]:d}')
        wallet += i[1]

    print(f'Now you have {wallet} dollars.\n')

