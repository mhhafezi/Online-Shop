import menu
import user
import my_log
import product
import sys


def main():
    menu.print_menu_register_login()
    username_list = menu.file_path_username_list()
    choice = 0
    while choice != "4":
        choice = input("Please enter your choice:")
        if choice == "1":
            username = input("Please enter your Username for register:\n")
            if not username:
                main()
            if username in username_list:
                if username == "admin":
                    print('You are not Admin. an admin is exist.')
                    my_log.logger.warning('Someone tried to register as admin.')
                    main()
                else:
                    print(f"Username {username.capitalize()} is exist in system. please enter another username.")
                    main()
            else:
                password = input(f"{username.capitalize()} please enter your password for register:\n")
                if username == "admin" and password == '1':  # for secure admin entry
                    user.User.register(username, password)  # Only one admin is allowed to register and login.
                    my_log.logger.info('Admin created successfully.')
                    main()
                elif username == "admin" and password != 1:
                    print('You are not Admin. an admin has special password.')
                    my_log.logger.warning('Someone tried to register as an admin with an insecure password.')
                    main()
                else:
                    user.User.register(username, password)
                    main()

        elif choice == "2":
            username = input('Please enter your name for login:')
            if not username:
                main()
            if username == 'admin':
                user.User.login(username)
            else:
                if username in username_list:
                    table = product.Product.show_product(username)
                    print(table.table)
                    print('If you want to buy should enter password.')
                    user.User.login(username)
                else:
                    print("Your not registered. please first register then login, or login with True username.")
                    main()

        elif choice == "3":
            print("\n******  Goodbye ******")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")


main()
