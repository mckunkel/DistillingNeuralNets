'''
Gets downloads a list of URLs for the names stored in "animals",
then calls a bash script to do the actual downloading
'''
import re, sys, os, subprocess
#import urllib
if sys.version_info[0] >= 3:
    import urllib.request as urllib
else:
    # Not Python 3 - today, it is most likely to be Python 2
    # But note that this might need an update when Python 4
    # might be around one day
    import urllib


class_names = sys.argv[1:]
print(class_names)

def new_dir(p):
    if not os.path.exists(p):
        os.makedirs(p)

for folder in ["data","features/teacher","features/student"]:
    for case in ["train","test"]:
        for name in class_names:
            path = "{}/{}/{}".format(folder,case,name)
            new_dir(path)
new_dir("models")

max_images = {"train":100,"test":50}

def get_wnid(name):
    wnid_data = open("index.noun","r").read()
    str1 = r'^q .*$'
    str2 = re.sub('q',name,str1)
    hits = re.findall(str2,wnid_data,re.MULTILINE)
    print(hits)
    assert len(hits)==1
    ids = re.findall(r'[\d]{8,8}',hits[0])
    wnid = 'n'+ids[0]
    print(wnid)
    return wnid

def get_urls(wnid,name):
    save_path = "URL_lists/{}_URLs".format(name)
    if not os.path.exists(save_path):
        new_dir("URL_lists")
        image_locations_url="http://image-net.org/api/text/imagenet.synset.geturls?wnid="+wnid
        urllib.urlretrieve(image_locations_url,save_path)

    urls = open(save_path,"r").readlines()
    urls = [re.sub("\n","",u) for u in urls]
    urls = [re.sub("\r","",u) for u in urls]
    return urls

for name in class_names:
    wnid = get_wnid(name)
    urls = get_urls(wnid,name)
    url_gen = (url for url in urls)
    for case in ["train","test"]:
        print("Downloading {} {} images".format(name,case))
        for i in range(max_images[case]):
            url = next(url_gen)
            save_path="data/{}/{}/{}{:05d}.jpg".format(case,name,name,i)
            subprocess.call(["./Downloader.sh",url,save_path])



#if __name__ == '__main__':
#adding come comments to check if on dev or master