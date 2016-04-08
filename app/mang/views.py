# coding=utf-8
from flask import render_template, redirect, url_for, flash
from flask.ext.login import login_required
from wtforms_components import read_only
from .. import db
from . import mang
from .forms import Add_Product, Add_Software
from ..models import ProductInfo, VersionInfo
from ..decorators import admin_required


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
    if software.validate_on_submit():
        software_info = VersionInfo(
                            product=product.id,
                            version_name=software.version_name.data,
                            version_descrit=software.version_descrit.data,
                            software_version=software.software_version.data,
                            version_features=add_product.version_features.data)

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
