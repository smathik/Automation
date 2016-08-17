from bottle import run,debug,get,post,hook, response, request, route
import sys, paramiko, time, commands, pexpect, bottle, ldap, shutil,smtplib,os, os.path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def check_login(username, password):
  ldap_server="xxx"
  user_dn = "yyy"
  base_dn = "zzz"
  connect = ldap.open(ldap_server)
  search_filter = "cn="+username
  try:
    connect.bind_s(user_dn,password)
    result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
    connect.unbind_s()
    dump = "success"
    return True
  except ldap.LDAPError:
    connect.unbind_s()
    return False

@route('/login')
def login():
    return '''<html>
                <head>
                    <style>
                        body {
                            font-style: italic;
                            width: 50%;
                            margin: 0px auto;
                        }
                        #login_form {

                        }

                        #f1 {
                            background-color: #FFF;
                            border-style: solid;
                            border-width: 1px;
                            padding: 23px 1px 20px 114px;
                        }
                        .f1_label {
                            white-space: nowrap;
                        }
                        span {color: white;}

                        .new {
                            background: black;
                            text-align: center;
                        }
                    </style>
                </head>

                <body>
                    <div id="login_form">
                        <div class="new"><span>Enter  Credentials</span></div>
                        <form action="/login" method="post">
                            <table>
                                <tr>
                                    <td class="f1_label">User Name : e</td>
                                    <td><input name="username" type="text" />
                                    </td>
                                </tr>
                                <tr>
                                    <td class="f1_label">Password  :</td>
                                    <td><input name="password" type="password" />
                                    </td>
                                </tr>
                                <tr>
                                    <td>Please Select an option ! :</td>
                                    <td><input type="radio" name="options" id="user" value="user"> User Creation </input><br>
                                    <input type="radio" name="options" id="pass" value="pass"> Password reset </input><br>
                                    </td>
                                <tr>
                                    <td>
                                        <input type="submit" name="login" value="Log In" style="font-size:18px;"/>
                                    </td>
                                </tr>
                            </table>
                        </form>
                    </div>
                </body>
            </html>'''


