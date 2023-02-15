# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2022/12/31
# @File : pagination.py
"""
自定义分页组件的使用，需要做以下几件事

在视图函数中：
    def pretty_list(request):
        data_dict = {}
        # 0. 如果有条件搜索，先找出条件
        search_data = request.GET.get('q', '')

        if search_data:
            data_dict["mobile__contains"] = search_data

        # 1.根据自己的条件进行筛选数据
        queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')

        # 2.实例化分页对象
        page_object = Pagination(request, queryset=queryset, search_data=search_data)


        context = {
            "search_data": search_data,
            "queryset": page_object.page_queryset,  #分完页的数据
            "page_string": page_object.html() # 生成页码
        }

        return render(request, 'pretty_list.html', context)

在html页面中：
    循环取数据
        {% for obj in queryset %}
    页码展示：
         <div class="clearfix">
            <ul class="pagination">
                {{ page_string }}
            </ul>
        </div>
"""


from math import ceil

from django.utils.safestring import mark_safe


class Pagination:
    def __init__(self, request, queryset, search_data, page_size=10, page_param='page', plus=5):
        """
        :param request:
        :param queryset:
        :param page_size:
        :param page_param:
        :param plus:
        """
        page = request.GET.get(page_param, '1')
        self.search_data = search_data

        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()
        # print(total_count)
        self.total_page_count = ceil(total_count / page_size)
        # print(self.total_page_count)

        self.plus = plus

    def html(self):
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库数据较少，没有达到11页
            start_page = 1
            end_page = self.total_page_count + 1
        else:
            # 当前页<5
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页 > 5
                # 当前页 +5 > 总页面
                if self.page >= self.total_page_count - 5:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []

        # 首页
        page_str_list.append('<li> <a href="?q={}&page={}"> 首页 </a> </li>'.format(self.search_data, 1))

        # 上一页
        if self.page == 1:
            page_str_list.append('<li> <a href="?q={}&page={}"> 上一页 </a> </li>'.format(self.search_data, 1))
        else:
            page_str_list.append('<li> <a href="?q={}&page={}"> 上一页 </a> </li>'.format(self.search_data, self.page - 1))

        # 中间页面
        for i in range(start_page, end_page):
            if i == self.page:
                ele = '<li class="active"> <a href="?q={}&page={}"> {} </a> </li>'.format(self.search_data, i, i)
            else:
                ele = '<li> <a href="?q={}&page={}"> {} </a> </li>'.format(self.search_data, i, i)
            page_str_list.append(ele)

        # 下一页
        if self.page == self.total_page_count:
            page_str_list.append(
                '<li> <a href="?q={}&page={}"> 下一页 </a> </li>'.format(self.search_data, self.total_page_count))
        else:
            page_str_list.append('<li> <a href="?q={}&page={}"> 下一页 </a> </li>'.format(self.search_data, self.page + 1))

        # 尾页
        page_str_list.append(
            '<li> <a href="?q={}&page={}"> 尾页 </a> </li>'.format(self.search_data, self.total_page_count))

        page_string = mark_safe("".join(page_str_list))

        return page_string
