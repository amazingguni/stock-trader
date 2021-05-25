from core.holding.domain import HoldingSummary


class HoldingSummaryRepository:
    def save(self, holding_summary: HoldingSummary):
        holding_summary.save()
