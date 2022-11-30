# 라이브러리 호출
import matplotlib.pyplot as plt    # 시각화를 위한 matplotlib.pyplot 모듈 불러오기
from sklearn.cluster import KMeans    # k-means 모듈 불러오기
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os
import numpy as np
from PIL import Image


targerdir = r"/Users/endless/deeplab-pytorch/labels"  # 해당 폴더 설정


# os.listdir(): 인자 내부에 있는 파일만 출력, 폴더라면 출력 안함
files = os.listdir(targerdir)


# 지원하는 파일 형태의 확장자들
format = [".jpg", ".png", ".jpeg", "bmp", ".JPG",
          ".PNG", "JPEG", "BMP"]


# os.walk(): 하위의 폴더들을 for문으로 탐색할 수 있게 해줌.
# 인자로 전달된 path에 대해서 path, dirs(path 아래 폴더), files(path 아래 파일)을 tuple로 넘겨줌.

for (path, dirs, files) in os.walk(targerdir):
    for file in files:
        if file.endswith(tuple(format)):
            image = Image.open(path + "/" + file)
            print(image.filename)
            print(image.size)

            if image.mode != 'RGB':
                image = image.convert('RGB')
                print("RGB 모드가 아닌 이미지(=마스크 안된 이미지) 를 변환!")
                # 'L'은 흑백버전인데 RGB가 색상 더 잘 잡을 거 같아서 일단 RGB

            image = image.resize((400, 400))
            image.save("/Users/endless/deeplab-pytorch/clusterlabel/" + file)
            # image.save(file)

            print(image.size)

        else:
            print(path)
            print("InValid", file)


# 변환할 이미지 목록 불러오기
image_path = "/Users/endless/deeplab-pytorch/clusterlabel/"


img_list = os.listdir(image_path)  # 디렉토리 내 모든 파일 불러오기
img_list_jpg = [img for img in img_list if img.endswith(
    ".png")]  # 지정된 확장자만 필터링

print("img_list_png: {}".format(img_list_jpg))

img_list_np = []

for i in img_list_jpg:
    img = Image.open(image_path + i)
    img_array = np.array(img)
    print(img_array)  # 이미지 1차원 배열

    img_list_np.append(img_array)
    #print(i, " 추가 완료 - 구조:", img_array.shape)  # 불러온 이미지의 차원 확인 (세로X가로X색)
    #print(img_array.T.shape)  # 축변경 (색X가로X세로)계산상 전치행렬

img_np = np.array(img_list_np)  # 리스트를 numpy로 변환
np.save('./sample_data', img_np)  # x_save.npy
print(img_np.shape)  # 배열 크기 출력
print("결과: 정상적으로 저장 완료")


sample_data = np.load('sample_data.npy')
# fruits = np.load('fruits_300.npy')
# If M is (32 x 32 x 3), then .reshape(1,-1) will produce a 2d array (not 1d), of shape (1, 32*32*3).
# That can be reshaped back to (32,32,3) with the same sort of reshape statement.

sample_data_2d = sample_data.reshape(-1, 400*400*3)
# 배열 생성 reshape(-1, 정수) 일때, 행 자리에 -1, 그리고 열 위치에 임의의 정수가 있을 때 정수에 따라서 10개의 원소가 해당 열 개수만큼 자동으로 구조화


print("sample_data의 shape 맞추기:", sample_data)
print("sample_data_2d의 shape 맞추기:", sample_data_2d)

# 여기에서 출력되는 차원의 숫자가 같아야 한다.
print("sample_data.shape:", sample_data.shape)
print("sample_data_2d.shape:", sample_data_2d.shape)


# K값을 지정해 준다.random_state=항상 값은값이 랜덤하게 나온다.
km = KMeans(n_clusters = 6)  # random_state=42 -> 항상 랜덤값이 같게 하기위해 쓴다.
# 사이킷 런의 철학은 nxd, 갯수x차원
km.fit(sample_data_2d)
# 할당된 레이블의 결과를 볼 수 있다.
print("km.labels_", km.labels_)
print("km.labels_.shape", km.labels_.shape)
print("첫번째:", km.labels_[0:])
# print("두번째:", km.labels_[10:20])
# print("세번째:", km.labels_[20:30])

print(np.unique(km.labels_, return_counts=True))
print(km.labels_)


# #----------------------비슷한 구도 이미지끼리 묶어서 시각화---------------------#

def draw_sample_data(arr, ratio=1):
    n = len(arr)  # n은 샘플 개수입니다
    # 한 줄에 10개씩 이미지를 그립니다. 샘플 개수를 10으로 나누어 전체 행 개수를 계산합니다.
    print(n)
    rows = int(np.ceil(n / 10))
    # 행이 1개 이면 열 개수는 샘플 개수입니다. 그렇지 않으면 10개입니다.
    cols = n if rows < 2 else 10
    fig, axs = plt.subplots(rows, cols,
                            figsize=(cols * ratio, rows * ratio), squeeze=False)
    for i in range(rows):
        print(i)
        for j in range(cols):
            if i * 10 + j < n:  # n 개까지만 그립니다.
                print(i)
                axs[i, j].imshow(arr[i * 10 + j], cmap='gray_r')
            axs[i, j].axis('off')
    plt.show()


draw_sample_data(sample_data[km.labels_ == 0])
draw_sample_data(sample_data[km.labels_ == 1])
draw_sample_data(sample_data[km.labels_ == 2])
draw_sample_data(sample_data[km.labels_ == 3])
draw_sample_data(sample_data[km.labels_ == 4])
draw_sample_data(sample_data[km.labels_ == 5])

# #------------------------------적합한 k값 찾기-----------------------------#

# #----------------------실루엣 계수로 적합한 k값 찾기---------------------#
# def visualize_elbowmethod(data, param_init='random', param_n_init=5):
#     distortions = []
#     for i in range(1, 20):
#         km = KMeans(n_clusters=i, init=param_init, n_init=param_n_init)
#         km.fit(data)
#         distortions.append(km.inertia_)

#     plt.plot(range(1, 20), distortions, marker='o')
#     plt.xlabel('Number of Cluster')
#     plt.ylabel('Distortion')
#     plt.show()

# visualize_elbowmethod(sample_data_2d)
# #-------------------------------------------------------------------#


# #----------------------Inertia value로 적합한 k값 찾기---------------------#
# # Import Module


# # k-means clustering & inertia simulation
# ks = range(1, 20)   # 1~19개의 k로 클러스터링하기 위함
# inertias = []    # 응집도 결과 저장을 위한 빈 리스트 만들어 놓기
# for k in ks:
#     # n_init 숫자 클수록 계산량 증가하니까 grid search 단계에서는 작게 설정
#     model = KMeans(n_clusters=k, n_init=5)
#     # 'df'라는 이름의 dataset을 사용하여 모델 학습 & 학습에 소요되는 시간 측정
#     model.fit(sample_data_2d)
#     inertias.append(model.inertia_)    # 응집도 결과를 inertias 리스트에 계속 저장(추가)
#     print('n_cluster : {}, inertia : {}'.format(
#         k, model.inertia_))    # k 설정에 따른 결과 출력

# # Visualization
# plt.figure(figsize=(15, 6))
# plt.plot(ks, inertias, '-o')
# plt.xlabel('number of clusters, k')
# plt.ylabel('inertia')
# plt.xticks(ks)
# plt.show()
# #---------------------------------------------------------------------#