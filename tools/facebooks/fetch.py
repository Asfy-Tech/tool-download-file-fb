def fetch_data(account):
    from helpers.base import render
    from terminal.crawl import Crawl
    crawl = Crawl(account,False)
    crawl.run()
    render('accounts')
