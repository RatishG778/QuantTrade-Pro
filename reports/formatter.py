class ReportFormatter:

    @staticmethod
    def console(report):

        print("=" * 60)

        print("QUANTTRADE-PRO RESEARCH REPORT")

        print("=" * 60)

        exp = report["experiment"]

        print(f"Strategy : {exp.strategy}")

        print(f"Profit   : {exp.profit}")

        print(f"Trades   : {exp.trades}")

        val = report["validation"]

        print(f"Robustness : {val['robustness']}")

        print("=" * 60)