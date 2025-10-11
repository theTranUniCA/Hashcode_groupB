import os
import argparse


def read_input(filename):
    """
    Read the input file and parse the problem parameters.
    Returns: rows, cols, vehicles, number of rides, bonus, total steps, rides list
    """
    with open(filename, "r") as f:
        rows, cols, veh, n_rides, bonus, steps = map(int, f.readline().split())
        rides = []
        for _ in range(n_rides):
            a, b, x, y, s, f_end = map(int, f.readline().split())
            rides.append((a, b, x, y, s, f_end))
    return rows, cols, veh, n_rides, bonus, steps, rides


def manhattan(a, b):
    """Compute Manhattan distance between two points a and b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve(rows, cols, veh, n_rides, bonus, steps, rides):
    """
    Greedy heuristic solver:
    Assign rides to vehicles based on earliest available vehicle
    and earliest feasible ride start time.
    """
    ride_len = [manhattan((a, b), (x, y)) for (a, b, x, y, s, f) in rides]

    t_of_the_car = [0] * veh
    car_x = [0] * veh
    car_y = [0] * veh
    sched = [[] for _ in range(veh)]

    taken = [False] * n_rides
    score = 0

    while True:
        cur_t = steps
        j = -1
        for v in range(veh):
            if t_of_the_car[v] < cur_t:
                cur_t = t_of_the_car[v]
                j = v

        if cur_t >= steps or j == -1:
            break

        best_start = steps
        k = -1
        for i in range(n_rides):
            if taken[i]:
                continue
            a, b, x, y, s, f = rides[i]
            go = manhattan((car_x[j], car_y[j]), (a, b))
            finish = cur_t + go + ride_len[i]

            if finish <= f:
                start_time = max(cur_t + go, s)
                if start_time < best_start:
                    best_start = start_time
                    k = i

        if k == -1:
            t_of_the_car[j] = steps
            continue

        taken[k] = True
        a, b, x, y, s, f = rides[k]
        sched[j].append(k)
        car_x[j], car_y[j] = x, y
        t_of_the_car[j] = best_start + ride_len[k]

        score += ride_len[k]
        if best_start == s:
            score += bonus

    return score, sched


def write_output(filename, sched):
    """Write the vehicle schedules to output file."""
    with open(filename, "w") as f:
        for rides in sched:
            f.write(str(len(rides)) + " " + " ".join(map(str, rides)) + "\n")

    print("=== Vehicle Ride Assignments ===")
    for i, rides in enumerate(sched):
        print(f"Vehicle {i} is assigned {len(rides)} rides: {rides}")


def main():
    parser = argparse.ArgumentParser(description="Hash Code Ride Scheduling Solver")
    parser.add_argument("--input", "-i", required=True, help="Path to input file (.in)")
    parser.add_argument("--output", "-o", default=None, help="Path to save output file (.out)")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    if output_file is None:
        os.makedirs("./output", exist_ok=True)
        base = os.path.basename(input_file).replace(".in", ".out")
        output_file = os.path.join("./output", base)

    print(f"Reading input file: {input_file}")
    rows, cols, veh, n_rides, bonus, steps, rides = read_input(input_file)

    print(f"Solving... (vehicles={veh}, rides={n_rides})")
    score, sched = solve(rows, cols, veh, n_rides, bonus, steps, rides)
    print(f"✅ Final Score = {score}")

    write_output(output_file, sched)
    print(f"\n📁 Output saved to {output_file}")


if __name__ == "__main__":
    main()
