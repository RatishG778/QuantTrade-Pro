from research.database.repository import ExperimentRepository

repo = ExperimentRepository()

rows = repo.get_all()

print("=" * 60)

print("Experiments")

print("=" * 60)

for row in rows:

    print(row)