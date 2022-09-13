wallet = int(input('How much money do you have? '))

while True:
    user_io_L = input('Add an expense or income record \
with description and amout:\n')
    if user_io_L == '':
        break

    io = int(user_io_L.split()[1])
    wallet += io

    print(f'Now you have {wallet} dollars.\n')