@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    option = request.forms.get('options')
    if username and password:
      if check_login(username, password):
        if option is None:
          return "<p>Please Select an option.</p>"
        elif option.startswith("user"):
            return """  <html>
                              <head>
                              <style>
                              ul {
                                  list-style-type: none;
                                  margin: 0;
                                  padding: 0;
                                  overflow: hidden;
                                  background-color: #333;
                              }

                              li {
                                  float: left;
                              }

                              li a {
                                  display: block;
                                  color: white;
                                  text-align: center;
                                  padding: 14px 16px;
                                  text-decoration: none;
                              }

                              li a:hover {
                                  background-color: #111;
                              }


                              .searchsubmit {
                                  background-color: #555555;
                                  border: none;
                                  color: white;
                                  padding: 15px 32px;
                                  text-align: center;
                                  text-decoration: none;
                                  display: inline-block;
                                  font-size: 16px;
                                  float: right;
                                  height: 39px;
                              }

                              .searchform {
                                padding-left: 25px;
                                height: 39px;
                                float:middle
                              }

                              h1 {
                               font-family: verdana;
                              }

                              table {
                                  border-collapse: collapse;
                                  width: 100%;
                              }

                              th, td {
                                  text-align: left;
                                  padding: 8px;
                              }

                              tr:nth-child(even){background-color: #f2f2f2}

                              th {
                                  background-color: #4CAF50;
                                  color: white;
                              }

                              </style>
                              </head>
                              <body style="background-color:lightgrey;">
                              <form action="/user_management" method="post">

                              <ul>
                                <li><a class="active" >USER MANAGEMENT DASHBOARD</a></li>
                              </ul>
                                Users : <textarea id="users" name="users" rows="20" cols="20"></textarea>
                                Servers : <textarea id="servers" name="servers" rows="20" cols="20"></textarea>
                                Mirror id : <input type="text" id="mirror" name="mirror">
                                Request : <input type="text" id="request" name="request">
                                <input type="submit" value="Submit">
                              </form>
                              </body>
                              </html>
              """
        elif option.startswith("pass"):
         return """  <html>
                          <head>
                          <style>
                          ul {
                              list-style-type: none;
                              margin: 0;
                              padding: 0;
                              overflow: hidden;
                              background-color: #333;
                          }

                          li {
                                  float: left;
                              }

                              li a {
                                  display: block;
                                  color: white;
                                  text-align: center;
                                  padding: 14px 16px;
                                  text-decoration: none;
                              }

                              li a:hover {
                                  background-color: #111;
                              }


                              .searchsubmit {
                                  background-color: #555555;
                                  border: none;
                                  color: white;
                                  padding: 15px 32px;
                                  text-align: center;
                                  text-decoration: none;
                                  display: inline-block;
                                  font-size: 16px;
                                  float: right;
                                  height: 39px;
                              }

                              .searchform {
                                padding-left: 25px;
                                height: 39px;
                                float:middle
                              }

                              h1 {
                               font-family: verdana;
                              }

                              table {
                                  border-collapse: collapse;
                                  width: 100%;
                              }

                              th, td {
                                  text-align: left;
                                  padding: 8px;
                              }

                              tr:nth-child(even){background-color: #f2f2f2}

                              th {
                                  background-color: #4CAF50;
                                  color: white;
                              }

                              </style>
                              </head>
                              <body style="background-color:lightgrey;">
                              <form action="/password_reset" method="post">

                              <ul>
                                <li><a class="active" >PASSWORD RESET PORTAL</a></li>
                              </ul>
                                Emp ID : e <input type="text" id="users" name="users">
                                Request : <input type="text" id="request" name="request">
                                Servers : <textarea id="servers" name="servers" rows="20" cols="20"></textarea>
                                <input type="submit" value="Submit">
                              </form>
                              </body>
                              </html>
              """
    else:
        return "<p>Login failed.</p>"


