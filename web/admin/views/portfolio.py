from flask_admin import BaseView, expose


class PortfolioView(BaseView):
    @expose('/')
    def index(self):
        from tasks.securities_tasks import fetch_account_deposit
        job = fetch_account_deposit.delay()
        result = job.wait()
        return self.render('admin/portfolio.html.j2',
                           deposit=result['deposit'],
                           d2_withdrawable_deposit=result['d2_withdrawable_deposit'])
