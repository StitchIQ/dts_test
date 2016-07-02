# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import logging

from flask import render_template, request, current_app, jsonify, make_response
from flask.ext.login import login_required, current_user

from ..models import Bugs, User, Process, BugStatus, Permission, \
    Bug_Now_Status, ProductInfo, VersionInfo, Attachment
from .. import db , dts_mongodb


from . import reports


dts_log = logging.getLogger('DTS')

# TODO URL不再使用
@reports.route('/dailycharts', methods=['GET'])
@login_required
def dailycharts():
    return render_template('reports/dailycharts.html')


@reports.route('/bugsversioncharts', methods=['GET'])
@login_required
def bugsversioncharts():
    product = ProductInfo.get_all_product()
    version = VersionInfo.query.all()

    return render_template('reports/versionreports.html', product=product,
                            version=version)


@reports.route('/dailydatas', methods=['GET'])
@login_required
def dailydatas():
    # daily_bugs2 = Bugs.query.with_entities(db.func.strftime(
    #        '%Y.%m.%d',Bugs.timestamp).label('date'),
    # db.func.count(Bugs.id).label('total')).group_by(db.func.strftime(
    #       '%Y.%m.%d',Bugs.timestamp).label('date')).all()

    daily_bugs = Bugs.query.with_entities(
                    db.func.date(Bugs.timestamp).label('date'),
                    db.func.count(Bugs.bug_id).label('total')).group_by(
                    db.func.date(Bugs.timestamp).label('date')).all()

    # ss = db.session.execute("select strftime('%Y.%m.%d',timestamp)
    # as date,count(id) as total from bugs GROUP BY
    # strftime('%Y.%m.%d',timestamp)")

    return jsonify({
        'name': "Bugs数",
        'type': "bar",
        'data': [s.total for s in daily_bugs],
        'date': [str(s.date) for s in daily_bugs]
        })


@reports.route('/productcharts', methods=['GET'])
@login_required
def productcharts():
    # product = ProductInfo.query.all()
    product = ProductInfo.get_all_product()

    return render_template('reports/productcharts.html', product=product)



@reports.route('/versiondatas', methods=['GET'])
@login_required
def versiondatas():
    version = request.args.get('product')
    # print prd
    daily_bugs = Bugs.query.with_entities(
        db.func.date(Bugs.timestamp).label('date'),
        db.func.count(Bugs.bug_id).label('total')).filter(
        Bugs.product_version == version).group_by(
        db.func.date(Bugs.timestamp).label('date')).all()

    return jsonify({
        'name': "Bugs",
        'type': "bar",
        'data': [s.total for s in daily_bugs],
        'date': [str(s.date) for s in daily_bugs]
        })


@reports.route('/bugtodaydatas', methods=['GET'])
@login_required
def bugtodaydatas():
    # TODO 今日新增问题
    # daily_bugs2 = Bugs.query.with_entities(db.func.strftime(
    #        '%Y.%m.%d',Bugs.timestamp).label('date'),
    # db.func.count(Bugs.id).label('total')).group_by(db.func.strftime(
    #       '%Y.%m.%d',Bugs.timestamp).label('date')).all()
    version = request.args.get('product')
    # 查询当天新增的问题单
    daily_bugs = db.session.query(
                    db.func.date(Bugs.timestamp).label('date'),
                    db.func.count(Bugs.bug_id).label('total')).filter(
                    db.func.date(Bugs.timestamp)==db.func.date('now','localtime')).filter(
                    Bugs.product_version == version).group_by(
                    db.func.date(Bugs.timestamp)).all()
    # ss = db.session.execute("select strftime('%Y.%m.%d',timestamp)
    # as date,count(id) as total from bugs GROUP BY
    # strftime('%Y.%m.%d',timestamp)")

    return jsonify({
        'name': "Bugs数",
        'type': "bar",
        'data': [s.total for s in daily_bugs],
        'date': [s.date for s in daily_bugs]
        })

@reports.route('/bugdailydatas', methods=['GET'])
@login_required
def bugdailydatas():
    product = request.args.get('product')
    version = request.args.get('version')
    dts_log.debug(product)
    dts_log.debug(version)
    # print prd
    daily_bugs = Bugs.query.with_entities(
        db.func.date(Bugs.timestamp).label('date'),
        db.func.count(Bugs.bug_id).label('total')).filter(
        Bugs.product_name == product)

    if version:
        daily_bugs = daily_bugs.filter(Bugs.product_version == version)

    daily_bugs = daily_bugs.group_by(
                        db.func.date(Bugs.timestamp)).all()
    #daily = db.session.execute("select count(bug_id) as total , DATE_FORMAT(timestamp,'%y-%m-%d') as dd from bugs group by dd;").fetchall()

    return jsonify({
        'name': "Bugs",
        'type': "bar",
        'dataY': [s.total for s in daily_bugs],
        'dataX': [str(s.date) for s in daily_bugs],
        })

@reports.route('/softwarebugdatas', methods=['GET'])
@login_required
def softwarebugdatas():
    product = request.args.get('product')
    version = request.args.get('version')
    # print prd
    daily_bugs = Bugs.query.with_entities(
        Bugs.software_version.label('software'),
        db.func.count(Bugs.bug_id).label('total')).filter(
        Bugs.product_name == product)

    if version:
        daily_bugs = daily_bugs.filter(Bugs.product_version == version)

    daily_bugs = daily_bugs.group_by(
                    Bugs.software_version.label('software')).all()

    return jsonify({
        'name': "Bugs",
        'type': "bar",
        'dataY': [s.total for s in daily_bugs],
        'dataX': [s.software for s in daily_bugs]
        })


