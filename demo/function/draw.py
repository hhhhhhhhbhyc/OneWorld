# -*- coding: utf-8 -*-
"""
Created on Thu May 14 23:12:08 2020

@author: 黄奕辰
"""
# import webbrowser
import pyecharts.options as opts
from pyecharts.charts import Line

# """
# Gallery 使用 pyecharts 1.1.0
# 参考地址: https://www.echartsjs.com/examples/editor.html?c=line-marker
#
# 目前无法实现的功能:
#
# 1、最低气温的最高值暂时无法和 Echarts 的示例完全复刻
# """

dic_all={'day1':[3,14],'day2':[5,54],'day3':[0,5],'day4':[13,24],'day5':[13,4]}

public_num = []
match_num = []
day = list(dic_all.keys())
for i in list(dic_all.values()):
    public_num.append(i[0]) 
    match_num.append(i[1])


(
    Line(init_opts=opts.InitOpts(width="1000px", height="600px"))
    .add_xaxis(xaxis_data=day)
    .add_yaxis(
        series_name="发布数",
        y_axis= public_num,is_smooth=True,
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
            ]
        ),
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="average", name="平均值")]
        ),
        areastyle_opts=opts.AreaStyleOpts(opacity=0.4, color="#808000")
    )
    .add_yaxis(
        series_name="匹配数",
        y_axis=match_num,is_smooth=True,
        
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="average", name="平均值"),
                opts.MarkLineItem(symbol="none", x="90%", y="max"),
                opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
            ]
        ),
        areastyle_opts=opts.AreaStyleOpts(opacity=0.4, color="#6A5ACD")
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="个人中心数据统计", subtitle="发布＆匹配"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
    .render("day_public_match.html")
)
# webbrowser.open('day-public-match.html')