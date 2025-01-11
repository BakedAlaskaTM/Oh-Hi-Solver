GRID_SIZE = int(input("Grid Size: "))

def check_row(grid, pointer_row):
    count = {
        "blue": 0,
        "yellow": 0
    }
    for i in grid[pointer_row]:
        if i == 1:
            count["yellow"] += 1
        elif i == 2:
            count["blue"] += 1

    if count["yellow"] == GRID_SIZE/2:
        return 2
    elif count["blue"] == GRID_SIZE/2:
        return 1
    else:
        return 0

def check_col(grid, pointer_col):
    count = {
        "blue": 0,
        "yellow": 0
    }
    for i in range(GRID_SIZE):
        if grid[i][pointer_col] == 1:
            count["yellow"] += 1
        elif grid[i][pointer_col] == 2:
            count["blue"] += 1
    
    if count["yellow"] == GRID_SIZE/2:
        return 2
    elif count["blue"] == GRID_SIZE/2:
        return 1
    else:
        return 0
    
def check_double(grid, pointer_row, pointer_col):
    if pointer_col >= 2: # Left side
        if grid[pointer_row][pointer_col-1] == grid[pointer_row][pointer_col-2]:
            if grid[pointer_row][pointer_col-1] == 1:
                return 2
            elif grid[pointer_row][pointer_col-1] == 2:
                return 1
    
    if pointer_col <= GRID_SIZE-3: # Right side
        if grid[pointer_row][pointer_col+1] == grid[pointer_row][pointer_col+2]:
            if grid[pointer_row][pointer_col+1] == 1:
                return 2
            elif grid[pointer_row][pointer_col+1] == 2:
                return 1
            
    if pointer_row >= 2: # Top side
        if grid[pointer_row-1][pointer_col] == grid[pointer_row-2][pointer_col]:
            if grid[pointer_row-1][pointer_col] == 1:
                return 2
            elif grid[pointer_row-1][pointer_col] == 2:
                return 1
    
    if pointer_row <= GRID_SIZE-3: # Bottom side
        if grid[pointer_row+1][pointer_col] == grid[pointer_row+2][pointer_col]:
            if grid[pointer_row+1][pointer_col] == 1:
                return 2
            elif grid[pointer_row+1][pointer_col] == 2:
                return 1
    return 0

def check_between(grid, pointer_row, pointer_col):
    if pointer_col >= 1 and pointer_col <= GRID_SIZE-2: # Row
        if grid[pointer_row][pointer_col-1] == grid[pointer_row][pointer_col+1]:
            if grid[pointer_row][pointer_col-1] == 1:
                return 2
            elif grid[pointer_row][pointer_col-1] == 2:
                return 1
    
    if pointer_row >= 1 and pointer_row <= GRID_SIZE-2: # Column
        if grid[pointer_row-1][pointer_col] == grid[pointer_row+1][pointer_col]:
            if grid[pointer_row-1][pointer_col] == 1:
                return 2
            elif grid[pointer_row-1][pointer_col] == 2:
                return 1
    
    return 0

def check_same_rows(grid, completed_rows, pointer_row, pointer_col):
    empty_count = 0
    for tile in grid[pointer_row]:
        if tile == 0:
            empty_count += 1
    if empty_count == 2:
        # Identify matching row
        matching_row = GRID_SIZE
        for row in completed_rows:
            matching = True
            for i in range(GRID_SIZE):
                if grid[pointer_row][i] != grid[row][i] and grid[pointer_row][i] != 0:
                    matching = False
                    break
            if matching:
                matching_row = row
                break
        # See which one to flip
        if matching_row == GRID_SIZE:
            return 0
        else:
            if grid[matching_row][pointer_col] == 1:
                return 2
            elif grid[matching_row][pointer_col] == 2:
                return 1
            else:
                return 0
    else:
        return 0

def check_same_cols(grid, completed_cols, pointer_row, pointer_col):
    empty_count = 0
    for i in range(GRID_SIZE):
        if grid[i][pointer_col] == 0:
            empty_count += 1
    if empty_count == 2:
        # Identify matching column
        matching_col = GRID_SIZE
        for col in completed_cols:
            matching = True
            for i in range(GRID_SIZE):
                if grid[i][pointer_col] != grid[i][col] and grid[i][pointer_col] != 0:
                    matching = False
                    break
            if matching:
                matching_col = col
                break
        # See which one to flip
        if matching_col == GRID_SIZE:
            return 0
        else:
            if grid[pointer_row][matching_col] == 1:
                return 2
            elif grid[pointer_row][matching_col] == 2:
                return 1
            else:
                return 0
    else:
        return 0

grid = []
for row in range(GRID_SIZE):
    grid.append([])
    for col in range(GRID_SIZE):
        grid[row].append(int(input(f"Row {row+1} Tile {col+1}: ")))
        
pointer = [0, 0] # Format is [row, col]
completed_rows = []
completed_cols = []
complete = False
while not complete:
    complete = True
    for row in range(GRID_SIZE):
        row_complete = True
        for col in range(GRID_SIZE):
            if grid[pointer[0]][pointer[1]] == 0:
                row_complete = False
                complete = False
                tile_temp = []
                tile_temp.append(check_row(grid, pointer[0]))
                tile_temp.append(check_col(grid, pointer[1]))
                tile_temp.append(check_double(grid, pointer[0], pointer[1]))
                tile_temp.append(check_between(grid, pointer[0], pointer[1]))
                tile_temp.append(check_same_rows(grid, completed_rows, pointer[0], pointer[1]))
                tile_temp.append(check_same_cols(grid, completed_cols, pointer[0], pointer[1]))
                tile_temp = list(set(tile_temp))
                if len(tile_temp) != 1 and tile_temp[0] == 0:
                    tile_temp.remove(0)
                grid[pointer[0]][pointer[1]] = tile_temp[0]

            # Add completed columns to the list
            if pointer[0] == GRID_SIZE-1:
                col_complete = True
                for i in range(GRID_SIZE):
                    if grid[i][pointer[1]] == 0:
                        col_complete = False
                        break
                if col_complete:
                    completed_cols.append(pointer[1])
                    completed_cols = list(set(completed_cols))
            pointer[1] += 1

        # Add completed rows to the list
        if row_complete:
            completed_rows.append(pointer[0])
            completed_rows = list(set(completed_rows))

        pointer[0] += 1
        pointer[1] = 0
    pointer[0] = 0

for row in grid:
    row_display = ""
    num = 1
    for tile in row:
        if num % 4 == 0:
            row_display += f"{str(tile)}    "
        else:
            row_display += f"{str(tile)} "
    print(row_display)
