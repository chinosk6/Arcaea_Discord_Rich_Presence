import PIL
from PIL import ImageEnhance
import pytesseract
import json
import sqlite3
import difflib
import re

ignore_list = ["cubesato","tama","Apollo program"]

def query_db(db_path, sql, para=""):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(sql, para)
    nb = cursor.fetchall()
    #connection.commit()
    cursor.close()
    connection.close()
    return(nb)

def get_text_right(s, f):
    '''
    原文本,查找文本
    '''
    l = s.rfind(f)
    return(s[l + len(f):])

def get_str_simi(str1, str2):
   return(difflib.SequenceMatcher(None, str1, str2).quick_ratio())

def get_diff(input):
    getlist = re.findall("\d+\+?", input)
    return(''.join(getlist))

def get_num_from_str(input):
    getlist = re.findall("\d+", input)
    return(''.join(getlist))

def ocr(filename, lang): #2日语
    im = PIL.Image.open(filename)
    iw = im.width
    ih = im.height
    im = im.crop((int(iw*0.75), 0, iw, int(ih*0.33)))
    im = ImageEnhance.Brightness(im).enhance(0.85)
    # 转化为8bit的黑白图片
    im = im.convert('L')
    # 二值化，采用阈值分割算法，threshold为分割点
    threshold = 140
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    im = im.point(table, '1')

    if(lang == '2'):
        result = pytesseract.image_to_string(im, lang="eng+jpn+chi_sim", config='')
    else:
        result = pytesseract.image_to_string(im, lang="eng", config='')
    result = result.split('\n')
    #print(result)
    return(result)


def get_info(tlist:list):
    songs = query_db("arcsong.db", "select `name_en`,`name_jp` from songs")
    #tlist = ['SCORE ~ ad', 'a', ': See een Beyond 11', '‘2 ses', 'aw Tempestissimo', 'NM Bf »', ', Whe if t+pazolite', '\x0c']
    difflist = ["Past", "Present", "Future", "Beyond"]
    diffstr = ''
    diff_flag = False #跳循环
    for d in difflist:
        diff_index = -1 #记录难度位置
        for g in tlist:
            diff_index += 1
            if(d in g):
                diff_flag = True
                diffstr = d
                diffnum = get_diff(get_text_right(g, d))
                try:
                    diffint = int(get_num_from_str(diffnum))
                    if(diffint <= 0 or diffint >= 12):
                        diffnum = ''
                except:
                    pass
                break
        if(diff_flag == True):
            break

    if(diffstr == ''): #未找到难度信息
        return("In Menu", "0")

    score = "0"
    for sc in tlist[:diff_index]:
        _sc = re.findall("[0-9]([0-9]{7})", sc)
        if(len(_sc) == 1):
            score = _sc[0]
            #print(score)
            break

    maxsimi = 0
    maxsimi_song = ''
    for sn in songs:
        for song in sn: #song-单曲名
            #print(song)
            if(song == ''):
                #print(114)
                continue
            for wd in tlist[diff_index + 1:]:
                pig = False
                for ig in ignore_list:
                    if(wd in ig):
                        pig = True
                        break
                if(pig == True):
                    continue
                s_now = get_str_simi(song, wd.replace(" ",'').replace("〇", "の"))
                if(s_now > maxsimi):
                    maxsimi = s_now
                    maxsimi_song = song

    #print(maxsimi_song, maxsimi)
    return(maxsimi_song + ' ' + diffstr + ' ' + diffnum, score)


def stat_identify(filename, lang):
    tlist = ocr(filename, lang)
    ret = get_info(tlist)
    return(ret)

#print(get_info())