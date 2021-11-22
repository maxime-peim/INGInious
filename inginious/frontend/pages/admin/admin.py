# -*- coding: utf-8 -*-
#
# This file is part of INGInious. See the LICENSE and the COPYRIGHTS files for
# more information about the licensing of this file.

""" Admin index page"""
from flask import redirect, request,jsonify
from inginious.frontend.pages.utils import INGIniousAdministratorPage
import hashlib


class AdministrationUsersPage(INGIniousAdministratorPage):
    """User Admin page."""
    def GET_AUTH(self):  # pylint: disable=arguments-differ
        """ Display admin users page """
        return self.show_page()

    def POST_AUTH(self):  # pylint: disable=arguments-differ
        """ Display admin users page """
        return self.show_page()

    def show_page(self):
        """Display page"""
        all_users = self.user_manager.get_users()
        return self.template_helper.render("admin/admin_users.html", all_users=all_users)


class AdministrationUserActionPage(INGIniousAdministratorPage):
    """Action on User Admin page."""
    def POST(self):
        return self.POST_AUTH()

    def POST_AUTH(self):
        username = request.form.get("username")
        activate_hash = self.user_manager.get_user_activate_hash(username)
        action = request.form.get("action")
        if action == "activate":
            self.user_manager.activate_user(activate_hash)
        elif action == "delete":
            self.user_manager.delete_user(username)
        elif action == "get_bindings":
            user_info = self.user_manager.get_user_info(username)
            return jsonify(user_info.bindings)
        elif action == "revoke_binding":
            binding_id = request.form.get("binding_id")
            _, _ = self.user_manager.revoke_binding(username, binding_id)
        elif action == "add_user":
            realname = request.form.get("realname")
            email = request.form.get("email")
            password = request.form.get("password")
            feedback = self.user_manager.create_user({
                "username": username,
                "realname": realname,
                "email": email,
                "password": hashlib.sha512(password.encode("utf-8")).hexdigest(),
                "bindings": {},
                "language": "en"})
            if feedback:
                all_users = self.user_manager.get_users()
                return self.template_helper.render("admin/admin_users.html", all_users=all_users, feedback=feedback)
        return redirect("/administrator/users")
