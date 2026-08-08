from research.optimization.grid_search import GridSearch

grid = GridSearch()

params = grid.moving_average(

    range(5, 30, 5),

    range(30, 120, 10)

)

print("=" * 60)

print(f"Total combinations: {len(params)}")

print("=" * 60)

for p in params[:10]:

    print(p)