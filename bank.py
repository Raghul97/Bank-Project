import sqlite3


class Account:

    def __init__(self, acc_holder, balance):
        self.acc_holder = acc_holder
        self.balance = balance

    def __str__(self):
        return f'{self.acc_holder} has bank balance of {self.balance}'

    def deposit(self, amount):
        self.balance = self.balance + amount
        print(' Amount successfully deposited')
        return self.balance

    def withdraw(self, amount):
        if amount < self.balance:
            self.balance = self.balance - amount
            print(' Amount successfully withdrawn')
        else:
            print(' Insufficient Balance ')
        return self.balance


def torun():
    global process
    ask = input('More process should be done? (Y or N)  ')
    if ask.upper() == 'Y':
        process = True
    else:
        process = False


conn = sqlite3.connect('bank.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS ACCOUNT
    (id INTEGER PRIMARY KEY, Acc_HOLDER TEXT UNIQUE,BALANCE INTEGER)''')

process = True
while process:
    name = input("Enter the Account holder name: ").upper()
    method = input(' to Deposit or Withdraw: (D or W) ')
    cur.execute('SELECT BALANCE FROM ACCOUNT WHERE Acc_HOLDER=? LIMIT 1', (name, ))
    try:
        row = cur.fetchone()
        balance = row[0]
    except:
        cur.execute('INSERT OR IGNORE INTO ACCOUNT (Acc_HOLDER, BALANCE) VALUES ( ?, 0 )', (name, ))
        balance = 0
    if method.upper() == 'D':
        try:
            money = int(input(' Enter the amount to be deposited: '))
        except:
            print('Enter a valid number to deposit: ')
            break
        instant = Account(name, balance)
        updbalance = instant.deposit(money)
        cur.execute('UPDATE ACCOUNT SET BALANCE=? WHERE Acc_HOLDER=?', (updbalance, name))
        conn.commit()
    elif method.upper() == 'W':
        try:
            money = int(input(' Enter the amount to be withdrawn: '))
        except:
            print('Enter a valid number to withdraw: ')
            break
        instant = Account(name, balance)
        updbalance = instant.withdraw(money)
        cur.execute('UPDATE ACCOUNT SET BALANCE=? WHERE Acc_HOLDER=?', (updbalance, name))
        conn.commit()
    print(instant)
    torun()