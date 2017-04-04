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


region_list = {
    '阿富汗': 'Afghanistan',
    '安哥拉': 'Angola',
    '阿尔巴尼亚': 'Albania',
    '阿联酋': 'United Arab Emirates',
    '阿根廷': 'Argentina',
    '亚美尼亚': 'Armenia',
    '澳大利亚': 'Australia',
    '澳洲': 'Australia',
    '奥地利': 'Austria',
    '阿塞拜疆': 'Azerbaijan',
    '布隆迪': 'Burundi',
    '比利时': 'Belgium',
    '比利時': 'Belgium',
    '贝宁': 'Benin',
    '布基纳法索': 'Burkina Faso',
    '孟加拉': 'Bangladesh',
    '保加利亚': 'Bulgaria',
    '玻利维亚': 'Bolivia',
    '巴西': 'Brazil',
    '文莱': 'Brunei',
    '博茨瓦纳': 'Botswana',
    '中非': 'Central African Republic',
    '加拿大': 'Canada',
    '瑞士': 'Switzerland',
    '智利': 'Chile',
    '中国': 'China',
    '香港': 'China',
    '澳门': 'China',
    '澳門': 'China',
    '台湾': 'China',
    '台灣': 'China',
    '大陆': 'China',
    '上海方言': 'China',
    '喀麦隆': 'Cameroon',
    '刚果': 'Republic of the Congo',
    '哥伦比亚': 'Colombia',
    '哥斯达黎加': 'Costa Rica',
    '古巴': 'Cuba',
    '塞浦路斯': 'Cyprus',
    '捷克': 'Czech Republic',
    '德国': 'Germany',
    '德國': 'Germany',
    '西德': 'Germany',
    '东德': 'Germany',
    '丹麦': 'Denmark',
    '多米尼加共和国': 'Dominican Republic',
    '阿尔及利亚': 'Algeria',
    '厄瓜多尔': 'Ecuador',
    '埃及': 'Egypt',
    '西班牙': 'Spain',
    '爱沙尼亚': 'Estonia',
    '埃塞俄比亚': 'Ethiopia',
    '芬兰': 'Finland',
    '芬蘭': 'Finland',
    '斐济': 'Fiji',
    '法国': 'France',
    '加蓬': 'Gabon',
    '英国': 'United Kingdom',
    '英國': 'United Kingdom',
    'UK': 'United Kingdom',
    '格鲁吉亚': 'Georgia',
    '加纳': 'Ghana',
    '几内亚': 'Guinea',
    '希腊': 'Greece',
    '危地马拉': 'Guatemala',
    '洪都拉斯': 'Honduras',
    '匈牙利': 'Hungary',
    '印度尼西亚': 'Indonesia',
    '印度': 'India',
    '爱尔兰': 'Ireland',
    '伊朗': 'Iran',
    '伊拉克': 'Iraq',
    '冰岛': 'Iceland',
    '以色列': 'Israel',
    '意大利': 'Italy',
    '牙买加': 'Jamaica',
    '约旦': 'Jordan',
    '日本': 'Japan',
    '哈萨克': 'Kazakhstan',
    '吉尔吉斯坦': 'Kyrgyzstan',
    '柬埔寨': 'Cambodia',
    '韩国': 'South Korea',
    '科威特': 'Kuwait',
    '老挝': 'Laos',
    '黎巴嫩': 'Lebanon',
    '利比里亚': 'Liberia',
    '利比亚': 'Libya',
    '斯里兰卡': 'Sri Lanka',
    '立陶宛': 'Lithuania',
    '卢森堡': 'Luxembourg',
    '拉脱维亚': 'Latvia',
    '摩洛哥': 'Morocco',
    '摩尔多瓦': 'Moldova',
    '马达加斯加': 'Madagascar',
    '墨西哥': 'Mexico',
    '马里': 'Mali',
    '缅甸': 'Myanmar',
    '蒙古': 'Mongolia',
    '莫桑比克': 'Mozambique',
    '马拉维': 'Malawi',
    '马来西亚': 'Malaysia',
    '纳米比亚': 'Namibia',
    '尼日尔': 'Niger',
    '尼日利亚': 'Nigeria',
    '尼加拉瓜': 'Nicaragua',
    '荷兰': 'Netherlands',
    '挪威': 'Norway',
    '尼泊尔': 'Nepal',
    '新西兰': 'New Zealand',
    '紐西蘭': 'New Zealand',
    'NewZealand': 'New Zealand',
    '阿曼': 'Oman',
    '巴基斯坦': 'Pakistan',
    '巴拿马': 'Panama',
    '秘鲁': 'Peru',
    '菲律宾': 'Philippines',
    '巴布亚新几内亚': 'Papua New Guinea',
    '波兰': 'Poland',
    '朝鲜': 'North Korea',
    '葡萄牙': 'Portugal',
    '巴拉圭': 'Paraguay',
    '卡塔尔': 'Qatar',
    '罗马尼亚': 'Romania',
    '俄罗斯': 'Russia',
    '苏联': 'Russia',
    '沙特阿拉伯': 'Saudi Arabia',
    '苏丹': 'Sudan',
    '塞内加尔': 'Senegal',
    '索马里': 'Somalia',
    '斯洛伐克': 'Slovakia',
    '斯洛文尼亚': 'Slovenia',
    '瑞典': 'Sweden',
    '斯威士兰': 'Swaziland',
    '叙利亚': 'Syria',
    '乍得': 'Chad',
    '多哥': 'Togo',
    '泰国': 'Thailand',
    '塔吉克斯坦': 'Tajikistan',
    '土库曼': 'Turkmenistan',
    '突尼斯': 'Tunisia',
    '土耳其': 'Turkey',
    '坦桑尼亚': 'United Republic of Tanzania',
    '乌干达': 'Uganda',
    '乌克兰': 'Ukraine',
    '烏克蘭': 'Ukraine',
    '乌拉圭': 'Uruguay',
    '美国': 'United States of America',
    'USA': 'United States of America',
    '美國': 'United States of America',
    'America': 'United States of America',
    'UnitedStatesUSA': 'United States of America',
    '乌兹别克': 'Uzbekistan',
    '委内瑞拉': 'Venezuela',
    '也门': 'Yemen',
    '南非': 'South Africa',
    '赞比亚': 'Zambia',
    '津巴布韦': 'Zimbabwe',
}


def generate_map_data(movie_data):
    region_count = {}
    for movie in movie_data:
        for k, v in region_list.items():
            if k in movie.region or v.lower() in movie.region.lower():
                if v not in region_count:
                    region_count[v] = 0
                region_count[v] += 1
    map_data = []
    for name, value in region_count.items():
        map_data.append({'name': name, 'value': value})
    return str(map_data).replace('\'name\'', 'name').replace('\'value\'', 'value')

