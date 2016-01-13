#coding=utf-8
from flask import render_template, redirect, request, url_for, flash, \
    current_app, jsonify
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from wtforms_components import read_only
from .. import db
from . import mang
from .forms import Add_Product, Add_Software
from ..models import Bugs, User, Process, BugStatus, ProductInfo, VersionInfo


@mang.route('/productlist', methods=['GET', 'POST'])
@login_required
def productlist():
    product = ProductInfo.query.all()

    return render_template('mang/productlist.html', product=product)

@mang.route('/add-software/<int:id>', methods=['GET', 'POST'])
@login_required
def add_software(id):
    product = ProductInfo.query.get_or_404(id)

    software = Add_Software()
    if software.validate_on_submit():
        software_info = VersionInfo(product_id=product.product_id,
                                    version_name=software.version_name.data,
                                    version_descrit=software.version_descrit.data,
                                    software_version=software.software_version.data)

        db.session.add(software_info)
        db.session.commit()
        flash('Softare 提交成功.')
        return render_template('mang/add_softare.html', software=software)
    software.product_name.data = product.product_name
    software.product_descrit.data = product.product_descrit

    read_only(software.product_name)
    read_only(software.product_descrit)
    return render_template('mang/add_softare.html', software=software)

@mang.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    add_product = Add_Product()
    if add_product.validate_on_submit():
        product_info = ProductInfo(product_name=add_product.product_name.data,
                                   product_descrit=add_product.product_descrit.data)

        db.session.add(product_info)
        db.session.commit()
        flash('Bugs 提交成功.')
        return render_template('mang/add_product.html', add_product=add_product)
    return render_template('mang/add_product.html', add_product=add_product)


@mang.route('/product-edit/<int:id>', methods=['GET', 'POST'])
@login_required
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
        #return render_template('mang/add_product.html', add_product=add_product)
        return redirect(url_for('mang.productlist'))

    add_product.product_name.data = product.product_name
    add_product.product_descrit.data = product.product_descrit
    #add_product.product_status.data = product.product_status
    add_product.product_status.checked = '0'
    return render_template('mang/add_product.html', add_product=add_product)
