import gridfs
from werkzeug import secure_filename
from pymongo import ASCENDING, DESCENDING

def store_file(f, username, db):
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
             'date': date}

    return db.fileinfo.insert(finfo)

def find_file(db, username, filename):
    finfo = db.fileinfo.find_one({'username': username,
                                  'filename': filename},
                                 sort = [('date', DESCENDING)])

    gfs = gridfs.GridFS(db)

    if finfo:
        return gfs.get(finfo['file_id'])

    return None
