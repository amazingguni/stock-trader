from flask_admin import BaseView, expose
# from tasks.securities_tasks import fetch_account_deposit


class PortfolioView(BaseView):
    pass
    # @expose('/')
    # def index(self):
    #     job = fetch_account_deposit.delay()
    #     result = job.wait()
    #     return self.render('admin/portfolio.html.j2',
    #                        deposit=result['deposit'],
    #                        d2_withdrawable_deposit=result['d2_withdrawable_deposit'])
