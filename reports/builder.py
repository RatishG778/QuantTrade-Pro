class ResearchReportBuilder:

    def build(

        self,

        experiment,

        validation,

        portfolio=None

    ):

        report = {

            "experiment": experiment,

            "validation": validation,

            "portfolio": portfolio

        }

        return report