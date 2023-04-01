from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=81)

#1. Go to: https://zeldabank.flyewzz.repl.co
#2. Press: REGISTER
#3. In the Username field, enter: F
#4. In the Password field, enter: 1
#5. In the Confirm Password: enter: 1
#6. In the Currency: choose USD
#7. In the Balance: enter 1000000
#8. Press: REGISTER
#(create second new account, repeat actions from #1 to #8)
#12. Press: REGISTER
#13. In the Username field, enter: G
#14. In the Password field, enter: 1
#15. In the Confirm Password: enter: 1
#16. In the Currency: choose EUR
#17. In the Balance: enter 1000000
#18. Press: REGISTER
#19. In the Username field, enter: G
#20. In the Password field, enter: 1
#21. Press: G
#22. Take a look at Transfer Money, in the Recipient choose F, enter: 21322,32
#23. Press: Transfer
#24. Press: LOGOUT
#25. Press: LOGIN
#26. In the Username field, enter: F
#27. In the Password field, enter: 1
#28. Press: login
#29. Press: F
# Look at the Current Balance. The amount in the account is incorrect: On F account you see 1003838.0176 USD ->
# 1,18 * 21322,32 = 25 160,3376 = 1025160,34
# Expected amount on F's account: 1025160,34 USD
# Actual amount on F's account: 1003838.0176 USD




#* Go to: https://zeldabank.flyewzz.repl.co
#* Press: LOGIN
#* In the Username field, enter: Petya
#* In the Password field, enter: 1234
#* Press: PETYA
#* Look at the Currency Balance, Balance
# Expected amount on Petya's account: 38987.00 USD
# Actual amount on Petya's account: 38987.000 USD

######30.03.2023######
#* Go to: https://zeldabank.flyewzz.repl.co
#* Press: LOGIN
#* In the Username field, enter: Vasya
#* In the Password field, enter: 1234
# Press: Login
#* Press: VASYA
#* Look at the Transfer Money, choose Recipient: Petya, Amount:7,88
# Press: Transfer 
#* Press: LOGOUT
#* In the Username field, enter: Petya
#* In the Password field, enter: 1234
# Pres: Login
#* Press: PETYA
# Expected amount on Petya's account: 20000 -> 20000.11 USD
# Actual amount on Petya's account: 20000,09456 USD

#* Press: LOGIN
#* In the Username field, enter: A
#* In the Password field, enter: 1
#* Press: A
#* Look at the Current Balance amd remember Balance: 8892.12
#* Press: LOGOUT
#* Press: LOGIN
#* In the Username field, enter: Vasya
#* In the Password field, enter: 1234
#* Press: VASYA
#* Look at the Current Balance: 7892.12 
#* In Transfer Money select A, amount 1000
#* Press: TRANSFER
#* Press: LOGOUT
#* Log in to account A and look at A's balance
# Expected amount on A's account: 9892,12 RUB
# Actual amount on A's account: 7892.12 RUB

#* Press: REGISTER
#* In the Username field, enter: D
#* In the Password field, enter: 1
#* In the Confirm Password, enter:12
#* In the Currency: choose RUB
#* In the Balance, enter: 100000
#* Press: REGISTER 
# Expected result: Password mismatch
# Actual result: Mismatch of passwords and inability to choose currency
