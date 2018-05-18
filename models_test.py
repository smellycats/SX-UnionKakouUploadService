# -*- coding: utf-8 -*-
import arrow

from app import app, db
from app.models import *
from app.helper import *


def test_scope_get():
    scope = Scope.query.all()
    for i in scope:
        print i.name

def test_user_get():
    user = Users.query.filter_by(username='admin', banned=0).first()
    print user.scope
    
def test_traffic_get():
    r = Traffic.query.first()
    #help(r)
    print r
    #print type(r.pass_time)
    #print r.crossing_id

def test_traffic_add():
    t_list = []
    for i in range(3):
        t = Traffic(crossing_id='441302123', lane_no=1, direction_index='IN',
                    plate_no=u'粤L12345', plate_type='',
                    pass_time='2015-12-13 01:23:45', plate_color='0')
        db.session.add(t)
        t_list.append(t)
    help(db.session.__call__)
    #db.session.commit()
    #r = [{'pass_id': r.pass_id} for r in t_list]
    #print r

def test_traffic_add2():
    vals = [
	u"('441302123', 1, 'IN', '粤L12345', '', '2015-12-13 01:23:45', '0')",
	u"('441302123', 1, 'IN', '粤L12345', '', '2015-12-13 01:23:45', '0')"
    ]
    #print ','.join(vals)
    sql = ("insert into traffic(crossing_id, lane_no, direction_index, plate_no, plate_type, pass_time, plate_color) values %s") % ','.join(vals)
    query = db.get_engine(app, bind='kakou').execute(sql)
    query.close()

def test_user_test():
    u = UserTest.query.all()
    for i in u:
	print i

def test_user_add():
    # u = UserTest(name='fire')
    #db.session.add(u)
    #db.session.commit()
    name = 'fire'
    sql = ("insert into test_user(name) values('%s'),('feizi')") % name
    query = db.get_engine(app, bind='kakou').execute(sql)
    sql2 = ("insert into test_user(name) values('huojian'),('maci')")
    query = db.get_engine(app, bind='kakou').execute(sql2)
    query.close()

def test_get_alarm():
    hphm = u'粤L54321'
    sql = ("select plate_no, plate_color, disposition_start_time, disposition_stop_time from traffic_disposition_vehicle where plate_no='%s'" % hphm)
    query = db.get_engine(app, bind='kakou').execute(sql)
    r = query.fetchone()
    print r
    query.close()

def test_get_alarm2():
    hphm = u'粤L543212'
    t = TrafficDispositionVehicle.query.filter_by(plate_no=hphm).first()
    print t
    print type(t.disposition_start_time)

def get_special_vehicle():
    r = set()
    t = TrafficSpecialVehicle.query.filter_by().all()
    for i in t:
	r.add((i.plate_no, int(i.plate_color)))
    return r

if __name__ == '__main__':
    #hpys_test()
    #hbc_add()
    #test_scope_get()
    #test_user_get()
    #test_hbc_get()
    #test_hbc_add()
    #test_hbcimg_get()
    #test_kkdd()
    #test_traffic_get()
    #test_traffic_add2()
    #test_user_test()
    #test_user_add()
    #test_get_alarm()
    #test_get_alarm2()
    print get_special_vehicle()


