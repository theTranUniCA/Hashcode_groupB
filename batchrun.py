import os
import time
import pandas as pd
from main2 import read_input, solve

# Danh sách file theo thứ tự mong muốn
FILE_ORDER = [
    "1_30_00","1_30_01","1_30_02","1_30_03","1_30_04","1_30_05",
    "1_30_06","1_30_07","1_30_08","1_30_09","1_30_10","1_30_11",
    "1_30_12","1_30_13","1_30_14","1_30_15","1_30_16","1_30_17",
    "1_30_18","1_30_19","2_30_00","2_30_01","2_30_02","2_30_03",
    "2_30_04","2_30_05","2_30_06","2_30_07","2_30_08","2_30_09",
    "2_30_10","2_30_11","2_30_12","2_30_13","2_30_14","2_30_15",
    "2_30_16","2_30_17","2_30_18","2_30_19","100_1000_00","100_1000_01",
    "100_1000_02","100_1000_03","100_1000_04","100_1000_05","100_1000_06",
    "100_1000_07","100_5000_00","100_5000_01","100_5000_02","100_5000_03",
    "100_10000_00","100_10000_01","100_10000_02","100_10000_03","200_1000_00",
    "200_1000_01","200_1000_02","200_1000_03","200_5000_00","200_5000_01",
    "200_5000_02","200_5000_03","200_10000_00","200_10000_01","200_10000_02",
    "200_10000_03","250_1000_00","250_1000_01","250_1000_02","250_1000_03",
    "250_5000_00","250_5000_01","250_5000_02","250_5000_03","500_1000_00",
    "500_1000_01","500_1000_02","500_1000_03","500_5000_00","500_5000_01",
    "500_5000_02","500_5000_03","500_10000_00","500_10000_01","500_10000_02",
    "500_10000_03","500_50000_00","500_50000_01","500_50000_02","500_50000_03",
    "500_50000_04","500_50000_05","500_50000_06","500_50000_07","1000_5000_00",
    "1000_5000_01","1000_5000_02","1000_5000_03","1000_10000_00","1000_10000_01",
    "1000_10000_03","1000_10000_12","1000_50000_00","1000_50000_01","1000_50000_02",
    "1000_50000_03","1000_50000_04","1000_50000_05","1000_50000_06","1000_50000_07",
    "2000_10000_00","2000_10000_01","2000_10000_02","2000_10000_03","2000_50000_00",
    "2000_50000_01","2000_50000_02","2000_50000_03"
]


def save_csv(csv_path, row_dict, first_write=False):
    df_row = pd.DataFrame([row_dict])
    df_row.to_csv(
        csv_path,
        index=False,
        mode="w" if first_write else "a",
        header=first_write,
        encoding="utf-8-sig"
    )
    print(f"💾 CSV updated → {csv_path} (size: {os.path.getsize(csv_path)} bytes)")


def run_batch(input_dir, output_dir="./output_batch"):
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "batch_results.csv")

    # Lấy tất cả file .in hiện có
    files_in_dir = [f for f in os.listdir(input_dir) if f.endswith(".in")]

    # Chỉ giữ những file có trong FILE_ORDER và tồn tại trong thư mục
    files = [f"{name}.in" for name in FILE_ORDER if f"{name}.in" in files_in_dir]

    if not files:
        print("⚠️ Không tìm thấy file .in nào trong thư mục!")
        return

    print(f"📂 Tìm thấy {len(files)} file cần xử lý theo thứ tự định sẵn.\n")

    first_write = True
    for filename in files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".in", ".out"))

        print(f"🚗 Processing {filename}...")
        try:
            rows, cols, veh, n_rides, bonus, steps, rides = read_input(input_path)

            start_time = time.time()
            score, sched = solve(rows, cols, veh, n_rides, bonus, steps, rides)
            elapsed = time.time() - start_time

            # Lưu .out
            with open(output_path, "w", encoding="utf-8") as f:
                for r in sched:
                    f.write(str(len(r)) + " " + " ".join(map(str, r)) + "\n")

            print(f"✅ Done {filename} | Score={score} | Time={elapsed:.2f}s")

            row = {
                "File": filename,
                "Score": score,
                "Execution Time (s)": round(elapsed, 3),
                "Vehicles": veh,
                "Number of Rides": n_rides,
                "Output Path": output_path,
                "Status": "OK"
            }

        except Exception as e:
            print(f"❌ Error on {filename}: {e}")
            row = {
                "File": filename,
                "Score": "ERROR",
                "Execution Time (s)": None,
                "Vehicles": None,
                "Number of Rides": None,
                "Output Path": output_path,
                "Status": f"ERROR: {str(e)}"
            }

        save_csv(csv_path, row, first_write)
        first_write = False
        print("-" * 60)

    print(f"\n✅ Batch finished.")
    print(f"📊 CSV saved to: {csv_path}")
    return csv_path


if __name__ == "__main__":
    input_folder = r"D:\Downloads\TEMP\generated_instances\generated_instances"
    run_batch(input_folder)
