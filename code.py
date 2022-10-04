import random, statistics

print("Social pressure on a network")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# INPUTS

# To run the program, first specify

# 1. The distribution of individual tipping points:

p0 = 0.20265441
p1 = 0.032637
p2 = 0.0439544
p3 = 0.0850202
p4 = 0.1231127

# 2. The grid size

s = 10

# 3. The initial share who do the activity

initial_share = 0.5

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# SIMULATIONS

probabilities = [p0, p1, p2, p3, p4]

for element in probabilities:
    if element < 0 or element > 1:
        print("ERROR -- ALL PROBABILITIES MUST BE BETWEEN 0 AND 1!")

if sum(probabilities) > 1:
    print("ERROR -- THE SUM OF PROBABILITIES CANNOT EXCEED 1!")

# If the f function is linear, let's print the fixed point

if p4 == p3 == p2 == p1:
    print(f'Fixed point: {round(p0/(1-4*p1), 2)}')

# Specify the size of the grid (make sure there are no integer issues!)

answers = []

for i in range(1000):

    # Specify the fraction who initially do the action, and randomly scatter on these on a grid

    initial_number = int(initial_share*s**2)

    initial_choices = []
    for i in range(initial_number):
        initial_choices.append(1)
    for i in range(s**2 - initial_number):
        initial_choices.append(0)

    random.shuffle(initial_choices)

    grid = [[0] * s for i in range(s)]

    z = 0
    for i in range(s):
        for j in range(s):
            grid[i][j] = initial_choices[z]
            z += 1

    # Randomly scatter the tipping points on the grid

    coordinates = []
    for i in range(0, s):
        for k in range(0, s):
            coordinates.append([i, k])

    random.shuffle(coordinates)

    tipping_points = [[-1] * s for i in range(s)]

    index = 0
    for element in coordinates:
        x = element[0]
        y = element[1]
        if index < int(s*s*p0):
            tipping_points[x][y] = 0
        elif index < int(s*s*p0) + int(s*s*p1):
            tipping_points[x][y] = 0.25
        elif index < int(s*s*p0) + int(s*s*p1) + int(s*s*p2):
            tipping_points[x][y] = 0.5
        elif index < int(s*s*p0) + int(s*s*p1) + int(s*s*p2) + int(s*s*p3):
            tipping_points[x][y] = 0.75
        elif index < int(s*s*p0) + int(s*s*p1) + int(s*s*p2) + int(s*s*p3) + int(s*s*p4):
            tipping_points[x][y] = 1
        else:
            tipping_points[x][y] = 5
        index += 1

    # Define a function that returns the neighbours of any given player

    def neighbours(coordinate):
        x = coordinate[0]
        y = coordinate[1]
        # Let's handle the corner players
        if [x, y] == [0, 0]:
            return [[0, 1], [1, 0]]
        elif [x, y] == [s-1, s-1]:
            return [[s-1, s-2], [s-2, s-1]]
        elif [x, y] == [0, s-1]:
            return [[1, s-1], [0, s-2]]
        elif [x, y] == [s-1, 0]:
            return [[s-1, 1], [s-2, 0]]
        # Let's handle the side players
        if y == 0:
            return [[x-1, y], [x, y+1], [x+1, y]]
        elif y == s-1:
            return [[x - 1, y], [x, y - 1], [x + 1, y]]
        elif x == 0:
            return [[x, y+1], [x, y-1], [x+1, y]]
        elif x == s-1:
            return [[x, y+1], [x, y-1], [x-1, y]]
        # Finally, the 'interior' players:
        return [[x-1, y], [x+1, y], [x, y-1], [x, y+1]]

    # Define a function that generates the next state (grid) from the old one

    def next_state(old_state):
        new_state = old_state
        # One player is randomly selected to change their choice (if they wish to do so)
        x = random.randint(0, s-1)
        y = random.randint(0, s-1)
        coordinate = [x, y]
        # Let's compute the fraction of their neighbours that are doing the action:
        doing_action = 0
        neighbour_list = neighbours(coordinate)
        for element in neighbour_list:
            a = element[0]
            b = element[1]
            if old_state[a][b] == 1:
                doing_action += 1
        fraction = doing_action/len(neighbour_list)
        # Let's allow them to change their action if they wish to do so
        if fraction >= tipping_points[x][y]:
            new_state[x][y] = 1
        else:
            new_state[x][y] = 0
        return new_state

    # Define a function that calculates how many people are doing for the action

    def counter(state):
        total = 0
        for row in state:
            for entry in row:
                if entry == 1:
                    total += 1
        return total

    # Define a function that checks if we are in a stable state.

    def stable(old_state):
        for i in range(0, s):
            for k in range(0, s):
                player = [i, k]
                current_action = old_state[i][k]
                doing_action = 0
                neighbour_list = neighbours(player)
                for element in neighbour_list:
                    a = element[0]
                    b = element[1]
                    if old_state[a][b] == 1:
                        doing_action += 1
                fraction = doing_action / len(neighbour_list)
                if fraction >= tipping_points[i][k]:
                    desired_action = 1
                else:
                    desired_action = 0
                if current_action != desired_action:
                    return False
        return True


    # Now let's iterate the evolution function many times...

    round = 0
    while not stable(grid):
        grid = next_state(grid)
        round += 1

    answer = counter(grid)/s**2
    answers.append(counter(grid)/s**2)

print(answers)
print(f'Mean: {statistics.mean(answers)}')
print(f'Variance: {statistics.variance(answers)}')