@route('/user_management',method=['POST'])
def user_creation():
        user = bottle.request.forms.getall('users')
        server = bottle.request.forms.getall('servers')
        mirror_id = bottle.request.forms.getall('mirror')
        request_id = bottle.request.forms.getall('request')
        user_list = []
        server_list = []
        current_time = time.strftime("%Y-%m-%d-%H-%M-%S")
        for i in user[0].split("\n"):
          c = i.rstrip()
          user_list.append(c)

        for j in server[0].split("\n"):
            d = j.rstrip()
            server_list.append(d)

        table_html="""
                  <!DOCTYPE html>
                  <html>
                  <head>
                  <style>
                  table {
                      font-family: arial, sans-serif;
                      border-collapse: collapse;
                      width: 100%;
                  }

                  td, th {
                      border: 1px solid #dddddd;
                      text-align: left;
                      padding: 8px;
                  }

                  </style>
                  </head>
                  <body>"""
        success_html = "<p><u><b>SUCCESSFULLY CREATED</p></u></b><table><tr><th>User</th><th>Server</th></tr>"
        fail_html = "<p><u><b>FAILED</p></u></b><table><th>Server</th><th>Error Log</th>"
        not_reachable = "<p><u><b>NOT REACHABLE SERVERS</p></u></b><table><th>Servers</th>"
        with open('/data/python_scripts/gui_scripts/logs/user_creation_script_output'+current_time,"w+") as output_file:
             for ser in server_list:
                    try:
                        server = ser.strip()
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        try:
                            ssh.connect(server)
                        except:
                            ssh.connect(server,allow_agent=False,look_for_keys=False,key_filename='/root/.ssh/id_dsa')
                        (stdin, stdout, stderr) = ssh.exec_command('uname')
                        os = stdout.readlines()
                        if os[0].startswith('Linux'):
                            for use in user_list:
                                 users = use.strip()
                                 (status, output) = commands.getstatusoutput('ldapsearch')
                                 a = output.split(":")
                                 b = a[-1].strip().replace(" ","_")
                                 req = request_id[0]+"-"+b
                                 (stdin, stdout, stderr) = ssh.exec_command('getent passwd '+mirror_id[0])
                                 mirror_exists = stdout.readlines()
                                 if mirror_exists:
                                        mirror_id_objects = mirror_exists[0].split(":")
                                        if mirror_id_objects[1] == 'x':
                                            (stdin, stdout, stderr) = ssh.exec_command('/usr/sbin/useradd -m -d /home/'+users+' -s '+mirror_id_objects[-1].strip()+' -c '+req+' -u 1'+users[1:]+' -g '+mirror_id_objects[3]+' '+users+';echo "'+users+':1234"|/usr/sbin/chpasswd;/usr/bin/chage -d 0 '+users+';/sbin/pam_tally2 --user='+users+' --reset')
                                            error = stderr.readlines()
                                            if not error:
                                                success_html += """<tr><td> %s </td><td> %s</td></tr>"""%(users,server)
                                                print >> output_file, "The %s has been successfully created in Linux Server %s"%(users,server)
                                            else:
                                                fail_html += """<tr><td> %s </td><td> %s</td></tr>"""%(server, error)
                                                print >> output_file, "Error : ",error
                                        else:
                                            fail_html += """<tr><td> %s </td><td> Mirrorid-%s(VAS)</td></tr>"""%(server,mirror_id[0])
                                            print >> output_file, "This mirror id '%s' is VAS Account"%(users)
                                 else:
                                      fail_html += """<tr><td> %s </td><td> Mirrorid-%s(does't exists)</td></tr>"""%(server,mirror_id[0])
                                      print >> output_file, "This mirror id '%s' does't exists in '%s'"%(mirror_id[0],server)
                        elif os[0].startswith('Sun'):
                            for use in user_list:
                                 users = use.strip()
                                 (status, output) = commands.getstatusoutput('ldapsearch')
                                 a = output.split(":")
                                 b = a[-1].strip().replace(" ","_")
                                 req = request_id[0]+"-"+b
                                 (stdin, stdout, stderr) = ssh.exec_command('getent passwd '+mirror_id[0])
                                 mirror_exists = stdout.readlines()
                                 if mirror_exists:
                                        mirror_id_objects = mirror_exists[0].split(":")
                                        if mirror_id_objects[1] == 'x':
                                            (stdin, stdout, stderr) = ssh.exec_command('/usr/sbin/useradd -m -d /local/home/'+users+' -s '+mirror_id_objects[-1].strip()+' -c '+req+' -u 1'+users[1:]+' -g '+mirror_id_objects[3]+' '+users)
                                            error = stderr.readlines()
                                            child = pexpect.spawn ('ssh '+server)
                                            child.expect ('# ')
                                            child.sendline ('passwd '+users)
                                            child.expect ('assword: ')
                                            child.sendline ('@123')
                                            child.expect ('assword: ')
                                            child.sendline ('@123')
                                            if not error and child.expect ('# ') == 0 and child.before.find("successfully") != -1:
                                                success_html += """<tr><td> %s </td><td> %s</td></tr>"""%(users,server)
                                                print >> output_file, "The %s has been successfully created in Sun Server %s"%(users,server)
                                            else:
                                                fail_html += """<tr><td> %s </td><td> %s</td></tr>"""%(server, error)
                                                print >> output_file, "Error : ",error
                                        else:
                                            fail_html += """<tr><td> %s </td><td> Mirrorid-%s(VAS)</td></tr>"""%(server,mirror_id[0])
                                            print >> output_file, "This mirror id '%s' is VAS Account"%(users)
                                 else:
                                      fail_html += """<tr><td> %s </td><td> Mirrorid-%s(does't exists)</td></tr>"""%(server,mirror_id[0])
                                      print >> output_file, "This mirror id '%s' does't exists in '%s'"%(mirror_id[0],server)
                        elif os[0].startswith('AIX'):
                            for use in user_list:
                                 users = use.strip()
                                 (status, output) = commands.getstatusoutput('ldapsearch')
                                 a = output.split(":")
                                 b = a[-1].strip().replace(" ","_")
                                 req = request_id[0]+"-"+b
                                 (stdin, stdout, stderr) = ssh.exec_command('cat /etc/passwd |grep '+mirror_id[0])
                                 mirror_exists = stdout.readlines()
                                 if mirror_exists:
                                        mirror_id_objects = mirror_exists[0].split(":")
                                        if mirror_id_objects[1] == 'x' or mirror_id_objects[1] == '!':

                                            (stdin, stdout, stderr) = ssh.exec_command('/usr/sbin/useradd -m -d /local/home/'+users+' -s '+mirror_id_objects[-1].strip()+' -c '+req+' -u 1'+users[1:]+' -g '+mirror_id_objects[3]+' '+users+';echo "'+users+':1234"|/usr/bin/chpasswd')
                                            error = stderr.readlines()
                                            if not error:
                                                success_html += """<tr><td> %s </td><td> %s</td></tr>"""%(users,server)
                                                print >> output_file, "The %s has been successfully created in AIX Server %s"%(users,server)
                                            else:
                                                fail_html += """<tr><td> %s </td><td> %s</td></tr>"""%(server, error)
                                                print >> output_file, "Error : ",error
                                        else:
                                            fail_html += """<tr><td> %s </td><td> Mirrorid-%s(VAS)</td></tr>"""%(server,mirror_id[0])
                                            print >> output_file, "This mirror id '%s' is VAS Account"%(users)
                                 else:
                                      fail_html += """<tr><td> %s </td><td> Mirrorid-%s(does't exists)</td></tr>"""%(server,mirror_id[0])
                                      print >> output_file, "This mirror id '%s' does't exists in '%s'"%(mirror_id[0],server)
                    except:
                        not_reachable += """<td> %s </td>"""%(server)
                        print >> output_file, "Cudt connect %s"%(server)
        success_html += "</table>"
        fail_html += "</table>"
        not_reachable += "</table>"
        template = table_html+success_html+fail_html+not_reachable
        return template


