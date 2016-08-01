# coding=utf-8
import logging
from flask import render_template, redirect, url_for, flash, request, \
                  current_app, jsonify
from flask_login import login_required
from wtforms_components import read_only
from .. import db
from . import mang
from .forms import Add_Product, Add_Software, Add_Version, Add_Software2, Add_Feature
from ..models import Bugs, User, ProductInfo, VersionInfo, Attachment, \
      SoftWareInfo, FeatureInfo
from ..decorators import admin_required


dts_log = logging.getLogger('DTS')

@mang.route('/userlist', methods=['GET'])
@login_required
@admin_required
def user_manage():
    userlist = User.query.all()

    return render_template('mang/user_manage.html', userlist=userlist)


@mang.route('/set-user-forbidden/<string:user_id>', methods=['POST'])
@login_required
@admin_required
def user_forbidden_status_manage(user_id=None):
    # bugs_list = Bugs.query.filter_by(bug_owner=current_user).all()
    status  = request.form.get('manager')
    dts_log.debug(status)
    dts_log.debug(user_id)
    dts_log.debug(request.url)

    user = User.get_by_id(user_id)

    return jsonify({"status": user.set_forbidden_status(status)})


@mang.route('/productlist', methods=['GET', 'POST'])
@login_required
@admin_required
def productlist():
    product = ProductInfo.query.all()

    return render_template('mang/productlist.html', product=product)


