from core.account.domain.repository import AccountRepository
from core.holding.domain.repository import HoldingSummaryRepository
from core.holding.domain.service import FetchHoldingSummaryService


class SyncHoldingSummaryService:
    def __init__(self, account_repository: AccountRepository,
                 holding_summary_repository: HoldingSummaryRepository,
                 fetch_holding_summary_service: FetchHoldingSummaryService):
        self.account_repository = account_repository
        self.holding_summary_repository = holding_summary_repository
        self.fetch_holding_summary_service = fetch_holding_summary_service

    def sync(self):
        primary_account = self.account_repository.find_primary_account()
        holding_summary = self.fetch_holding_summary_service.fetch(
            primary_account.number)
        self.holding_summary_repository.save(holding_summary)
