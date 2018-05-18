# -*- coding: utf-8 -*-
import json
#from functools import wraps

import arrow
from flask import g, request, make_response, jsonify, abort

from . import db, app, cache, logger
from .models import *
from . import helper


@app.route('/', methods=['GET'])
def index_get():
    result = {
        'kakou_url': '{0}'.format(request.url_root)
    }
    header = {'Cache-Control': 'public, max-age=60, s-maxage=60'}
    return jsonify(result), 200, header


@cache.cached(timeout=60)
def flesh_bk_info():
    """刷新全局变量布控信息"""
    v = TrafficDispositionVehicle.query.filter_by(
        del_flag=0, identify=0, check_result='1', status='2').all()
    for i in v:
        app.config['BKCP_DICT'][i.plate_no] = {
            'disposition_type': i.disposition_type,
            'disposition_id': i.disposition_id,
            'disposition_reason': i.disposition_reason
        }
    return True


# 添加布控车牌
def set_bkcp(i):
    if i['hphm'] == '-' or i['hphm'] is None:
        return
    tsv = app.config['BKCP_DICT'].get(i['hphm'], None)
    if tsv is None:
        return
    fxbh = {u'IN': 9, u'OT': 10, u'WE': 2, u'EW': 1, u'SN': 3, u'NS': 4, 0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10}
    hpzl = helper.hphm2hpzl(i['hphm'], i['hpys_id'], i['hpzl'])

    sql = (u"insert into traffic_disposition_alarm(disposition_type, disposition_id, disposition_reason, crossing_id, lane_no, direction_index, pass_time, plate_no, plate_type, plate_color, vehicle_speed, image_path) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')".format(tsv['disposition_type'], tsv['disposition_id'], tsv['disposition_reason'], i['kkdd_id'], i['cdbh'], fxbh.get(i['fxbh'], 9), i['jgsj'], i['hphm'], hpzl, i['hpys_id'], i['clsd'], i['img_path']))
    query = db.get_engine(app, bind='kakou').execute(sql)
    query.close()


@cache.cached(timeout=60*5)
def flesh_white_info():
    """刷新全局变量布控信息"""
    r = set()
    v = TrafficSpecialVehicle.query.filter_by().all()
    for i in v:
        r.add((i.plate_no, int(i.plate_color)))
    app.config['WHITE_SET'] = r
    return True


# 判断是否白名单车辆
def set_spcp(i):
    if i['hphm'] == '-' or i['hphm'] is None:
        return
    try:
        if (i['hphm'], i['hpys_id']) in app.config['WHITE_SET']:
            fxbh = {'IN': 9, 'OT': 10, 'WE': 2, 'EW': 1, 'SN': 3, 'NS': 4, 0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10}
            hpzl = helper.hphm2hpzl(i['hphm'], i['hpys_id'], i['hpzl'])
            sql = ("insert into traffic_privilegevehicle_pass(crossing_id, lane_no, direction_index, plate_no, plate_type, pass_time, plate_color, image_path, vehicle_color, vehicle_type, vehicle_speed) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(i['kkdd_id'], i['cdbh'], fxbh.get(i['fxbh'], 9), i['hphm'], hpzl, i['jgsj'], i['hpys_id'], i['img_path'], 0, 0, i['clsd']))
            query = db.get_engine(app, bind='kakou').execute(sql)
            query.close()
    except Exception as e:
        pass


@app.route('/', methods=['POST'])
def kakou_post():
    if not request.json:
        return jsonify({'message': 'Problems parsing JSON'}), 415
    fxbh = {'IN': 9, 'OT': 10, 'WE': 2, 'EW': 1, 'SN': 3, 'NS': 4, 0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10}
    try:
        flesh_bk_info()
        flesh_white_info()
        # 正常车辆数据
        vals = []
        for i in request.json:
            if i['kkdd_id'] is None:
                continue
            elif len(i['kkdd_id']) < 9:
                continue
            hpzl = helper.hphm2hpzl(i['hphm'], i['hpys_id'], i['hpzl'])

            vals.append("('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(
                i['kkdd_id'], i['cdbh'], fxbh.get(i['fxbh'], 9), i['hphm'], hpzl, i['jgsj'], i['hpys_id'], i['img_path'], 0, 0, i['clsd']))
            set_bkcp(i)
            set_spcp(i)
        if len(vals) > 0:
            sql = ("insert into traffic_vehicle_pass(crossing_id, lane_no, direction_index, plate_no, plate_type, pass_time, plate_color, image_path, vehicle_color, vehicle_type, vehicle_speed) VALUES %s" % ','.join(vals))
            query = db.get_engine(app, bind='kakou').execute(sql)
            query.close()
    except Exception as e:
        logger.error('request.json')
        logger.error(request.json)
        logger.exception(e)
        raise
    
    return jsonify({'total': len(request.json)}), 201

