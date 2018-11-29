# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request
from lib.log import get_logger
from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param
from service.category_service import CategoryService
from service.tag_service import TagService

menu_service = Blueprint('menu_service', __name__)

logger = get_logger('main')

# 导航接口
@menu_service.route('/category/list', methods=['POST'])
def list_category():
    res  = {'code' : 1000, 'msg' : '成功'}
    service = CategoryService()
    try:
        result = service.get_categorys()
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|category request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


# 拉取游戏的标签
@menu_service.route('/tags/content/list', methods=['POST'])
def get_tags():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get('data')
    if not data:
        return handle_param_error()

    user_id    = data.get("userid") or 0
    type_id    = data.get("type_id") or 'all'

    if not type_id:
        return handle_param_error()

    service = TagService()
    try:
        result = service.get_tag_by_content(type_id)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|tag list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


@menu_service.route('/tag/game/all', methods=['POST'])
def get_all_game():
    res  = {'code' : 1000, 'msg' : '成功'}
    service = TagService()
    try:
        result = service.get_all_content()
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|game list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res
