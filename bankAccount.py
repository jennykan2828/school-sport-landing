class BankAccount:
    """Base class for all bank accounts."""

    def __init__(self, name, gender, account_no, currency="USD", initial_balance=0.0):
        self.name = name
        self.gender = gender
        self.account_no = account_no
        self.currency = currency
        self.balance = initial_balance
        self.transactions = []

    def deposit(self, amount, method="Counter"):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposit: +{amount} ({method})")
            return True
        return False

    def withdraw(self, amount, method="Counter"):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdraw: -{amount} ({method})")
            return True
        return False

    def check_balance(self):
        return self.balance


class DepositAccount(BankAccount):
    """A savings/deposit account that might restrict heavy withdrawals."""

    def __init__(
        self,
        name,
        gender,
        account_no,
        currency="USD",
        initial_balance=0.0,
        interest_rate=0.02,
    ):
        super().__init__(name, gender, account_no, currency, initial_balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        """Adds interest to the savings balance."""
        interest = self.balance * self.interest_rate
        self.deposit(interest, method="Interest Yield")


class CheckingAccount(BankAccount):
    """A standard transactional checking account with an overdraft limit."""

    def __init__(
        self,
        name,
        gender,
        account_no,
        currency="USD",
        initial_balance=0.0,
        overdraft_limit=500.0,
    ):
        super().__init__(name, gender, account_no, currency, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount, method="ATM/Debit"):
        """Overridden to allow overdraft up to the limit."""
        if 0 < amount <= (self.balance + self.overdraft_limit):
            self.balance -= amount
            self.transactions.append(f"Withdraw: -{amount} ({method})")
            return True
        print("Transaction declined: Overdraft limit exceeded.")
        return False


class Bank:
    """Manages all accounts and central system workflows."""

    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.accounts = {}  # Stores accounts as account_no: account_object

    def add_account(self, account):
        self.accounts[account.account_no] = account
        print(f"Account {account.account_no} successfully added to {self.bank_name}.")

    def get_account(self, account_no):
        return self.accounts.get(account_no, None)

    def transfer(self, from_acc_no, to_acc_no, amount):
        """Transfers funds between two managed accounts."""
        from_acc = self.get_account(from_acc_no)
        to_acc = self.get_account(to_acc_no)

        if not from_acc or not to_acc:
            print("Transfer failed: One or both account numbers are invalid.")
            return False

        if from_acc.currency != to_acc.currency:
            print("Transfer failed: Currency mismatch.")
            return False

        if from_acc.withdraw(amount, method=f"Transfer to {to_acc_no}"):
            to_acc.deposit(amount, method=f"Transfer from {from_acc_no}")
            print(
                f"Successfully transferred {amount} {from_acc.currency} from {from_acc_no} to {to_acc_no}."
            )
            return True
        return False


# 1. Initialize the Central Bank
my_bank = Bank("Global Trust Bank")

# 2. Open a Checking and Deposit account
checking = CheckingAccount("Alex Dan", "Male", "CH-1001", "USD", 200.0)
deposit = DepositAccount("Alex Dan", "Male", "DP-2002", "USD", 5000.0)

my_bank.add_account(checking)
my_bank.add_account(deposit)

# 3. Test Checking Overdraft
checking.withdraw(
    300.0, "ATM"
)  # Balance goes down to -100.0 (Allowed due to $500 overdraft limit)

# 4. Test Internal Transfer via the Bank System
my_bank.transfer("DP-2002", "CH-1001", 1000.0)

# Check Final Balances
print(f"Checking Balance: ${checking.check_balance()}")  # Result: $900.0
print(f"Deposit Balance: ${deposit.check_balance()}")  # Result: $4000.0
