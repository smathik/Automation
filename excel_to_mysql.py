import xlrd, MySQLdb
from datetime import date, datetime
book = xlrd.open_workbook("/root/master.xlsx")
sheet = book.sheet_by_name("New Version")
database = MySQLdb.connect(host="localhost", user="root", passwd="passw0rd", db="unixinventory")
cursor = database.cursor()
query = """INSERT INTO master (ip, fqdn, server_name, serverowner, application_name, app_support_contact, console, machine_type, site_type, last_patched, in_scope_for_patch, environment, updated_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
for r in range(sheet.nrows):
    try:
      ip      = str(sheet.cell(r,0).value)
      fqdn = str(sheet.cell(r,1).value)
      server_name          = str(sheet.cell(r,2).value)
      serverowner     = str(sheet.cell(r,3).value)
      application_name       = str(sheet.cell(r,4).value)
      app_support_contact = str(sheet.cell(r,5).value)
      console        = str(sheet.cell(r,6).value)
      machine_type       = str(sheet.cell(r,7).value)
      site_type     = str(sheet.cell(r,8).value)
      try:
          last     = sheet.cell(r,9).value
          last_patch =  xlrd.xldate_as_tuple(last, 0)
          a1_datetime = datetime(*last_patch)
          last_patched = a1_datetime.strftime("%d/%m/%Y") 
      except:
          last_patched = str(sheet.cell(r,9).value) 
      in_scope_for_patch = str(sheet.cell(r,10).value)
      environment = str(sheet.cell(r,11).value)
      updated_by = "MASTER_INVENTORY"
      values = (ip, fqdn, server_name, serverowner, application_name, app_support_contact, console, machine_type, site_type, last_patched, in_scope_for_patch, environment, updated_by)
      cursor.execute(query, values)
    except:
      ip      = str(sheet.cell(r,0).value)
      print "failed>>",ip
      continue      

cursor.close()
database.commit()
database.close()