@route('/password_reset',method=['POST'])
def user_creation():
    user = bottle.request.forms.getall('users')
    server = bottle.request.forms.getall('servers')
    request = bottle.request.forms.getall('request')
    server_list = []
    emp_id = user[0].strip()
    request_id = request[0].strip()
    if len(emp_id) < 6:
        emp_id = "e0" + emp_id
    else:
        emp_id = "e" + emp_id
    (status, output) = commands.getstatusoutput('ldapsearch')
    manager_mail_id = output.split("\n")[1].split(":")[-1].strip()
    user_mail_id = output.split("\n")[2].split(":")[-1].strip()
    for j in server[0].split("\n"):
        d = j.rstrip()
        server_list.append(d)
    html_output_passwd_create = ''
    html_output_passwd_success = ''
    html_output_passwd_fail = ''
    html_output_passwd_error = ''
    html_output_passwd_vas = ''
    for ser in server_list:
        try:
            server = ser.strip()
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(server)
            except:
                ssh.connect(server,allow_agent=False,look_for_keys=False,key_filename='/root/.ssh/id_dsa')
            (stdin, stdout, stderr) = ssh.exec_command('id '+emp_id)
            account_check = stdout.readlines()
            if account_check:
                (stdin, stdout, stderr) = ssh.exec_command('uname')
                os = stdout.readlines()
                if os[0].startswith('Linux'):
                        (stdin, stdout, stderr) = ssh.exec_command('getent passwd '+emp_id)
                        vas_account_check = stdout.readlines()
                        if vas_account_check[0][8] == "V":
                                (stdin, stdout, stderr) = ssh.exec_command('/opt/quest/bin/vastool flush')
                        (stdin, stdout, stderr) = ssh.exec_command('getent passwd '+emp_id)
                        vas_account_check1 = stdout.readlines()
                        if vas_account_check1[0][8] == "V":
                                html_output_passwd_vas += "%s '%s' is VAS account please use your  credentials\n"%(server, emp_id)
                        else:
                                (stdin, stdout, stderr) = ssh.exec_command('echo "'+emp_id+':1234"|/usr/sbin/chpasswd;/usr/bin/chage -d 0 '+emp_id+';/sbin/pam_tally2 --user='+emp_id+' --reset')
                                err = stderr.readlines()
                                if err:
                                        html_output_passwd_error += "%s   '%s' %s\n"%(server,emp_id,err)
                                else:
                                        html_output_passwd_success += "%s     1234\n"%(server)
                elif os[0].startswith('AIX'):
                        (stdin, stdout, stderr) = ssh.exec_command('echo "'+emp_id+':1234"|/usr/bin/chpasswd;/usr/bin/chsec  -f /etc/security/lastlog -a "unsuccessful_login_count=0" -s '+emp_id+';/usr/bin/chuser "account_locked=false" '+emp_id)
                        err = stderr.readlines()
                        if err:
                                html_output_passwd_error += "%s   '%s' %s\n"%(server,emp_id,err)
                        else:
                                html_output_passwd_success += "%s     1234\n"%(server)
                elif os[0].startswith('Sun'):
                        (stdin, stdout, stderr) = ssh.exec_command('getent passwd '+emp_id)
                        vas_account_check = stdout.readlines()
                        if vas_account_check[0][8] == "V":
                                (stdin, stdout, stderr) = ssh.exec_command('/opt/quest/bin/vastool flush')
                        (stdin, stdout, stderr) = ssh.exec_command('getent passwd '+emp_id)
                        vas_account_check1 = stdout.readlines()
                        if vas_account_check1[0][8] == "V":
                                html_output_passwd_vas += "%s   '%s' is VAS account please use your  credentials\n"%(server, emp_id)
                        else:
                            try:
                                import pexpect
                                child = pexpect.spawn ('ssh '+server)
                                child.expect ('# ')
                                child.sendline ('passwd '+emp_id)
                                child.expect ('assword: ')
                                child.sendline ('@123')
                                child.expect ('assword: ')
                                child.sendline ('@123')
                                if child.expect ('# ') == 0 and child.before.find("successfully") != -1:
                                    html_output_passwd_success += "%s     @123\n"%(server)
                            except:
                                html_output_passwd_error += "%s   Solaris_Server_failed_pexpect\n"%(server)
            else:
                html_output_passwd_create += "%s   ID_doesnt_exist\n"%(server)
        except:
            html_output_passwd_fail += "%s   SSH_Connection_failed\n"%(server)
    output_screen = ""
    if html_output_passwd_fail or html_output_passwd_error:
        error_output = gen_html(html_output_passwd_fail,"fail", emp_id) + gen_html(html_output_passwd_error,"error", emp_id)
        output_screen += error_output
    user_email = gen_html(html_output_passwd_success,"success",emp_id)+gen_html(html_output_passwd_create,"create",emp_id)+gen_html(html_output_passwd_vas,"vas",emp_id)
    if user_email:
        user_mail_output = gen_mail_reseted_user_passwd(user_mail_id,user_email, request_id)
        output_screen += "<p><h2><u>Mail sent to User</h2></p></u>"+user_mail_output
    else:
        output_screen += "<p><h2><u>No Mail sent to User</h2></p></u>"
    dl_it_html = gen_html(html_output_passwd_success,"dl_it", emp_id)
    if dl_it_html:
        dl_it_email = gen_mail_reseted_dlit_passwd(user_mail_id,manager_mail_id,dl_it_html, request_id)
        output_screen += "<p><h2><u>Mail sent to DL-IT</h2></p></u>"+dl_it_email
    else:
        output_screen += "<p><h2><u>No Mail sent to DL-IT</h2></p></u>"
    return "<p><h3><u>Output(%s)</h3></p></u>"%request_id+output_screen



