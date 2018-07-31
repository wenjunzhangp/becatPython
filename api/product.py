#!/usr/bin/evn python
# coding=utf-8

import json
from bottle import get, put, post, delete
from common import web_helper, db_helper, convert_helper, json_helper, string_helper


@get('/api/product/')
def callback():
    """
    获取列表数据
    """
    # 设置查询条件
    wheres = ''
    # 产品分类id
    product_class_id = convert_helper.to_int0(web_helper.get_query('product_class_id', '产品分类id', is_check_null=False))
    if product_class_id > 0:
        wheres = 'where product_class_id=' + str(product_class_id)
    # 页面索引
    page_number = convert_helper.to_int1(web_helper.get_query('page', '', is_check_null=False))
    # 页面显示记录数量
    page_size = convert_helper.to_int0(web_helper.get_query('rows', '', is_check_null=False))
    # 排序字段
    sidx = web_helper.get_query('sidx', '', is_check_null=False)
    # 顺序还是倒序排序
    sord = web_helper.get_query('sord', '', is_check_null=False)
    # 初始化排序字段
    order_by = 'id desc'
    if sidx:
        order_by = sidx + ' ' + sord
    # 类型
    type = web_helper.get_query('type', '类型', is_check_null=False)
    # 判断是否是前台提交获取数据
    if type != 'backstage':
        # 判断是否已经存在查询条件了，是的话在原查询条件后面拼接
        if wheres:
            wheres = wheres + ' and is_enable=1'
        else:
            wheres = 'where is_enable=1'

    #############################################################
    # 初始化输出格式（前端使用jqgrid列表，需要指定输出格式）
    data = {
        'records': 0,
        'total': 0,
        'page': 1,
        'rows': [],
    }
    #############################################################
    # 执行sql，获取指定条件的记录总数量
    sql = 'select count(1) as records from product %(wheres)s' % {'wheres': wheres}
    result = db_helper.read(sql)
    # 如果查询失败或不存在指定条件记录，则直接返回初始值
    if not result or result[0]['records'] == 0:
        return data
    # 保存总记录数量
    data['records'] = result[0].get('records', 0)

    #############################################################
    ### 设置分页索引与页面大小 ###
    # 设置分页大小
    if page_size is None or page_size <= 0:
        page_size = 10
    # 计算总页数
    if data['records'] % page_size == 0:
        page_total = data['records'] // page_size
    else:
        page_total = data['records'] // page_size + 1
    # 记录总页面数量
    data['total'] = page_total

    # 判断提交的页码是否超出范围
    if page_number < 1 or page_number > page_total:
        page_number = page_total
    # 记录当前页面索引值
    data['page'] = page_number

    # 计算当前页面要显示的记录起始位置
    record_number = (page_number - 1) * page_size
    # 设置查询分页条件
    paging = ' limit ' + str(page_size) + ' offset ' + str(record_number)
    ### 设置排序 ###
    if not order_by:
        order_by = 'id desc'
    #############################################################

    # 组合sql查询语句
    sql = "select * from product %(wheres)s order by %(orderby)s %(paging)s" % \
           {'wheres': wheres, 'orderby': order_by, 'paging': paging}
    # 读取记录
    result = db_helper.read(sql)
    if result:
        # 存储记录
        data['rows'] = result

    if data:
        # 直接输出json
        return web_helper.return_raise(json.dumps(data, cls=json_helper.CJsonEncoder))
    else:
        return web_helper.return_msg(-1, "查询失败")


@get('/api/product/<id:int>/')
def callback(id):
    """
    获取指定记录
    """
    sql = """select * from product where id = %s""" % (id,)
    # 读取记录
    result = db_helper.read(sql)
    if result:
        # 直接输出json
        return web_helper.return_msg(0, '成功', result[0])
    else:
        return web_helper.return_msg(-1, "查询失败")


@post('/api/product/')
def callback():
    """
    新增记录
    """
    name = web_helper.get_form('name', '产品名称')
    code = web_helper.get_form('code', '产品编码')
    product_class_id = convert_helper.to_int0(web_helper.get_form('product_class_id', '产品分类'))
    standard = web_helper.get_form('standard', '产品规格')
    quality_guarantee_period = web_helper.get_form('quality_guarantee_period', '保质期')
    place_of_origin = web_helper.get_form('place_of_origin', '产地')
    front_cover_img = web_helper.get_form('front_cover_img', '封面图片')
    content = web_helper.get_form('content', '产品描述', is_check_special_char=False)
    # 防sql注入攻击处理
    content = string_helper.filter_str(content, "'")
    # 防xss攻击处理
    content = string_helper.clear_xss(content)
    is_enable = convert_helper.to_int0(web_helper.get_form('is_enable', '是否启用'))

    # 添加记录（使用returning这个函数能返回指定的字段值，这里要求返回新添加记录的自增id值）
    sql = """insert into product (name, code, product_class_id, standard, quality_guarantee_period,
                place_of_origin, front_cover_img, content, is_enable)
              values (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning id"""
    vars = (name, code, product_class_id, standard, quality_guarantee_period, place_of_origin, front_cover_img, content, is_enable)
    # 写入数据库
    result = db_helper.write(sql, vars)
    # 判断是否提交成功
    if result and result[0].get('id'):
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, "提交失败")


@put('/api/product/<id:int>/')
def callback(id):
    """
    修改记录
    """

    name = web_helper.get_form('name', '产品名称')
    code = web_helper.get_form('code', '产品编码')
    product_class_id = convert_helper.to_int0(web_helper.get_form('product_class_id', '产品分类'))
    standard = web_helper.get_form('standard', '产品规格')
    quality_guarantee_period = web_helper.get_form('quality_guarantee_period', '保质期')
    place_of_origin = web_helper.get_form('place_of_origin', '产地')
    front_cover_img = web_helper.get_form('front_cover_img', '封面图片')
    content = web_helper.get_form('content', '产品描述', is_check_special_char=False)
    # 防sql注入攻击处理
    content = string_helper.filter_str(content, "'")
    # 防xss攻击处理
    content = string_helper.clear_xss(content)
    is_enable = convert_helper.to_int0(web_helper.get_form('is_enable', '是否启用'))

    # 编辑记录
    sql = """
          update product
            set name=%s, code=%s, product_class_id=%s, standard=%s, quality_guarantee_period=%s,
                place_of_origin=%s, front_cover_img=%s, content=%s, is_enable=%s
          where id=%s returning id"""
    vars = (name, code, product_class_id, standard, quality_guarantee_period, place_of_origin, front_cover_img, content,
            is_enable, id)
    # 写入数据库
    result = db_helper.write(sql, vars)
    # 判断是否提交成功
    if result and result[0].get('id'):
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, "提交失败")


@delete('/api/product/<id:int>/')
def callback(id):
    """
    删除指定记录
    """
    # 编辑记录
    sql = """delete from product where id=%s returning id"""
    vars = (id,)
    # 写入数据库
    result = db_helper.write(sql, vars)
    # 判断是否提交成功
    if result:
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, "删除失败")
