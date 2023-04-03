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

#02.04.2023 
#I created 8 accounts (A,B,C,D,E,F,G,H)
#Two of them are administrators (A and E)
#I checked the ability to make transfers to blocked and unblocked users, I checked if the transfer scale is correct and if you can send more money than we have on the account, whether you can send negative amounts, I checked if any error pops up when registering a new user (different passwords, same names)

#* Go to: https://zeldabank.flyewzz.repl.co/login
#* In the Username field, enter: B
#* In the Password field, enter: 1
# Press: Login
#* Press: B
#* Look at the Transfer Money, choose Recipient: A, Amount: 7,88
# Press: Transfer 
#* Press: LOGOUT
#* In the Username field, enter: A
#* In the Password field, enter: 1
# Pres: Login
#* Press: A(A) (in the header of site)
# Expected result: It is not possible to make a transfer to a blocked account
# Actual result: The transfer was successful even though the user is blocked

#* Go to: https://zeldabank.flyewzz.repl.co/login
#* In the Username field, enter: D
#* In the Password field, enter: 1
# Press: Login
#* Press: D
#* Look at the Transfer Money, choose Recipient: C, Amount: 10000
# Press: Transfer 
# Expected result: You cannot send money from a blocked account
# Actual result: The transfer was sent without problems

#* Go to: https://zeldabank.flyewzz.repl.co/backoffice (before log out of the account you are logged in to)
# Expected result: You will be redirected to the login page.
# Actual result: We see the screamed page with code.

#* Go to: https://zeldabank.flyewzz.repl.co/login
#* Press: LOGIN
#* In the Username field, enter: E
#* In the Password field, enter: 1
# Press: Login
#* Press: E
#* Look at the Transfer Money, choose Recipient: F, Amount:10,88
# Press: Transfer 
#* Press: LOGOUT
#* In the Username field, enter: A
#* In the Password field, enter: 1
# Pres: Login
#* Press: A(A)
# Expected result: Visibility of two digits after the decimal point in account E and F
# Actual result: From the backoffice, see the sum after the decimal points of account E and F (E = 1000098.920 EUR, F = 1000000000000000894.0096 RUB)

#* Go to: https://zeldabank.flyewzz.repl.co/login
#* Press: LOGIN
#* In the Username field, enter: C
#* In the Password field, enter: 1
# Press: Login
#* Press: C
#* Look at the Transaction History. 
# Expected result: We should see individual information about the money sent.
# Actual result: We see the information about the money sent repeated twice.

#* Go to: https://zeldabank.flyewzz.repl.co
#* Press: REGISTER
#* In the Username field, enter: G
#* In the Password field, enter: 1
#* In the Confirm Password field, enter: 1
#* In place of currency, select RUB
#* In the Balance, enter: -10,88
# Press: REGISTER
#* In the Username field, enter: G
#* In the Password field, enter: 1
# Pres: Login
#* Press: G
# Actual result: An account with a negative balance has been created.
# Expected result: You cannot create an account with negative balance.

#* Go to: https://zeldabank.flyewzz.repl.co/login
#* Press: LOGIN
#* In the Username field, enter: B
#* In the Password field, enter: 1
#* Press: Login
#* Change a website address (URI) manually (https://zeldabank.flyewzz.repl.co) add backoffice (https://zeldabank.flyewzz.repl.co/backoffice) press: enter
# Expected result: 403 Forbidden (for standard user)
# Actual result: We have access to the back office and can block users from there.