def gen_html(html_obj,check,emp_id):
    ret_html = ""
    if check == "create" or check == "vas":
        ret_html += '''<p>We are not able to complete your request password reset for your ID "%s" on below servers.</p>'''%(emp_id)
    if check == "success":
        ret_html += ''' <p>Hi,This is to inform the password for your ID "%s" has been successfully reset on below severs. Kindly login and change your password within 3 days to avoid password expiration.</p>
                       <table border="1" style="width:500px;" margin-left:40px;top: 20px;position: relative;"><tr><th bgcolor="#ffcb00">Server Name</th><th bgcolor="#ffcb00">New Password</th></tr>
                    '''%(emp_id)
    elif check == "create" or check == "vas" or check == "fail" or check == "error":
        ret_html += '''<table border="1" style="width:500px;" margin-left:40px;top: 20px;position: relative;"><tr><th bgcolor="#ffcb00">Server Name</th><th bgcolor="#ffcb00">Server Status</th></tr>
                      '''
    elif check == "dl_it":
        ret_html += ''' <p>Hi,This is to inform the password for your ID "%s" has been successfully reset on below severs. Kindly login and change your password within 3 days to avoid password expiration.</p>
                       <table border="1" style="width:200px;" margin-left:40px;top: 20px;position: relative;"><tr><th bgcolor="#ffcb00">Server Name</th></tr>
                    '''%(emp_id)
        split = html_obj.splitlines()
        val = False
        for i in split:
            if i:
                val = True
                a = i.split(" ")
                ret_html += """<tr><td>%s</td></tr>
                                    """%(a[0])
        ret_html += '</table>'
        if val:
            return ret_html
        else:
            return ""
    split = html_obj.splitlines()
    val = False
    for i in split:
        if i:
            val = True
            a = i.split(" ")
            ret_html += """<tr><td>%s</td><td>%s</td></tr>
                                """%(a[0]," ".join(a[1:]))
    ret_html += '</table>'
    if val:
        return ret_html
    else:
        return ""