@mang.route('/add-version/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_version(id):
    product = ProductInfo.query.get_or_404(id)
    version_list = VersionInfo.query.filter_by(product=product.id).all()
    software_list = SoftWareInfo.query.all()
    software = Add_Version()
    print software.errors
    print request.form.get('software_version')
    print request.form.getlist('software_version')
    print request.form.get('version_features')
    print request.form.getlist('version_features')
    if software.validate_on_submit():
        software_info = VersionInfo(
                            product=product.id,
                            version_name=software.version_name.data,
                            version_descrit=software.version_descrit.data)

        db.session.add(software_info)
        db.session.commit()
        flash('Softare 提交成功.')
        software_list = VersionInfo.query.filter_by(product=product.id).all()
        #return render_template('mang/add_softare.html', software=software,
        #                       version_list=version_list)
        return redirect(url_for('mang.add_version', id=product.id))
    software.product_name.data = product.product_name
    software.product_descrit.data = product.product_descrit

    read_only(software.product_name)
    read_only(software.product_descrit)

    return render_template(
                'mang/add_version.html',
                software=software, version_list=version_list,software_list=software_list)


@mang.route('/add-software/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_software(id):
    version = VersionInfo.query.filter_by(id=id).first()
    software = Add_Software2()
    print software.errors
    print request.form.get('software_version')
    print request.form.getlist('software_version')
    print request.form.get('version_features')
    print request.form.getlist('version_features')
    if software.validate_on_submit():
        software_info = SoftWareInfo(
                            version_id=version.id,
                            software_name=software.software_name.data,
                            software_descrit=software.software_descrit.data)
        db.session.add(software_info)
        db.session.commit()
        flash('Softare 提交成功.')

        return redirect(url_for('mang.add_version', id=id))
    software.product_name.data = version.version.product_name
    software.product_descrit.data = version.version.product_descrit
    software.version_name.data = version.version_name
    software.version_descrit.data = version.version_descrit

    read_only(software.product_name)
    read_only(software.product_descrit)
    read_only(software.version_name)
    read_only(software.version_descrit)
    return render_template('mang/add_software.html', software=software)


@mang.route('/add-feature/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_feature(id):
    version = VersionInfo.query.filter_by(id=id).first()
    feature = Add_Feature()
    if feature.validate_on_submit():
        feature_info = FeatureInfo(
                            version_id=version.id,
                            feature_name=feature.feature_name.data,
                            feature_descrit=feature.feature_descrit.data)
        db.session.add(feature_info)
        db.session.commit()
        flash('Softare 提交成功.')

        return redirect(url_for('mang.add_version', id=id))
    feature.product_name.data = version.version.product_name
    feature.product_descrit.data = version.version.product_descrit
    feature.version_name.data = version.version_name
    feature.version_descrit.data = version.version_descrit

    read_only(feature.product_name)
    read_only(feature.product_descrit)
    read_only(feature.version_name)
    read_only(feature.version_descrit)
    return render_template('mang/add_feature.html', feature=feature)


@mang.route('/add-product', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    add_product = Add_Software()
    if add_product.validate_on_submit():
        product_info = ProductInfo(
                            product_name=add_product.product_name.data,
                            product_descrit=add_product.product_descrit.data,
                            product_status=add_product.product_status.data)

        db.session.add(product_info)
        db.session.commit()

        software_info = VersionInfo(
                            product=product_info.id,
                            version_name=add_product.version_name.data,
                            version_descrit=add_product.version_descrit.data,
                            software_version=add_product.software_version.data,
                            version_features=add_product.version_features.data)
        db.session.add(software_info)
        db.session.commit()
        flash('增加产品和版本成功.')
        return redirect(url_for('mang.add_software', id=product_info.id))
    return render_template('mang/add_product.html', add_product=add_product)


@mang.route('/product-edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def product_edit(id):
    product = ProductInfo.query.get_or_404(id)
    add_product = Add_Product()
    if add_product.validate_on_submit():

        product.product_name = add_product.product_name.data
        product.product_descrit = add_product.product_descrit.data
        product.product_status = add_product.product_status.data
        db.session.add(product)
        db.session.commit()
        flash('产品信息更新成功.')
        # return render_template('mang/add_product.html',
        # add_product=add_product)
        return redirect(url_for('mang.productlist'))

    add_product.product_name.data = product.product_name
    add_product.product_descrit.data = product.product_descrit
    # add_product.product_status.data = product.product_status
    add_product.product_status.checked = '0'
    return render_template('mang/add_product.html', add_product=add_product)


@mang.route('/product-manage/<int:id>', methods=['POST'])
@login_required
@admin_required
def product_manage(id):
    product = ProductInfo.query.get_or_404(id)
    status  = request.form.get('manager')
    dts_log.debug(status)
    dts_log.debug(request.url)

    return jsonify({"status": product.set_status(status)})



@mang.route('/bug-manager')
@mang.route('/bug-manager/<string:product>')
@login_required
@admin_required
def bug_manage(product=None):
    # bugs_list = Bugs.query.filter_by(bug_owner=current_user).all()
    page     = request.args.get('page', 1, type=int)
    version  = request.args.get('version')
    software = request.args.get('software')
    status   = request.args.get('status')
    author   = request.args.get('author')

    dts_log.debug(product)
    dts_log.debug(request.url)
    dts_log.debug(request.url_root)
    dts_log.debug(request.base_url)

    bugs_list = Bugs.query

    if product:
        bugs_list = bugs_list.filter(Bugs.product_name == product)

    if version:
        bugs_list = bugs_list.filter(Bugs.product_version == version)

    if software:
        bugs_list = bugs_list.filter(Bugs.software_version == software)

    if status:
        st = BugStatus.query.filter_by(bug_status_descrit=status).first()
        bugs_list = bugs_list.filter_by(now_status = st)

    if author:
        au = User.query.filter_by(username=author).first()
        bugs_list = bugs_list.filter_by(author = au)

    pagination = bugs_list.order_by(Bugs.timestamp.desc()).paginate(
                 page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)

    bugs_list = pagination.items

    return render_template('mang/bug_manage.html', bugs_list=bugs_list,
                                                pagination=pagination)


@mang.route('/bug-delete/<string:bug_id>', methods=['POST'])
@login_required
@admin_required
def bug_delete(bug_id=None):
    # bugs_list = Bugs.query.filter_by(bug_owner=current_user).all()
    status  = request.form.get('manager')
    dts_log.debug(status)
    dts_log.debug(request.url)

    bug = Bugs.get_by_bug_id(bug_id)

    return jsonify({"status": bug.bug_delete()})


@mang.route('/set-bug-forbidden/<string:bug_id>', methods=['POST'])
@login_required
@admin_required
def bug_forbidden_status_manage(bug_id=None):
    # bugs_list = Bugs.query.filter_by(bug_owner=current_user).all()
    status  = request.form.get('manager')
    dts_log.debug(status)
    dts_log.debug(request.url)

    bug = Bugs.get_by_bug_id(bug_id)

    return jsonify({"status": bug.set_running_manage(status)})


@mang.route('/bug-attach')
@login_required
@admin_required
def bug_attach():
    page = request.args.get('page', 1, type=int)

    pagination = Attachment.query.order_by(
                    Attachment.uploadTime.desc()).paginate(
                    page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out=False)

    attach_list = pagination.items

    return render_template('mang/attach_manger.html', attach_list=attach_list,
                                                pagination=pagination)

@mang.route('/bug-attach-non')
@login_required
@admin_required
def bug_attach_no_bug_id():
    page = request.args.get('page', 1, type=int)
    '''
    pagination = Attachment.query.order_by(
                    Attachment.uploadTime.desc()).paginate(
                    page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out=False)

    pagination = Attachment.query.join(Bugs, Attachment.bug_id == Bugs.bug_id).filter(
                    Attachment.bug_id == None).order_by(
                    Attachment.uploadTime.desc()).paginate(
                    page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out=False)'''
    attach_list = db.session.execute("select * from attachment where attachment.bug_id not in (select bug_id from bugs);").fetchall()

    #attach_list = pagination.items

    return render_template('mang/attach_manger.html', attach_list=attach_list)