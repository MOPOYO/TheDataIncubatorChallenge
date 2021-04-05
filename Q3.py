#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# #### Question: You roll a fair 6-sided dice repeatedly until the sum of the dice rolls is greater than or equal to M. For all questions, give your answer to 5 decimal places.

# ##### 1. What is the mean of the sum minus M when M=20?

# In[6]:


# set up the fair 6-sided dice
dice = [i+1 for i in range(6)]
probabilities = [1/6 for i in range(6)]


# In[8]:


# roll a fair 6-sided dice repeatedly until the sum of the dice rolls is greater than or equal to M
M = 20
dice_sum = 0
while dice_sum < M:
    dice_sum += np.random.choice(dice, p = probabilities, size = 1)
print(dice_sum)


# In[9]:


# Make the rolling of dices as a function
def roll_dice(M):
    dice_sum = 0
    count = 0 
    while dice_sum < M:
        dice_sum +=  np.random.choice(dice, p = probabilities, size = 1)
        count += 1
    return dice_sum, count


# In[10]:


# run statisitcal simulation to model 50000 times, and record the results into an array
sums_20 = np.empty(50000)
counts_20 = np.empty(50000)

for i in range(len(sums_20)):
    sums_20[i] = roll_dice(M = 20)[0]
    counts_20[i] = roll_dice(M = 20)[1]


# In[11]:


# calculate the mean of the sum minus M when M = 20
Q1_mean = np.mean(sums_20 - 20)


# In[12]:


print("the mean of the sum minus M when M = 20 is {:.5f}".format(Q1_mean))


# ##### 2. What is the mean of the number of rolls when M=20?

# In[13]:


# calculate the mean of the number of rolls when M=20?
Q2_number = np.mean(counts_20)


# In[14]:


print("the mean of the number of rolls when M=20 is {:.5f}".format(Q2_number))


# ##### 3. What is the standard deviation of the sum minus M when M=20?

# In[15]:


# calculate the standard deviation of the sum minus M when M=20
Q3_std = np.std(sums_20 - 20)


# In[16]:


print("the standard deviation of the sum minus M when M = 20 is {:.5f}".format(Q3_std))


# ##### 4. What is the mean of the sum minus M when M=5000?

# In[17]:


# run statisitcal simulation to model 50000 times, and record the results into an array
sums_5000 = np.empty(50000)
counts_5000 = np.empty(50000)

for i in range(len(sums_5000)):
    sums_5000[i] = roll_dice(M = 5000)[0]
    counts_5000[i] = roll_dice(M = 5000)[1]


# In[18]:


# calculate the mean of the sum minus M when M = 5000
Q4_mean = np.mean(sums_5000 - 5000)


# In[19]:


print("the mean of the sum minus M when M = 5000 is {:.5f}".format(Q4_mean))


# ##### 5. What is the mean of the number of rolls when M=5000?

# In[22]:


# calculate the mean of the number of rolls when M=5000?
Q5_number = np.mean(counts_5000)


# In[23]:


print("the mean of the number of rolls when M=5000 is {:.5f}".format(Q5_number))


# ##### 6. What is the standard deviation of the sum minus M when M=5000?

# In[24]:


# calculate the standard deviation of the sum minus M when M=5000
Q6_std = np.std(sums_5000 - 5000)


# In[25]:


print("the standard deviation of the sum minus M when M = 5000 is {:.5f}".format(Q6_std))


# In[ ]:




