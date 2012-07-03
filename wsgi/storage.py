import gridfs
from werkzeug import secure_filename
from pymongo import ASCENDING, DESCENDING
from datetime import datetime
import fnmatch

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

def retrieve_file(db, finfo):
    gfs = gridfs.GridFS(db)

    if finfo:
        return gfs.get(finfo['file_id'])

    return None

def ensure_file_index(db):
    db.fileinfo.ensure_index([('username', ASCENDING), 
                              ('filename', ASCENDING), 
                              ('date', DESCENDING)])


def get_fileinfo(db, username, filename):
    ensure_file_index(db)

    finfo = db.fileinfo.find_one({'username': username,
                                  'filename': filename},
                                 sort = [('date', DESCENDING)])

    return finfo

def get_versions(db, username, filename, earliest=None, latest=None):
    ensure_file_index(db)

    query = {'username': username,
             'filename': filename}

    if earliest and latest:
        query['$and'] = [{'date': {'$gt': earliest}}, 
                         {'date': {'$lt': latest}}]
    elif earliest:
        query['date'] = {'$gt': earliest}
    elif latest:
        query['date'] = {'$lt': latest}

    return db.fileinfo.find(query).sort('date', DESCENDING)
    

def copy_file(db, user_from, user_to, filename, aes_key):
    finfo = get_fileinfo(db, user_from, filename)

    if not finfo:
        return False
    
    finfo['filename'] = user_from + '_' + filename
    finfo['aes_key'] = aes_key
    finfo['username'] = user_to
    finfo['date'] = datetime.now()
    del finfo['_id']

    return db.fileinfo.insert(finfo)

def delete_file(db, username, filename, earliest=None, latest=None):
    versions = get_versions(db, username, filename, earliest, latest)
    gfs = gridfs.GridFS(db)
    ids = []

    for finfo in versions:
       gfs.delete(finfo['file_id'])
       ids.append(finfo['_id'])

    db.fileinfo.remove({'_id': {'$in': ids}})

def list_files(db, username, pattern=None):
    ensure_file_index(db)

    query = {'username': username}
    
    if pattern:
        query['filename'] = {'$regex': fnmatch.translate(pattern)}

    files = db.fileinfo.group(['filename'], query,
                {'date': datetime(1970, 1, 1)},
                '''
                function(obj, prev){
                    if(obj.date > prev){
                        prev.date = obj.date;
                        prev.filename = obj.filename;
                    }
                }
                ''')

    return [f for f in files]
