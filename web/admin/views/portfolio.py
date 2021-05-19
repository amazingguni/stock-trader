from flask_admin import BaseView, expose


from tasks.stock_summaries import get_account_deposit


class PortfolioView(BaseView):
    @expose('/')
    def index(self):
        job = get_account_deposit.delay()
        result = job.wait()
        return self.render('admin/portfolio.html.j2',
                           deposit=result['deposit'],
                           d2_withdrawable_deposit=result['d2_withdrawable_deposit'])
