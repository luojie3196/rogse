#!/usr/bin/python
# encoding:utf-8
import os
from django.utils.encoding import smart_str
from django.http import FileResponse
import xlwt
import time


def merge_to_list(generator):
    p_list = []
    for p in generator:
        for n in p.split('/'):
            p_list.append(n.replace(' ', ''))
    p_list = list(set(p_list))
    return p_list

M_TYPES = ['爱情', '喜剧', '剧情', '动画', '科幻', '动作', '经典',
           '悬疑', '青春', '犯罪', '惊悚', '文艺', '搞笑', '纪录片',
           '励志', '恐怖', '战争', '短片', '黑色幽默', '魔幻', '传记',
           '情色', '感人', '暴力', '家庭', '音乐', '动画短片', '童年',
           '浪漫', '女性', '黑帮', '同志', '史诗', '烂片', '童话', '西部']

REGIONS = ['美国', '日本', '香港', '英国', '中国', '韩国', '法国',
           '台湾', '中国大陆', '德国', '意大利', '印度', '内地',
           '泰国', '西班牙', '欧洲', '加拿大', '澳大利亚', '俄罗斯',
           '伊朗', '瑞典', '爱尔兰', '巴西', '丹麦', '波兰', '捷克',
           '阿根廷', '比利时', '墨西哥', '新西兰', '荷兰', '奥地利',
           '土耳其', '匈牙利', '以色列', '瑞士']


def file_download(file_name_path):
    file_name = os.path.basename(file_name_path)
    path_to_file = os.path.dirname(file_name_path)
    response = FileResponse(open(file_name_path, 'rb'),
                            content_type='application/octet-stream')
    # mimetype is replaced by content_type for django 1.7
    response['Content-Disposition'] = 'attachment; filename="%s"' % smart_str(file_name)
    response['X-Sendfile'] = smart_str(path_to_file)
    response['Content-Length'] = os.path.getsize(file_name_path)
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response


def generate_xls(list_object, start_index, end_index):
    export_list = list_object[(int(start_index) - 1):int(end_index)]
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    today_date = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    borders.bottom_colour = 0x3A
    style0 = xlwt.easyxf('font: name Times New Roman, color-index 4, bold on', num_format_str='#,##0.00')
    style0.borders = borders
    style1 = xlwt.XFStyle()
    style1.borders = borders
    # Add first head line
    fields_list = ['No.', '电影名称', 'ID', '评分', '电影链接', '封面链接', '导演',
                   '编剧', '主演', '类型', '地区', '语言', '上映时间', '集数', '时长',
                   '别名', 'IMDB链接', '网址', '评论数', '简介']
    for n in range(len(fields_list)):
        sheet.write(0, n, fields_list[n], style0)
    i = 1
    for movie in export_list:
        sheet.write(i, 0, i, style1)
        sheet.write(i, 1, movie.title, style1)
        sheet.write(i, 2, movie.movie_id, style1)
        sheet.write(i, 3, movie.rate, style1)
        sheet.write(i, 4, movie.url, style1)
        sheet.write(i, 5, movie.cover, style1)
        sheet.write(i, 6, movie.director, style1)
        sheet.write(i, 7, movie.scriptwriter, style1)
        sheet.write(i, 8, movie.protagonist, style1)
        sheet.write(i, 9, movie.m_type, style1)
        sheet.write(i, 10, movie.region, style1)
        sheet.write(i, 11, movie.language, style1)
        sheet.write(i, 12, movie.release_time, style1)
        sheet.write(i, 13, movie.numbers, style1)
        sheet.write(i, 14, movie.run_time, style1)
        sheet.write(i, 15, movie.other_title, style1)
        sheet.write(i, 16, movie.imdb_link, style1)
        sheet.write(i, 17, movie.website, style1)
        sheet.write(i, 18, movie.comment_num, style1)
        sheet.write(i, 19, movie.summary, style1)
        i += 1
    file_name_path = os.path.join(os.environ['TMP'], 'movie_list_' + str(today_date)+'.xls')
    # file_name_path = 'movie_list_' + str(today_date)+'.xls'
    wbk.save(file_name_path)
    return file_name_path

