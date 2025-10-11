import random

def generate_random_instance(filename, rows=3, cols=4, vehicles=2, n_rides=3,
                                              bonus=2, steps=10, seed=None):
    """
    Generate a random instance and print a human-readable description of rides.
    """
    if seed is not None:
        random.seed(seed)

    rides = []
    for i in range(n_rides):
        a = random.randint(0, rows-1)
        b = random.randint(0, cols-1)
        x = random.randint(0, rows-1)
        y = random.randint(0, cols-1)
        while a == x and b == y:
            x = random.randint(0, rows-1)
            y = random.randint(0, cols-1)

        earliest_start = random.randint(0, steps//2)
        ride_duration = abs(a - x) + abs(b - y)
        latest_finish = earliest_start + ride_duration + random.randint(0, steps//2)
        latest_finish = min(latest_finish, steps)

        rides.append((a, b, x, y, earliest_start, latest_finish))

    # Write to file
    with open(filename, "w") as f:
        f.write(f"{rows} {cols} {vehicles} {n_rides} {bonus} {steps}\n")
        for ride in rides:
            f.write(" ".join(map(str, ride)) + "\n")

    # Print human-readable description
    print(f"{rows} rows, {cols} columns, {vehicles} vehicles, {n_rides} rides, {bonus} bonus and {steps} steps")
    for i, (a, b, x, y, s, f) in enumerate(rides):
        print(f"ride {i+1} from [{a}, {b}] to [{x}, {y}], earliest start {s}, latest finish {f}")

    return rides

def compute_max_possible_score(rides, bonus):
    """
    Compute the maximum possible score assuming:
    - Every ride is completed.
    - Every ride starts at its earliest start (gets bonus).
    """
    max_score = 0
    for a, b, x, y, s, f in rides:
        ride_len = abs(a - x) + abs(b - y)
        max_score += ride_len + bonus
    return max_score


rides = generate_random_instance("./input/random_instance.in", rows=800, cols=1000,
                                 vehicles=100, n_rides=300, bonus=25, steps=25000, seed=42)

max_score = compute_max_possible_score(rides, bonus=25)
print("Maximum possible theoretical score (all rides completed + all bonuses):", max_score)