def gen_mail_reseted_user_passwd(recipients, html_table, request_id):
        me = "mail"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Password Reset Status"
        msg['From'] = me
        msg['To'] = recipients
        text = "Password Reset Status(%s)"%request_id
        html = """<html>
                                <head></head>
                                        <body>
                                        <h2>Unix Password Reset</h2>"""
        html += html_table
        html +="""      <table border="1" style="width:500px;" margin-left:40px;top: 10px;position: relative;">
                                <tr><th bgcolor="#ffcb00">Reason</th><th bgcolor="#ffcb00">Explanation</th><th bgcolor="#ffcb00">Your Next action</th></tr>
                                <tr><td>Your User ID doesnt exist</td><td>Your ID is not present in the requested server.</td><td>Raise a request for ID creation using service Exchange & attach you mangers approval to the ticket </td></tr>
                                <tr><td>Server not reachable</td><td>Unable to reach the server, request you to verify the server name.</td><td>Verify the server name and if valid, raise a new service request for the password reset.</td></tr>
                        </table>
                        <p>Please respond only to mail if you have any quires.</p>
                        <p>Thanks,</p>
                        <p>Unix Service Team</p>
                        </body>
                </html>
                        """
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        s = smtplib.SMTP('localhost')
        s.sendmail(me, recipients, msg.as_string())
        s.quit()
        return html

