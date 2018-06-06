# -*- coding: utf-8 -*-
import pymysql
from pygraph.classes.digraph import digraph

class PRIterator:
    __doc__ = '''计算一张图中的PR值'''

    def __init__(self, dg):
        self.damping_factor = 0.85  # 阻尼系数,即α
        self.max_iterations = 100  # 最大迭代次数
        self.min_delta = 0.00001  # 确定迭代是否结束的参数,即ϵ
        self.graph = dg

    def page_rank(self):
        #  先将图中没有出链的节点改为对所有节点都有出链
        for node in self.graph.nodes():
            if len(self.graph.neighbors(node)) == 0:
                for node2 in self.graph.nodes():
                    digraph.add_edge(self.graph, (node, node2))

        nodes = self.graph.nodes()
        graph_size = len(nodes)
        if graph_size == 0:
            return {}
        page_rank = dict.fromkeys(nodes, 1.0 / graph_size)  # 给每个节点赋予初始的PR值
        damping_value = (1.0 - self.damping_factor) / graph_size  # 公式中的(1−α)/N部分

        flag = False
        for i in range(self.max_iterations):
            change = 0
            for node in nodes:
                rank = 0
                for incident_page in self.graph.incidents(node):  # 遍历所有“入射”的页面
                    rank += self.damping_factor * (page_rank[incident_page] / len(self.graph.neighbors(incident_page)))
                rank += damping_value
                change += abs(page_rank[node] - rank)  # 绝对值
                page_rank[node] = rank

            print("This is NO.%s iteration" % (i + 1))
            print(page_rank)

            if change < self.min_delta:
                flag = True
                break
        if flag:
            print("finished in %s iterations!" % node)
        else:
            print("finished out of 100 iterations!")
        return page_rank


if 1:
    dg = digraph()
    db = pymysql.connect("localhost", "root", "root", "zhihu", charset='utf8')
    cursor = db.cursor()
    # 删除多余节点
    url_links = []
    sql = "delete from url_link where url or link not in (select url from get_title)"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    #获取url顶点
    urls = []
    sql = "select distinct url from get_url"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for var in results:
            urls.append(var[0])
        print(urls)
        db.commit()
    except:
        db.rollback()
    #获取边Link
    url_links = []
    sql = "select url,link from url_link"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for var in results:
            url_links.append(var)
        print(url_links)
        db.commit()
    except:
        db.rollback()
    dg.add_nodes(urls)
    for var in url_links:
        dg.add_edge(var)
    pr = PRIterator(dg)
    page_ranks = pr.page_rank()
    print("The final page rank is\n", page_ranks)
    for key,val in page_ranks.items():
        sql = "UPDATE get_title SET score = "+ str(val) +" where url='"+key+"'";
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    db.close()