from src.main import Actions, read_grid_file, get_script


def run_testcase(filename):
    origin, passager, target, grid = read_grid_file(filename)
    width = len(grid[0])
    height = len(grid)
    script = get_script(origin, passager, target, grid)
    has_passenger = False
    picked_passenger = False
    pos_x, pos_y = origin[0], origin[1]

    for step in script:
        if step == Actions.GO_UP:
            pos_y -= 1
        elif step == Actions.GO_DOWN:
            pos_y += 1
        elif step == Actions.GO_LEFT:
            pos_x -= 1
        elif step == Actions.GO_RIGHT:
            pos_x += 1
        elif step == Actions.PICK_PASSENGER:
            if pos_x == passager[0] and pos_y == passager[1]:
                has_passenger = True
                picked_passenger = True

            assert has_passenger, "Invalid passager location!"
        elif step == Actions.DROP_PASSENGER:
            assert has_passenger, "No passenger to drop!"

            if pos_x == target[0] and pos_y == target[1]:
                has_passenger = False

            assert has_passenger == False, "Dropped passager on invalid location!"
        
        assert pos_x >= 0, "Fell from world!"
        assert pos_y >= 0, "Fell from world!"
        assert pos_x < width, "Fell from world!"
        assert pos_y < height, "Fell from world!"
        assert grid[pos_y][pos_x] == False, "Run through wall!"

    assert picked_passenger, "Piecked no passenger!"
    assert pos_x == target[0] and pos_y == target[1], "Didn't reached target"
