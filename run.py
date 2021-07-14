import requests
from bs4 import BeautifulSoup
import os
import re

def main(url,fname="default"): # must be in the format of https://m.weibo.cn/detail/xxxxxxx"
    #check format
    pattern = re.compile("https://m.weibo.cn/detail/[0-9]+")
    if not pattern.match(url):
        print("invalid string, should match the format of https://m.weibo.cn/detail/xxxxxxx")
        return
    video_link = getDownloadLink(url)
    videoname = GetResource(video_link,fname)
    print(videoname)

    



def getDownloadLink(weiboUrl):
    r = requests.get(weiboUrl)
    soup = BeautifulSoup(r.text,"html.parser")
    script_text = soup.find_all('script')[1]
    all_video_links = re.findall('(https://f\.video.*?\,video)', script_text.string)
    def find_area(string):
        n = re.search('template=(.*?)\.25',string)
        text = n.group(1)
        text_list = text.split("x")
        area = float(text_list[0])*float(text_list[1])
        return area
    maximum_hd_link = sorted(all_video_links,key = lambda string: find_area(string),reverse=True)[0]
    
    return maximum_hd_link

    
    

def GetResource(videoUrl,fname="default",extension = '.mp4'):
    print('start downloading')
    mp4_file = requests.get(videoUrl)     #获取文件

    root = os.getcwd()
    path=root+"/resource"                #资源存放目录
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    checkFileName = os.path.exists(path+"/"+fname+extension)
    
    while checkFileName:
        nums = re.compile(r"\(([0-9]*)\)")
        check = nums.search(fname)
        if check:
            include_pre = check.group(0)
            number_only = check.group(1)
            inc = int(number_only)+1
            fname = fname.replace(include_pre,"("+str(inc)+")")
        else:
            fname = fname + "(1)"
        checkFileName = os.path.exists(path+"/"+fname+extension)
    videoname = root + '/resource/' + fname + extension
    with open(videoname, 'wb') as f:
        f.write(mp4_file.content)
    print("finished downloading"+videoname)
    return videoname

if __name__ == "__main__":
    with open("url.txt","r") as f:
        lines = [i.strip("\n") for i in f.readlines()]
        urls = [line.split(",")[0] for line in lines]
        fnames = [line.split(",")[1] for line in lines]


    for i in range(len(lines)):
        main(urls[i],fnames[i])