from research.optimization.parameter_grid import ParameterGrid

grid = ParameterGrid()

params = grid.moving_average()

print(f"Total combinations : {len(params)}")

for p in params[:10]:

    print(p)