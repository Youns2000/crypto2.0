   # def clean_screen():
#         if os.name == 'nt':
#             _ = os.system('cls')
#         else:
#             _ = os.system('clear')
   
   # if actual_curr == 'Comedy':
    #     with st.container():
    #         st.write('You selected comedy.')
    # else:
    #     with st.container():
    #         st.write("You didn't select comedy.")

    # acc = account.Account()

    # while True:
    #     for c in acc.currencies:
    #         print(c.name + " : " + str(c.fake_money))
    #     print("USDT : " + str(acc.usdt_var.fake_money))
    #     print()
    #     print("1.ADD A CURRENCY")
    #     print("2.BUY")
    #     print("3.SELL")
    #     print("4.EXIT")
    #     choix = input('Make you choice: ')
    #     if choix == "1":
    #             curr = input('Currency: ')
    #             acc.add_curr(curr)
    #             acc.close()
    #     elif choix == "2":
    #             curr = input('Currency: ')
    #             value = input('Buy Value: ')
    #             print(float(value))
    #             acc.buy_curr(curr, float(value))
    #             acc.close()
    #     elif choix == "3":
    #             curr = input('Currency: ')
    #             percent = input('Sell Percent: ')
    #             acc.sell_curr(curr, float(percent))
    #             acc.close()
    #     elif choix == "4":
    #             acc.close()
    #             exit()
    #     else:
    #             print("err")