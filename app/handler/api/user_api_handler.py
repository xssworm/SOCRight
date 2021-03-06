#-*- encoding: utf-8 -*-

import tornado.web
#import tornado.escape
from datetime import datetime


import config
from common import state, redis_cache
from helper import str_helper
from handler import base_handler
from logic import usergroup_logic, user_logic

#{"code":0,"msg":"OK","data":{"id": 1, "tel": "123", "email": "treeyh@126.com", "name": "\u4f59\u6d77"}}
#{"code":0,"msg":"OK"}
#{"code":0,"msg":"OK","data":{"id": 1, "tel": "123", "email": "treeyh@126.com", "name": "\u4f59\u6d77", "rights": [{"id":12, "path":"xx.aa","right":1, "customRight": ",1,2,3,"}, {"id":13, "path":"xx.aa.bb","right":1, "customRight": ""}]}}
class UserGetInfoHandler(base_handler.BaseHandler):    
    def get(self):
        token = self.get_arg('token','')
        if '' == token:
            self.out_fail(code = 1001, msg = 'token')
            return
        user = redis_cache.getStr(token)
        if None == user:
            self.out_ok()
            return
        redis_cache.delete(token)
        self.out_ok(user)
        return
            
class UserByUserGroupHandler(base_handler.BaseHandler):    
    def get(self):
        userGroupID = int(self.get_arg('userGroupID','0'))
        if 0 == userGroupID:
            self.out_fail(code = 1001, msg = 'userGroupID')
            return

        json = usergroup_logic.query_users_by_user_group_cache(userGroupID = userGroupID)
        self.out_ok(data = json)
        return


class UserByUserNameHandler(base_handler.BaseHandler):    
    def get(self):
        userName = self.get_arg('userName','')
        if '' == userName:
            self.out_fail(code = 1001, msg = 'userName')
            return

        user = user_logic.query_user_by_name_cache(name = userName)
        if None == users:
            self.out_ok(data = '{}')
            return
        
        json = str_helper.json_encode(user)
        self.out_ok(data = json)
        return


class UsersByUserNamesHandler(base_handler.BaseHandler):    
    def get(self):
        names = self.get_arg('names','')
        if '' == names:
            self.out_fail(code = 1001, msg = 'names')
            return
        names = str_helper.format_str_to_list_filter_empty(names, ',')

        users = []
        for name in names:
            if str_helper.is_null_or_empty(name):
                continue
            user = user_logic.query_user_by_name_cache(name = name)    
            if None != user:
                users.append(user)
                
        json = str_helper.json_encode(users)
        self.out_ok(data = json)
        return
