import Everything.SearchByName
import sys
import os

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes)

def split(fromfile, todir, chunksize=chunksize):
    print('splitting file', fromfile)
    try:
        if not os.path.exists(todir):
            os.mkdir(todir)
        else:
            for filename in os.listdir(todir):
                os.remove(os.path.join(todir, filename))
    except PermissionError:
        print('permision denied')
        return

    if not os.path.exists(fromfile):
        return

    partnum = 0
    input = open(fromfile, 'rb')
    (temp, inputfilename) = os.path.split(fromfile)
    while True:
        chunk = input.read(chunksize)
        if not chunk:
            break        
        filename = os.path.join(todir,  inputfilename + '_part_%d' %(partnum))
        output = open(filename, 'wb')
        output.write(chunk)
        output.close()
        partnum += 1
    input.close()

def merge(fromdir, tofile, filenamePrefix):
    if not os.path.exists(fromdir):
        return 

    output = open(tofile, 'wb')
    filelist = list(os.listdir(fromdir))
    filelist.sort()
    for partfilename in filelist:
        if not filenamePrefix in partfilename: continue
        filepath = os.path.join(fromdir, partfilename)
        filesize = os.path.getsize(filepath)
        fileobj = open(filepath, 'rb')
        output.write(fileobj.read(filesize))
        fileobj.close()
    output.close()
