# Download dataset, took around 4 minutes for me
# 'https://www.mvtec.com/company/research/datasets/mvtec-screws'
import requests, tarfile, os

url = "https://osf.io/ruca6/download"
tarname = "mvtec_screws_v1.0.tar.gz"
if not os.path.isfile(tarname):
    print("Data archive downloading...")
    r = requests.get(url, stream=True)
    with open(tarname, "wb") as fd:
        fd.write(r.content)
    print("Download completed.")

# unpack tar datafile
datapath = "screwdata"
if not os.path.exists(datapath):
    with tarfile.open(tarname) as tar:
        tar.extractall(datapath)
    os.remove(tarname)

# Some json files and a folder full of images
print(os.listdir(datapath))

# There's some details in the readme
with open("screwdata/README_v1.0.txt") as f:
    file_contents = f.read()
    print(file_contents)
