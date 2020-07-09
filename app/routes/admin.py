# -*- coding: utf-8 -*-
from flask import Blueprint

bp = Blueprint('admin', __name__)


@bp.route('/')
def index():
    return "Wellcome to admin VIZURO."


@bp.route('/config')
def config():
    return "Wellcome to admin VIZURO config."
