from PIL import Image
import numpy as np
import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


img = cv2.imread('/Users/endless/deeplab-pytorch/labels/0.png')
print(img.shape)

# 채널 순서 다름 : 채널을 BGR -> RGB로 변경
image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# image = image.reshape((image.shape[0] * image.shape[1], 3))
# # height, width 통합
print(image.shape)
# (25024, 3)

plt.imshow(image)
plt.show()

image = image[300:400, 200:300]
# image = cv2.cvtColor(re_img, cv2.COLOR_BGR2RGB)

plt.imshow(image)
plt.show()

# (25024, 3)
image = image.reshape((image.shape[0] * image.shape[1], 3))  # height, width 통합
print(image.shape)


k = 5  # 색깔 5개 kmean로

clt = KMeans(n_clusters=k)
clt.fit(image)

print("-------clustering된 컬러값------")
for center in clt.cluster_centers_:
    print(center)

print("------------------------------")


# 클러스터 개수의 영역에 얼마만큼의 퍼센테이지가 차지하고 있는지 return
def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist


hist = centroid_histogram(clt)
print(hist)

print("\n 이 사진의 모든 색상코드 : ")
colorlist = clt.cluster_centers_.astype("uint8").tolist()
dup = list(set(map(tuple, colorlist)))
print(dup)


def rgb_to_hex(list):
    r, g, b = int(list[0]), int(list[1]), int(list[2])
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)


def plot_colors(hist, centroids):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)

        if(max(hist) == percent):
            print("\n가장 큰 비율의 색깔코드 : ")
            print(rgb_to_hex(color.astype("uint8").tolist()))

        # if(max(percent)):
        #     print(color.astype("uint8").tolist())

        startX = endX

    # return the bar chart
    return bar


bar = plot_colors(hist, clt.cluster_centers_)


# show our color bart
plt.figure()
plt.axis("off")
plt.imshow(bar)
plt.show()