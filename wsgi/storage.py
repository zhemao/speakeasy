import gridfs
from werkzeug import secure_filename
from pymongo import ASCENDING, DESCENDING
from datetime import datetime

def store_file(f, username, aes_key, db):
    fname = secure_filename(f.filename)
    
    gfs = gridfs.GridFS(db)
    
    gf = gfs.new_file(filename=fname, contentType=f.content_type)
    
    gf.write(f)
    gf.close()
    f.close()

    date = datetime.now()

    finfo = {'file_id': gf._id, 
             'username': username, 
             'filename': fname,
             'aes_key': aes_key,
             'date': date}

    return db.fileinfo.insert(finfo)

def find_file(db, username, filename):
    finfo = get_fileinfo(db, username, filename)

    gfs = gridfs.GridFS(db)

    if finfo:
        return gfs.get(finfo['file_id']), finfo['aes_key']

    return None

def get_fileinfo(db, username, filename):
    finfo = db.fileinfo.find_one({'username': username,
                                  'filename': filename},
                                 sort = [('date', DESCENDING)])

    return finfo

def copy_file(db, user_from, user_to, filename, aes_key):
    finfo = get_fileinfo(db, user_from, filename)
    
    finfo['aes_key'] = aes_key
    finfo['username'] = user_to
    finfo['date'] = datetime.now()

    return db.fileinfo.insert(finfo)

def list_files(db, username):
    files = db.fileinfo.group(['filename'], {'username': username}, 
                {'date': datetime(1970, 1, 1)},
                '''
                function(obj, prev){
                    if(obj.date > prev){
                        prev.date = obj.date;
                        prev.filename = obj.filename;
                        prev.aes_key = obj.aes_key;
                    }
                }
                ''')

    return [f for f in files]
