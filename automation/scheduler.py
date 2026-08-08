from automation.jobs import AutomationJob


class Scheduler:

    def create_jobs(

        self,

        symbols,

        strategies

    ):

        jobs = []

        for symbol in symbols:

            for strategy in strategies:

                jobs.append(

                    AutomationJob(

                        symbol=symbol,

                        strategy=strategy

                    )

                )

        return jobs