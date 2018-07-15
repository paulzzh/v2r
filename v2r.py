def error():
    print("VideoToResource By Paulzzh [Version 2.0]\nWebsite: https://github.com/paulzzh/v2r/\nUsage: python v2r.py <mode> <videoinput> <resourceoutputdir> <block> <size> <count> <fps> <frametime>\n <mode>\n  PC Make ResourcePack for Minecraft Java Edition 1.?-1.12.2\n  PE Make ResoucePack for Minecraft PE/Win10 Edition\n <videoinput>\n  The video path. eg. D:/documents/anime.mp4\n <resourceoutputdir>\n  The output dir. eg. D:/documents/ \n <block>\n  The block id name you want. eg. sea_lantern\n <size>\n  The size of your resoucepack. eg.64 128 2048\n <count>\n  Frames in one pack.\n <fps>\n  Change the fps of the video.\n <frametime>\n  Frametime in .png.mcmeta or ticks_per_frame in flipbook_textures.json\n")
    sys.exit(1)

def images():
    imagelist = []
    picnum = 0
    for file in os.listdir(imglistdir):
        imagelist.append(file)
    totalpicnum = len(imagelist)
    global totaldirnum
    totaldirnum = (totalpicnum // count) + 1
    for dirnum in range(totaldirnum):
        dirpath = imglistdir + "/" + str(dirnum)
        os.mkdir(dirpath)
    for picnum in range(totalpicnum):
        dirnum = (picnum // count)
        fromfile = imglistdir + "/" + imagelist[picnum]
        tofile = imglistdir + "/" + str(dirnum) + "/" + imagelist[picnum]
        shutil.move(fromfile,tofile)
    for dirnum in range(totaldirnum):
        dirpath = imglistdir + "/" + str(dirnum) + "/"
        cmd = "convert -append " + dirpath + "*.png " + dirpath + block + ".png"
        os.system(cmd)

def video():
    if not os.path.exists(workdir):
        os.mkdir(workdir)
    if not os.path.exists(imglistdir):
        os.mkdir(imglistdir)
    shutil.copy(videoinput,workdir)
    cmd = "ffmpeg -i " + videoinput + " -vf pad=2048:2048:64:484:white -r " + fps + " " + workdir + "/2048.mp4" 
    os.system(cmd)
    cmd = "ffmpeg -i " + workdir + "/2048.mp4 -vf scale=-2:" + size + " " + workdir + "/" + size + ".mp4"
    os.system(cmd)
    cmd = "ffmpeg -i " + workdir + "/" + size + ".mp4 -f image2 " + imglistdir + "/img%06d.png"
    os.system(cmd)
    #print("mdz")

def clean():
    shutil.rmtree(workdir)

def packPC():
    if os.path.exists(assetsdir):
        shutil.rmtree(blocksdir)
    for dirnum in range(totaldirnum):
        os.makedirs(blocksdir)
        dirpath = imglistdir + "/" + str(dirnum) + "/"
        shutil.copy(dirpath + block + ".png",blocksdir)
        outputfile = resourceoutputdir + mode + "_" + block + "_" + str(dirnum) + ".zip"
        shutil.copy("PC.dll",outputfile)
        mcmetafile = blocksdir + "/" + block + ".png.mcmeta"
        line1 = "{\n"
        line2 = "    \"animation\": {\n"
        line3 = "        \"frametime\":" + frametime +"\n"
        line4 = "    }\n"
        line5 = "}"
        with open(mcmetafile, 'w') as f:
            f.writelines([line1, line2, line3, line4, line5])
        cmd = "7z u " + outputfile + " " + assetsdir
        os.system(cmd)
        shutil.rmtree(blocksdir)
    clean()

def packPE():
    if os.path.exists(texturesdir):
        shutil.rmtree(peblocksdir)
    for dirnum in range(totaldirnum):
        os.makedirs(peblocksdir)
        dirpath = imglistdir + "/" + str(dirnum) + "/"
        shutil.copy(dirpath + block + ".png",peblocksdir)
        outputfile = resourceoutputdir + mode + "_" + block + "_" + str(dirnum) + ".zip"
        shutil.copy("PE.dll",outputfile)
        jsonfile = texturesdir + "/flipbook_textures.json"
        line1 = "[\n"
        line2 = "  {\n"
        line3 = "    \"flipbook_texture\": \"textures/blocks/" + block + "\",\n"
        line4 = "    \"atlas_tile\": \"" + block + "\",\n"
        line5 = "    \"ticks_per_frame\":" + frametime + "\n"
        line6 = "  }\n"
        line7 = "]"
        with open(jsonfile, 'w') as f:
            f.writelines([line1, line2, line3, line4, line5, line6, line7])
        cmd = "7z u " + outputfile + " " + texturesdir
        os.system(cmd)
        shutil.rmtree(texturesdir)
    clean()

def rmode():
    if mode == "PC":
        video()
        images()
        packPC()
    elif mode == "PE":
        video()
        images()
        packPE()
    else:
        error()

if __name__ == '__main__':
    import sys
    import os
    import shutil
    import tempfile
    totaldirnum = 1
    workdir = tempfile.mkdtemp().replace("\\", "/")
    imglistdir = workdir + "/imglist"
    assetsdir = workdir + "/assets"
    blocksdir = workdir + "/assets/minecraft/textures/blocks"
    peblocksdir = workdir + "/textures/blocks"
    texturesdir = workdir + "/textures"
    args = sys.argv[1:]
    if len(args) != 8:
        error()
    mode, videoinput, resourceoutputdir, block, size, count, fps, frametime = args
    count = int(count)
    rmode()