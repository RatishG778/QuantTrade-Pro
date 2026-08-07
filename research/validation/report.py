class ValidationReport:

    @staticmethod
    def generate(validation):

        print("\n" + "=" * 60)
        print("RESEARCH VALIDATION REPORT")
        print("=" * 60)

        print(f"Profit            : {validation['profit']:.2f}")

        print(f"Drawdown         : {validation['drawdown']:.2f}%")

        print(f"Trades           : {validation['trades']}")

        print(f"Walk Forward     : {'PASS' if validation['passed'] else 'FAIL'}")

        print(f"Robustness Score : {validation['robustness']:.2f}")

        print("=" * 60)

        if validation["robustness"] >= 80:

            print("Recommendation : Continue Research")

        elif validation["robustness"] >= 60:

            print("Recommendation : Needs Improvement")

        else:

            print("Recommendation : Reject Strategy")

        print("=" * 60)