# coding=utf-8
import logging
from flask import render_template, redirect, url_for, flash, request, current_app
from flask.ext.login import login_required
from wtforms_components import read_only
from .. import db
from . import mang
from .forms import Add_Product, Add_Software
from ..models import Bugs, User, ProductInfo, VersionInfo, Attachment
from ..decorators import admin_required


dts_log = logging.getLogger('DTS')

@mang.route('/productlist', methods=['GET', 'POST'])
@login_required
@admin_required
def productlist():
    product = ProductInfo.query.all()

    return render_template('mang/productlist.html', product=product)


@mang.route('/add-software/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_software(id):
    product = ProductInfo.query.get_or_404(id)
    software_list = VersionInfo.query.filter_by(product=product.id).all()
    software = Add_Software()
    print software.errors
    print request.form.get('software_version')
    print request.form.getlist('software_version')
    print request.form.get('version_features')
    print request.form.getlist('version_features')
    if software.validate_on_submit():
        software_info = VersionInfo(
                            product=product.id,
                            version_name=software.version_name.data,
                            version_descrit=software.version_descrit.data,
                            software_version=software.software_version.data,
                            version_features=software.version_features.data)

        db.session.add(software_info)
        db.session.commit()
        flash('Softare 提交成功.')
        software_list = VersionInfo.query.filter_by(product=product.id).all()
        return render_template('mang/add_softare.html', software=software,
                               software_list=software_list)
    software.product_name.data = product.product_name
    software.product_descrit.data = product.product_descrit

    read_only(software.product_name)
    read_only(software.product_descrit)
    # flash(software_list)
    return render_template(
                'mang/add_softare.html',
                software=software, software_list=software_list)


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



@mang.route('/bug-manger')
@mang.route('/bug-manger/<string:product>')
@login_required
@admin_required
def bug_manger(product=None):
    # bugs_list = Bugs.query.filter_by(bug_owner=current_user).all()
    page     = request.args.get('page', 1, type=int)
    version  = request.args.get('version')
    software = request.args.get('software')
    date     = request.args.get('date')
    features = request.args.get('features')
    serious  = request.args.get('serious')
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

    if date:
        bugs_list = bugs_list.filter(db.func.date(Bugs.timestamp)== date)

    if features:
        bugs_list = bugs_list.filter(Bugs.version_features == features)

    if serious:
        bugs_list = bugs_list.filter(Bugs.bug_level == serious)

    if status:
        st = BugStatus.query.filter_by(bug_status_descrit=status).first()
        bugs_list = bugs_list.filter_by(now_status = st)

    if author:
        au = User.query.filter_by(username=author).first()
        bugs_list = bugs_list.filter_by(author = au)

    pagination = bugs_list.order_by(Bugs.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)

    bugs_list = pagination.items

    return render_template('mang/bugmang.html', bugs_list=bugs_list,
                                                pagination=pagination)



@mang.route('/bug-attach')
@login_required
@admin_required
def bug_attach():
    # bugs_list = Bugs.query.filter_by(bug_owner=current_user).all()
    page     = request.args.get('page', 1, type=int)


    pagination = Attachment.query.order_by(
                    Attachment.uploadTime.desc()).paginate(
                    page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out=False)

    attach_list = pagination.items

    return render_template('mang/attach_manger.html', attach_list=attach_list,
                                                pagination=pagination)
