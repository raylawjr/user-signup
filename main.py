#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi
user_re = "^[a-zA-Z0-9_-]{3,20}$"
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)
def valid_password(password):
    return PASS_RE.match(password)
def valid_email(email):
    return EMAIL_RE.match(email)
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a>Signup</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

#username, password, verify password, e-mail(optional)
content = page_header + page_footer
class Index(webapp2.RequestHandler):
    def get(self):
        user_fields = '''
        <form action ="/submit_fields" method="post">
            <label>
            Username <input type="text" name="username"/><br>
            Password <input type="password" name="password"/><br>
            Verify Password <input type="password" name="verify_password"/><br>
            E-Mail (optional) <input type="text" name="e-mail"/>
            </label>
            <br><input type="submit" value = "Submit"/>
        </form>
        '''
        error = self.request.get("error")
        if error:
            error_element = (
            "<p class='error'>" + cgi.escape(error, quote=True) + "</p>")
        else:
            error_element = ""
        content = page_header + user_fields + error_element + page_footer
        self.response.write(content)

class Submit_Fields(webapp2.RequestHandler):
    def post(self):
        username_input = self.request.get("username")
        password_input = self.request.get("password")
        password_verify = self.request.get("verify_password")
        email_input = self.request.get("e-mail")
        error_content = """
        <form action ="/submit_fields" method="post">
            <label>
            Username <input type="text" name="username" value ='"""+username_input+"""'/><br>
            Password <input type="password" name="password"/><br>
            Verify Password <input type="password" name="verify_password"/><br>
            E-Mail (optional) <input type="text" name="e-mail" value='"""+email_input+"""'/>
            </label>
            <input type="submit" value = "Submit"/>
        </form>
        """
        if username_input == "":
            error = "<span style=color:red> Please fill out this form.</span>"
            self.response.write(page_header+"""
            <form action ="/submit_fields" method="post">
                <label>
                Username <input type="text" name="username" value ='"""+username_input+"""'/>"""+error+"""<br>
                Password <input type="password" name="password"/><br>
                Verify Password <input type="password" name="verify_password"/><br>
                E-Mail (optional) <input type="text" name="e-mail" value='"""+email_input+"""'/>
                </label>
                <br><input type="submit" value = "Submit"/>
            </form>
            """)
        elif password_input == "":
            error = "<span style=color:red>Please fill out this form.</span>"
            self.response.write(page_header+"""<form action ="/submit_fields" method="post">
                <label>
                Username <input type="text" name="username" value ='"""+username_input+"""'/><br>
                Password <input type="password" name="password"/>"""+error+"""<br>
                Verify Password <input type="password" name="verify_password"/><br>
                E-Mail (optional) <input type="text" name="e-mail" value='"""+email_input+"""'/>
                </label>
                <br><input type="submit" value = "Submit"/>
            </form>
            """)
        elif password_input != password_verify:
            error = "<span style=color:red>Your passwords did not match.</span>"
            self.response.write(page_header+"""
            <form action ="/submit_fields" method="post">
                <label>
                Username <input type="text" name="username" value ='"""+username_input+"""'/><br>
                Password <input type="password" name="password"/><br>
                Verify Password <input type="password" name="verify_password"/>"""+error+"""<br>
                E-Mail (optional) <input type="text" name="e-mail" value='"""+email_input+"""'/>
                </label>
                <br><input type="submit" value = "Submit"/>
            </form>
            """)
        elif not valid_username(username_input):
            error = "<span style=color:red>That is not a valid username.</span>"
            self.response.write(page_header+"""
            <form action ="/submit_fields" method="post">
                <label>
                Username <input type="text" name="username" value ='"""+username_input+"""'/>"""+error+"""<br>
                Password <input type="password" name="password"/><br>
                Verify Password <input type="password" name="verify_password"/><br>
                E-Mail (optional) <input type="text" name="e-mail" value='"""+email_input+"""'/>
                </label>
                <br><input type="submit" value = "Submit"/>
            </form>
            """)
        elif not valid_password(password_input):
            error = "<span style=color:red>That is not a valid password.</span>"
            self.response.write(page_header+"""
            <form action ="/submit_fields" method="post">
                <label>
                Username <input type="text" name="username" value ='"""+username_input+"""'/><br>
                Password <input type="password" name="password"/>"""+error+"""<br>
                Verify Password <input type="password" name="verify_password"/><br>
                E-Mail (optional) <input type="text" name="e-mail" value='"""+email_input+"""'/>
                </label>
                <br><input type="submit" value = "Submit"/>
            </form>
            """)
        elif not valid_email(email_input):
            error = "<span style=color:red>That is not a valid email.</span>"
            self.response.write(page_header+"""
            <form action ="/submit_fields" method="post">
                <label>
                Username <input type="text" name="username" value ='"""+username_input+"""'/><br>
                Password <input type="password" name="password"/><br>
                Verify Password <input type="password" name="verify_password"/><br>
                E-Mail (optional) <input type="text" name="e-mail" value='"""+email_input+"""'/>"""+error+"""
                </label>
                <br><input type="submit" value = "Submit"/>
            </form>
            """)


        #for i in username_input:
        #    for x in user_re:
        #        if i == x:
        #            error = "That's not a valid username."
        #            self.redirect("/?error="+error)
        else:
            good_username = cgi.escape(username_input, quote=True)
            sentence = "Welcome, "+good_username+"!"
            content = page_header+"<p>"+sentence+"</p>"+page_footer
            self.response.write(content)
app = webapp2.WSGIApplication([
    ('/', Index),
    ('/submit_fields', Submit_Fields)
], debug=True)