@reports.route('/featuresbugdatas', methods=['GET'])
@login_required
def featuresbugdatas():
    product = request.args.get('product')
    version = request.args.get('version')
    # print prd
    daily_bugs = Bugs.query.with_entities(
        Bugs.version_features.label('features'),
        db.func.count(Bugs.bug_id).label('total')).filter(
        Bugs.product_name == product)

    if version:
        daily_bugs = daily_bugs.filter(Bugs.product_version == version)

    daily_bugs = daily_bugs.group_by(
                    Bugs.version_features.label('features')).all()
    return jsonify({
        'name': "Bugs",
        'type': "bar",
        'dataY': [s.total for s in daily_bugs],
        'dataX': [s.features for s in daily_bugs]
        })

@reports.route('/seriousbugdatas', methods=['GET'])
@login_required
def seriousbugdatas():
    product = request.args.get('product')
    version = request.args.get('version')
    # print prd
    daily_bugs = Bugs.query.with_entities(
        Bugs.bug_level.label('level'),
        db.func.count(Bugs.bug_id).label('total')).filter(
        Bugs.product_name == product)

    if version:
        daily_bugs = daily_bugs.filter(Bugs.product_version == version)

    daily_bugs = daily_bugs.group_by(
                    Bugs.bug_level.label('level')).all()

    return jsonify({
        'name': "Bugs",
        'type': "bar",
        'dataY': [s.total for s in daily_bugs],
        'dataX': [s.level for s in daily_bugs]
        })

@reports.route('/statusbugdatas', methods=['GET'])
@login_required
def statusbugdatas():
    product = request.args.get('product')
    version = request.args.get('version')
    # print prd
    daily_bugs = db.session.query(
                db.func.count(Bugs.bug_id).label('total'),
                BugStatus.bug_status_descrit.label('status')).filter(
                Bugs.product_name == product)

    if version:
        daily_bugs = daily_bugs.filter(Bugs.product_version == version)

    daily_bugs = daily_bugs.filter(
                Bugs.bug_status == BugStatus.bug_status).group_by(
                Bugs.bug_status).all()

    return jsonify({
        'name': "Bugs",
        'type': "bar",
        'dataY': [s.total for s in daily_bugs],
        'dataX': [s.status for s in daily_bugs]
        })


@reports.route('/authorbugsdatas', methods=['GET'])
@login_required
def authorbugsdatas():
    product = request.args.get('product')
    version = request.args.get('version')

    daily_bugs = db.session.query(db.func.count(Bugs.id).label('total'),
                                  User.username.label('status')).filter(
                                  Bugs.product_name == product)

    if version:
        daily_bugs = daily_bugs.filter(Bugs.product_version == version)

    daily_bugs = daily_bugs.filter(Bugs.author_id == User.id).group_by(
                                  Bugs.author_id).all()
    return jsonify({
        'name': "Bugs",
        'type': "bar",
        'dataY': [s.total for s in daily_bugs],
        'dataX': [s.status for s in daily_bugs]
        })


@reports.route('/seriousdataspie', methods=['GET'])
@login_required
def seriousdataspie():
    prd = request.args.get('product')
    daily_bugs = Bugs.query.with_entities(
                    Bugs.bug_level.label('level'),
                    db.func.count(Bugs.bug_id).label('total')).filter(
                    Bugs.product_name == prd).group_by(
                    Bugs.bug_level.label('level')).all()

    data = [{"value": s.total, "name": s.level} for s in daily_bugs]

    return jsonify({
        'name': "Bugs",
        'type': "bar",
        'data': data,
        'level': [s.level for s in daily_bugs]
        })


@reports.route('/statusdatas', methods=['GET'])
@login_required
def statusdatas():
    prd = request.args.get('product')

    # dd = db.session.query(db.func.count(Bugs.id).label('total'),
    # BugStatus.bug_status_descrit.label('status'))
    # ss = dd.join(BugStatus, BugStatus.bug_status==Bugs.bug_status).filter(
    # Bugs.product_name==prd).group_by(Bugs.bug_status).all()
    daily_bugs = db.session.query(
                db.func.count(Bugs.bug_id).label('total'),
                BugStatus.bug_status_descrit.label('status')).filter(
                Bugs.product_name == prd).filter(
                Bugs.bug_status == BugStatus.bug_status).group_by(
                Bugs.bug_status).all()
    # print '44'*20
    # print str(daily_bugs)
    # print '44'*20

    # 直接使用sql语句查询的结果访问属性会失败，返回500的错误
    # daily_bugs = db.session.execute("SELECT bugstatus.bug_status_descrit as
    # bugs_bug_status, count(bugs.id) as total FROM bugs, bugstatus on
    # bugs.bug_status=bugstatus.bug_status WHERE bugs.product_name ='IPC'
    # GROUP BY bugstatus.bug_status")

    return jsonify({
        'name': "Bugs",
        'type': "bar",
        'data': [s.total for s in daily_bugs],
        'status': [s.status for s in daily_bugs]
        })
