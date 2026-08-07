import numpy as np


class MonteCarloMetrics:

    @staticmethod
    def summarize(results):

        return {

            "best": float(np.max(results)),

            "worst": float(np.min(results)),

            "average": float(np.mean(results)),

            "median": float(np.median(results)),

            "std": float(np.std(results)),

            "p5": float(np.percentile(results, 5)),

            "p95": float(np.percentile(results, 95))

        }