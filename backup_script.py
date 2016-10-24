import os, zipfile, time, sys, datetime

def raw_data(source_folder, target_zip):
    zipf = zipfile.ZipFile(target_zip, "w")
    for subdir, dirs, files in os.walk(source_folder):
        for file in files:
            print os.path.join(subdir, file)
            zipf.write(os.path.join(subdir, file))
    print "Created ", target_zip

def processed_data(source_folder, target_zip):
    zipf = zipfile.ZipFile(target_zip, "w")
    for subdir, dirs, files in os.walk(source_folder):
        for file in files:
            print os.path.join(subdir, file)
            zipf.write(os.path.join(subdir, file))
    print "Created ", target_zip

def delete_raw_data(path):
    for file in os.listdir(path):
        fullpath   = os.path.join(path,file)   
        timestamp  = os.stat(fullpath).st_ctime
        createtime = datetime.datetime.fromtimestamp(timestamp)
        now        = datetime.datetime.now()
        delta      = now - createtime
        if delta.days > 90:
            os.remove(fullpath)
            print "Removed ", path

def delete_process_data(path):    
    for file in os.listdir(path):
        fullpath   = os.path.join(path,file)   
        timestamp  = os.stat(fullpath).st_ctime
        createtime = datetime.datetime.fromtimestamp(timestamp)
        now        = datetime.datetime.now()
        delta      = now - createtime
        if delta.days > 365:
            os.remove(fullpath)
            print "Removed ", path

if __name__ =='__main__':
    print "Starting execution"

    #compress to zip_Processed
    source_folder = '/callman/CAR/'
    target_zip = '/callman/CAR/Raw_data.zip'
    raw_data(source_folder, target_zip)  
    
    #compress to zip_Processed
    source_folder = '/callman/CAR/Processed'
    target_zip = '/callman/CAR/Processed/Processed.zip'
    processed_data(source_folder, target_zip)   

    #delete_after_3_months_raw_data
    delete_raw_data("/callman/CAR/Processed/Processed.zip")

    #delete_after_1_year_Processed_data
    delete_process_data("/callman/CAR/Processed/Processed.zip")

    print "Ending execution"
