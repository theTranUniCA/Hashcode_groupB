import os
import heapq
from dataclasses import dataclass


@dataclass
class Ride:
    startRow: int
    startCol: int
    endRow: int
    endCol: int
    earliestStart: int
    latestFinish: int

    def length(self):
        return abs(self.startRow - self.endRow) + abs(self.startCol - self.endCol)


def readInput(filename):
    with open(filename, "r") as f:
        rows, cols, numVehicles, numRides, bonus, totalSteps = map(int, f.readline().split())
        rides = []
        for _ in range(numRides):
            a, b, x, y, s, f_end = map(int, f.readline().split())
            rides.append(Ride(a, b, x, y, s, f_end))
    return rows, cols, numVehicles, numRides, bonus, totalSteps, rides


def manhattanDistance(pointA, pointB):
    return abs(pointA[0] - pointB[0]) + abs(pointA[1] - pointB[1])


def computeScore(vehicleSchedules, rides, bonus):
    """Compute total score from schedules."""
    score = 0
    for schedule in vehicleSchedules:
        time = 0
        position = (0, 0)
        for idx in schedule:
            ride = rides[idx]
            distToStart = manhattanDistance(position, (ride.startRow, ride.startCol))
            startTime = max(time + distToStart, ride.earliestStart)
            finishTime = startTime + ride.length()
            if finishTime <= ride.latestFinish:
                score += ride.length()
                if startTime == ride.earliestStart:
                    score += bonus
                position = (ride.endRow, ride.endCol)
                time = finishTime
            else:
                break
    return score


def solve(rows, cols, numVehicles, numRides, bonus, totalSteps, rides):
    rideLengths = [ride.length() for ride in rides]

    # Vehicle state
    vehiclePositions = [(0, 0) for _ in range(numVehicles)]
    vehicleSchedules = [[] for _ in range(numVehicles)]
    rideTaken = [False] * numRides

    # Min-heap: (timeVehicleIsFree, vehicleIndex)
    availableVehicles = [(0, v) for v in range(numVehicles)]
    heapq.heapify(availableVehicles)

    while availableVehicles:
        currentTime, vehicleIndex = heapq.heappop(availableVehicles)

        if currentTime >= totalSteps:
            continue

        bestStartTime = totalSteps
        bestRideIndex = -1

        for i, ride in enumerate(rides):
            if rideTaken[i]:
                continue

            distToStart = manhattanDistance(vehiclePositions[vehicleIndex],
                                            (ride.startRow, ride.startCol))
            finishTime = currentTime + distToStart + rideLengths[i]

            if finishTime > ride.latestFinish:
                continue

            startTime = max(currentTime + distToStart, ride.earliestStart)
            if startTime < bestStartTime:
                bestStartTime = startTime
                bestRideIndex = i

        if bestRideIndex == -1:
            continue

        # Assign the ride
        rideTaken[bestRideIndex] = True
        ride = rides[bestRideIndex]
        vehicleSchedules[vehicleIndex].append(bestRideIndex)

        vehiclePositions[vehicleIndex] = (ride.endRow, ride.endCol)
        newTime = bestStartTime + rideLengths[bestRideIndex]
        heapq.heappush(availableVehicles, (newTime, vehicleIndex))

    # ---- Local Search Optimization ----
    improved = True
    while improved:
        improved = False
        for v1 in range(numVehicles):
            for v2 in range(v1 + 1, numVehicles):
                for i in range(len(vehicleSchedules[v1])):
                    for j in range(len(vehicleSchedules[v2])):
                        # Swap ride i in v1 with ride j in v2
                        vehicleSchedules[v1][i], vehicleSchedules[v2][j] = vehicleSchedules[v2][j], vehicleSchedules[v1][i]
                        newScore = computeScore(vehicleSchedules, rides, bonus)
                        if newScore > computeScore(vehicleSchedules, rides, bonus):
                            improved = True
                        else:
                            # Swap back if not better
                            vehicleSchedules[v1][i], vehicleSchedules[v2][j] = vehicleSchedules[v2][j], vehicleSchedules[v1][i]
    totalScore = computeScore(vehicleSchedules, rides, bonus)
    return totalScore, vehicleSchedules


def writeOutput(filename, vehicleSchedules):
    with open(filename, "w") as f:
        for rides in vehicleSchedules:
            f.write(str(len(rides)) + " " + " ".join(map(str, rides)) + "\n")


if __name__ == "__main__":
    filename = "./input/bCopy.in"
    rows, cols, numVehicles, numRides, bonus, totalSteps, rides = readInput(filename)

    totalScore, vehicleSchedules = solve(rows, cols, numVehicles, numRides, bonus, totalSteps, rides)
    print("Score =", totalScore)

    os.makedirs("./output", exist_ok=True)
    baseName = os.path.basename(filename).replace(".in", ".out")
    outFile = os.path.join("./output", baseName)
    writeOutput(outFile, vehicleSchedules)
