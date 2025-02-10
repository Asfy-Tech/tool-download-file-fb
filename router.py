from pages.home import main_page
from pages.accounts import accounts_page
from pages.add_account import add_account_page
from pages.logs import logs_page
from pages.settings import settings_page
from pages.login import login_page
router = {
    'home' : main_page,
    'accounts' : accounts_page,
    'add_account' : add_account_page,
    'logs': logs_page,
    'settings': settings_page,
    'login': login_page,
}
