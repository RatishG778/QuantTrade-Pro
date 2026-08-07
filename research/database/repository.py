from research.database.database import ResearchDatabase


class ExperimentRepository:

    def __init__(self):

        self.db = ResearchDatabase()

    def save(self, experiment):

        cursor = self.db.connection.cursor()

        cursor.execute("""
        INSERT INTO experiments(

            created_at,
            strategy,
            symbol,
            capital,
            parameters,
            profit,
            return_pct,
            sharpe,
            max_drawdown,
            trades,
            win_rate

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?)
        """, (

            experiment["created_at"],

            experiment["strategy"],

            experiment["symbol"],

            experiment["capital"],

            experiment["parameters"],

            experiment["profit"],

            experiment["return_pct"],

            experiment["sharpe"],

            experiment["max_drawdown"],

            experiment["trades"],

            experiment["win_rate"]

        ))

        self.db.connection.commit()