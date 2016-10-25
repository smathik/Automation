from bottle import run,debug,get,post,hook, response, request, route
import sys, paramiko, time, commands, pexpect, bottle

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/test',method=['GET', 'POST'])
def array():
  global html
  html ="""               <html>
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


                          </style>
                          </head>
                          <body style="background-color:lightgrey;">
                          <form action="/test1" method="post">

                          <ul>
                            <li><a class="active" >CHECKING SERVER STATUS</a></li>
                          </ul>
                            Server Name : <textarea id="servers" name="servers" rows="20" cols="20"></textarea>
                            <input type="submit" value="Get Details">
                          </form>
                          </body>
                          </html>
          """
  return html

@bottle.route('/test1', method='POST')
def pool():
        global html
        global server_list
        server = bottle.request.forms.getall('servers')
        server_list = []
        for j in server[0].split("\n"):
            d = j.rstrip()
            server_list.append(d)
        print server_name[0]
        current_time = time.strftime("%Y-%m-%d-%H-%M-%S")
        try:
                        server = server_name[0].strip()
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        try:
                            ssh.connect('localhost', username="root", password="passw0rd")
                        except:
                            ssh.connect(server,allow_agent=False,look_for_keys=False,key_filename='/root/.ssh/id_dsa')
                        (stdin, stdout, stderr) = ssh.exec_command('uname')
                        os = stdout.readlines()
                        if os[0].startswith('Linux'):
                                        print "yes"
                                        html += """
                                        <form action="/test2" method="post">
                                        <p> Tool :  <select name="select">
                                        <option value="httpd">%s</option>
                                        <option value="tomcat">%s</option>
                                        <option value="weblogic">%s</option>
                                        </select>
                                        </p>
                                        <input type="radio" name="options" id="health" value="health"> Status </input><br>
                                        <input type="radio" name="options" id="restart" value="restart"> Restart </input><br>
                                        <input type="radio" name="options" id="restart" value="restart"> Stop </input><br>
                                        <input type="submit" value="Submit">
                                        </form>
                                         """%("httpd","tomcat","weblogic")
        except:
                        print "nope"
        return html

@route('/test2',method=['GET', 'POST'])
def tier():
    global html
    health = bottle.request.forms.getall('health')
    restart = bottle.request.forms.getall('restart')
    select = bottle.request.forms.getall('select')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('localhost', username="root", password="passw0rd")
    output = []
    if select[0].startswith("httpd"):
        (stdin, stdout, stderr) = ssh.exec_command('ps -ef | grep -i java | wc -l')
        httpd_output = stdout.readlines()
        if int(httpd_output[0]) >= 2:
            (stdin, stdout, stderr) = ssh.exec_command('/etc/init.d/httpd status')
            httpd_status = stdout.readlines()
            output.append(httpd_status[0])
    html +='''
    Summary : <textarea id="users" name="users" rows="10" cols="50">%s</textarea>
    '''%output[0]

    return html

run(host="localhost", port=8010)
