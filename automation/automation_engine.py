from datetime import datetime

from automation.scheduler import Scheduler
from automation.notifications import NotificationService

from dashboard.run_backtest import run_backtest


class AutomationEngine:

    def __init__(self):

        self.scheduler = Scheduler()

    def run(

        self,

        config

    ):

        jobs = self.scheduler.create_jobs(

            config.symbols,

            config.strategies

        )

        results = []

        for job in jobs:

            try:

                job.status = "Running"

                job.started_at = datetime.now()

                NotificationService.info(

                    f"{job.symbol} | {job.strategy}"

                )

                result = run_backtest(

                    symbol=job.symbol,

                    capital=config.capital,

                    strategy_name=job.strategy

                )

                job.status = "Completed"

                job.finished_at = datetime.now()

                results.append(result)

                NotificationService.success(

                    f"{job.symbol} completed"

                )

            except Exception as e:

                job.status = "Failed"

                job.finished_at = datetime.now()

                job.error = str(e)

                NotificationService.error(

                    f"{job.symbol}: {e}"

                )

        return results