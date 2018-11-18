import numpy as np
def calc_hist(img):
    histogram = np.zeros((256))
    for i in range(len(img)):
        for j in range(img[0].size):
            histogram[img[j][i]] += 1
    return histogram

def find_max(arr):
    maximum = 0
    for i in range(len(arr)):
        if arr[i]>maximum:
            maximum = arr[i]
    return maximum

def hist_filter(img):
    histogram = calc_hist(img)
    if find_max(histogram) > 900:
        return 0
    sum=0
    for i in range(25):
        sum += histogram[i]
    if sum >= 1400:
        return 0
    i=1
    j=25
    while j<256:
        sum -= histogram[i-1]
        sum += histogram[j]
        i += 1
        j += 1
        if sum >= 1400:
            return 0
    sum = 0
    for i in range(50):
        sum += histogram[i]
    if sum >= 1850:
        return 0
    i = 1
    j = 50
    while j < 256:
        sum -= histogram[i - 1]
        sum += histogram[j]
        i += 1
        j += 1
        if sum >= 1850:
            return 0
    return 1