def gen_mail_reseted_dlit_passwd(user_mail_id, manager_mail_id, dl_it_html, request_id):
        me = "mail"
        recipients = [manager_mail_id]
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Password Reset Status(%s)"%request_id
        msg['From'] = me
        msg['To'] = user_mail_id
        msg['Cc'] = ", ".join(recipients)
        text = "Password Reset Status"
        html = """<html>
                                <head></head>
                                        <body>
                                        <h2>Unix Password Reset</h2>
                                        """
        html += dl_it_html
        html +="""      <p>Please respond only to mail if you have any quires.</p>
                        <p>Thanks,</p>
                        <p>Unix Service Team</p>
                        </body>
                </html>
                        """
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        s = smtplib.SMTP('localhost')
        s.sendmail(me, recipients, msg.as_string())
        s.quit()
        return html

run(host="server", port=8080)




# @route('/sox_deletion',method=['GET'])
# def sox_deletion():
#   html2 ='''<form action="/sox_deletions" method="post">
#             <p>Request : <input type="text" id="request" name="request"></p>
#             Users : <textarea id="users" name="users" rows="20" cols="20"></textarea>
#             Servers : <textarea id="servers" name="servers" rows="20" cols="20"></textarea>
#             <input type="submit" value="Submit">
#             <form>
#           '''
#   return html2

# @route('/sox_deletions',method=['GET', 'POST'])
# def sox_deletions():
#         request_id = bottle.request.forms.getall('request')
#         user = bottle.request.forms.getall('users')
#         server = bottle.request.forms.getall('servers')
#         user_list = []
#         server_list = []
#         current_time = time.strftime("%Y-%m-%d-%H-%M-%S")
#         for i in user[0].split("\n"):
#           c = i.rstrip()
#           user_list.append(c)

#         for j in server[0].split("\n"):
#             d = j.rstrip()
#             server_list.append(d)

#         html3 = ''
#         with open('/data/python_scripts/gui_scripts/logs/sox_deletions'+request_id[0]+current_time,"w+") as output_file:
#              for ser in server_list:
#                 for use in user_list:
#                     try:
#                         server = ser.strip()
#                         users = use.strip()
#                         ssh = paramiko.SSHClient()
#                         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#                         try:
#                             ssh.connect(server)
#                         except:
#                             ssh.connect(server,allow_agent=False,look_for_keys=False,key_filename='/root/.ssh/id_dsa')
#                         (stdin, stdout, stderr) = ssh.exec_command('uname')
#                         os = stdout.readlines()
#                         if os[0].startswith('Linux'):
#                           (stdin, stdout, stderr) = ssh.exec_command('/usr/sbin/userdel '+users)
#                           error = stderr.readlines()
#                           if not error:
#                               html3 += """<p> %s deleted in %s Successfully</p>"""%(users,server)
#                               print >> output_file, "<p> %s deleted in %s Successfully</p>"%(users,server)
#                           else:
#                               html3 += """<p>Error : %s</p>"""%(error)
#                               print >> output_file, "Error : ",error
#                         elif os[0].startswith('Sun'):
#                           (stdin, stdout, stderr) = ssh.exec_command('/usr/sbin/userdel '+users)
#                           error = stderr.readlines()
#                           if not error:
#                               html3 += """<p> %s deleted in %s Successfully</p>"""%(users,server)
#                               print >> output_file, "<p> %s deleted in %s Successfully</p>"%(users,server)
#                           else:
#                               html3 += """<p>Error : %s</p>"""%(error)
#                               print >> output_file, "Error : ",error
#                         elif os[0].startswith('AIX'):
#                           (stdin, stdout, stderr) = ssh.exec_command('/usr/sbin/rmuser '+users)
#                           error = stderr.readlines()
#                           if not error:
#                               html3 += """<p> %s deleted in %s Successfully</p>"""%(users,server)
#                               print >> output_file, "<p> %s deleted in %s Successfully</p>"%(users,server)
#                           else:
#                               html3 += """<p>Error : %s</p>"""%(error)
#                               print >> output_file, "Error : ",error
#                     except:
#                         html3 += """<p>Cudt connect %s</p>"""%(server)
#         return html3



