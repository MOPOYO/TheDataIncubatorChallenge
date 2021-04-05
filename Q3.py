import numpy as np


# #### Question: You roll a fair 6-sided dice repeatedly until the sum of the dice rolls is greater than or equal to M. For all questions, give your answer to 5 decimal places.

# ##### 1. What is the mean of the sum minus M when M=20?

# set up the fair 6-sided dice
dice = [i+1 for i in range(6)]
probabilities = [1/6 for i in range(6)]

# roll a fair 6-sided dice repeatedly until the sum of the dice rolls is greater than or equal to M
M = 20
dice_sum = 0
while dice_sum < M:
    dice_sum += np.random.choice(dice, p = probabilities, size = 1)
print(dice_sum)

# Make the rolling of dices as a function
def roll_dice(M):
    dice_sum = 0
    count = 0 
    while dice_sum < M:
        dice_sum +=  np.random.choice(dice, p = probabilities, size = 1)
        count += 1
    return dice_sum, count

# run statisitcal simulation to model 50000 times, and record the results into an array
sums_20 = np.empty(50000)
counts_20 = np.empty(50000)

for i in range(len(sums_20)):
    sums_20[i] = roll_dice(M = 20)[0]
    counts_20[i] = roll_dice(M = 20)[1]

# calculate the mean of the sum minus M when M = 20
Q1_mean = np.mean(sums_20 - 20)

print("the mean of the sum minus M when M = 20 is {:.5f}".format(Q1_mean))


# ##### 2. What is the mean of the number of rolls when M=20?

# calculate the mean of the number of rolls when M=20?
Q2_number = np.mean(counts_20)

print("the mean of the number of rolls when M=20 is {:.5f}".format(Q2_number))


# ##### 3. What is the standard deviation of the sum minus M when M=20?

# calculate the standard deviation of the sum minus M when M=20
Q3_std = np.std(sums_20 - 20)

print("the standard deviation of the sum minus M when M = 20 is {:.5f}".format(Q3_std))


# ##### 4. What is the mean of the sum minus M when M=5000?

# run statisitcal simulation to model 50000 times, and record the results into an array
sums_5000 = np.empty(50000)
counts_5000 = np.empty(50000)

for i in range(len(sums_5000)):
    sums_5000[i] = roll_dice(M = 5000)[0]
    counts_5000[i] = roll_dice(M = 5000)[1]

# calculate the mean of the sum minus M when M = 5000
Q4_mean = np.mean(sums_5000 - 5000)

print("the mean of the sum minus M when M = 5000 is {:.5f}".format(Q4_mean))


# ##### 5. What is the mean of the number of rolls when M=5000?

# calculate the mean of the number of rolls when M=5000?
Q5_number = np.mean(counts_5000)

print("the mean of the number of rolls when M=5000 is {:.5f}".format(Q5_number))


# ##### 6. What is the standard deviation of the sum minus M when M=5000?

# calculate the standard deviation of the sum minus M when M=5000
Q6_std = np.std(sums_5000 - 5000)

print("the standard deviation of the sum minus M when M = 5000 is {:.5f}".format(Q6_std))



