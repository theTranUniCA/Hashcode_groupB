import random
import argparse


# ------------------ GENERATION ------------------
def generate_dataset(R, C, F, N, B, T, output_file):
    rides = []
    for i in range(N):
        a, b = random.randint(0, R-1), random.randint(0, C-1)
        x, y = random.randint(0, R-1), random.randint(0, C-1)
        dist = abs(x - a) + abs(y - b)
        s = random.randint(0, max(0, T - dist - 1))
        slack = random.randint(dist, min(T-1, dist*2))
        f_time = min(T, s + dist + slack)
        rides.append((a, b, x, y, s, f_time))

    with open(output_file, "w") as f:
        f.write(f"{R} {C} {F} {N} {B} {T}\n")
        for r in rides:
            f.write(" ".join(map(str, r)) + "\n")


# ------------------ MAIN ------------------
def main():
    parser = argparse.ArgumentParser(description="Hash Code dataset generator")
    parser.add_argument("mode", choices=["generate"], help="Mode of operation")
    parser.add_argument("input_file", help="Input dataset file)")
    parser.add_argument("output_file", help="Output dataset file")
    parser.add_argument("--num_rides", type=int, help="Number of rides for sampling or generation")
    parser.add_argument("--R", type=int, help="Rows (for generate)")
    parser.add_argument("--C", type=int, help="Columns (for generate)")
    parser.add_argument("--F", type=int, help="Vehicles (for generate)")
    parser.add_argument("--B", type=int, help="Bonus (for generate)")
    parser.add_argument("--T", type=int, help="Steps horizon (for generate)")
    parser.add_argument("--coord_shift", type=int, default=10, help="Coordinate perturbation")
    parser.add_argument("--time_shift", type=int, default=50, help="Time perturbation")
    args = parser.parse_args()
        
    generate_dataset(args.R, args.C, args.F, args.num_rides, args.B, args.T, args.output_file)

if __name__ == "__main__":
    main()



#Execution
# python instanceGeneration.py generate c_no_hurry.in c_generateddata.in --R 100 --C 100 --F 10 --num_rides 200 --B 2 --T 10000
