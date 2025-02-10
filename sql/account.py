import json
import uuid

class Account:
    def __init__(self):
        self.accounts = self.load_files()

    def load_files(self):
        dataFile = {}
        try:
            with open('db.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                listData = data.get('accounts', [])
                for acc in listData:
                    dataFile[acc.get('id')] = acc
        except FileNotFoundError:
            dataFile = {}
        except Exception:
            dataFile = {}
        return dataFile

    def get_all(self):
        return self.load_files()

    def add(self, account):
        account['id'] = str(uuid.uuid4())  # Generate a unique ID
        self.accounts[account['id']] = account
        self.save()

    def update(self, account):
        acc = self.accounts.get(account.get('id'))
        if acc:
            self.accounts[account.get('id')] = account
        self.save()

    def save(self):
        data = []
        for idx, acc in self.accounts.items():
            account_copy = acc.copy()
            if 'row' in account_copy:
                del account_copy['row']
            data.append(account_copy)

        with open('db.json', 'w') as file:
            json.dump({'accounts': data}, file, indent=4)
