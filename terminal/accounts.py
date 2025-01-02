import json
import uuid
from terminal.crawl import Crawl
import pytz
import schedule
import calendar
import time
from datetime import datetime
from threading import Thread

class Account:
    def __init__(self):
        with open('db.json', 'r') as file:
            data = json.load(file)
            self.accounts = data.get('accounts', [])

    def get(self):
        return self.accounts

    def add(self, account):
        account['id'] = str(uuid.uuid4())  # Generate a unique ID
        self.accounts.append(account)
        self.save()

    def save(self):
        with open('db.json', 'w') as file:
            json.dump({'accounts': self.accounts}, file, indent=4)