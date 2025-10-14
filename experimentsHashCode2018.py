import sys
import json
import time

def distance(x, y, a, b):
    return abs(y - b) + abs(x - a)

def generate_json(rides, solutions, output_file, row, column, B):
    """Generate JSON file with rides info including status code, start_time, end_time"""
    json_data = {
        "row": row,
        "column": column,
        "rides": []
    }

    ride_info = [[r["start_x"], r["start_y"], r["finish_x"], r["finish_y"], -1, None, None] for r in rides]

    for vehicle_rides in solutions:
        last_x, last_y = 0, 0
        current_time = 0
        for rid in vehicle_rides:
            r = rides[rid]
            dist2start = distance(r["start_x"], r["start_y"], last_x, last_y)
            start_time = current_time + dist2start
            qualifier = 0
            if start_time <= r["earliest_start"]:
                start_time = r["earliest_start"]
                qualifier = 1000  # bonus
            dist2dest = distance(r["start_x"], r["start_y"], r["finish_x"], r["finish_y"])
            end_time = start_time + dist2dest
            if end_time <= r["latest_finish"]:
                if qualifier != 1000:
                    qualifier = 1  # completed but no bonus
                ride_info[rid] = [r["start_x"], r["start_y"], r["finish_x"], r["finish_y"], qualifier, start_time, end_time]
                last_x, last_y = r["finish_x"], r["finish_y"]
                current_time = end_time

    json_data["rides"] = ride_info

    json_file = output_file + ".json"
    with open(json_file, "w") as f:
        json.dump(json_data, f, indent=2)
    print(f"JSON saved to: {json_file}")

def main():
    start_time = time.time()  # Start execution timer

    if len(sys.argv) < 3:
        print("USAGE: python judge.py input output")
        sys.exit(0)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Read input file
    try:
        with open(input_file, "r") as f:
            R, C, F, N, B, T = map(int, f.readline().split())
            rides = []
            for _ in range(N):
                sx, sy, fx, fy, es, lf = map(int, f.readline().split())
                rides.append({
                    "start_x": sx,
                    "start_y": sy,
                    "finish_x": fx,
                    "finish_y": fy,
                    "earliest_start": es,
                    "latest_finish": lf,
                    "finished": False
                })
    except FileNotFoundError:
        print(f"Cannot open file {input_file}")
        sys.exit(0)

    # Read output file
    try:
        with open(output_file, "r") as f:
            lines = [list(map(int, line.split())) for line in f.readlines()]
    except FileNotFoundError:
        print(f"Cannot open file {output_file}")
        sys.exit(0)

    # Parse solution
    solutions = [[] for _ in range(F)]
    nbRides = 0
    for i in range(F):
        if not lines:
            print("Not enough lines in output file.")
            sys.exit(0)
        M, *rides_ids = lines[i]
        if M != len(rides_ids):
            print(f"Invalid format in vehicle {i}: expected {M} rides, got {len(rides_ids)}.")
            sys.exit(0)

        for r_id in rides_ids:
            if r_id < 0 or r_id >= N:
                print(f"There is no ride number {r_id}.")
                sys.exit(0)
            if rides[r_id]["finished"]:
                print(f"Ride number {r_id} is already assigned.")
                sys.exit(0)
            rides[r_id]["finished"] = True
            solutions[i].append(r_id)
        nbRides += M

    if nbRides > N:
        print("Too many rides assigned.")
        sys.exit(0)

    # Compute score
    car_scores = [0] * F
    car_times = [0] * F
    total_distance = 0
    bonus_count = 0
    completed_rides = 0

    for i in range(F):
        last_x, last_y = 0, 0
        current_time = 0
        for r_id in solutions[i]:
            r = rides[r_id]
            dist2start = distance(r["start_x"], r["start_y"], last_x, last_y)
            start = dist2start + current_time
            bonus = 0
            if start <= r["earliest_start"]:
                start = r["earliest_start"]
                bonus = B
                bonus_count += 1
            dist2dest = distance(r["start_x"], r["start_y"], r["finish_x"], r["finish_y"])
            if start + dist2dest <= r["latest_finish"]:
                car_scores[i] += bonus + dist2dest
                total_distance += dist2dest
                completed_rides += 1
                last_x, last_y = r["finish_x"], r["finish_y"]
                current_time = start + dist2dest
        car_times[i] = current_time

    total_score = sum(car_scores)
    total_time = max(car_times)
    pct_complete_rides = 100 * completed_rides / len(rides) if len(rides) > 0 else 0
    pct_bonus = 100 * bonus_count / completed_rides if completed_rides > 0 else 0
    score_per_distance = total_score / total_distance if total_distance > 0 else 0
    execution_time = time.time() - start_time

    print(f"Score = {total_score}")
    print(f"Total Time = {total_time} / {T}")
    print(f"% of Complete Rides = {pct_complete_rides:.2f}%")
    print(f"% Bonuses = {pct_bonus:.2f}%")
    print(f"Score/Distance = {score_per_distance:.2f}")
    print(f"Execution Time = {execution_time:.4f} seconds")

    # Generate JSON file
    generate_json(rides, solutions, output_file, R, C, B)

if __name__ == "__main__":
    main()
