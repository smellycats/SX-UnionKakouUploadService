# -*- coding: utf-8 -*-


class Config(object):
    # 密码 string
    SECRET_KEY = 'jintiandalaohu'
    # 服务器名称
    HEADER_SERVER = 'SX-UnionKakouDataServer'
    # 加密次数 int
    ROUNDS = 123456
    # token生存周期，默认2小时 int
    EXPIRES = 7200
    # 数据库连接 string
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../hbc.db'
    # 数据库连接绑定 dict
    SQLALCHEMY_BINDS = {
        'kakou': 'postgresql://vms:123@123.123.123.123:54320/vmsDB'
    }
    # 连接池大小 int
    #SQLALCHEMY_POOL_SIZE = 10
    # 布控字典 dict
    BKCP_DICT = {}


class Develop(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False


class Testing(Config):
    TESTING = True
