import os,shutil
sourceDir = r"C:\Users\FYC\Desktop\newColpng"
baseDir = r"F:/"

def movePng():
    with open(r"C:\Users\FYC\Desktop\allKinds.txt","r") as f:#读取对应txt文件
        lines = f.readlines()
    currentNum = 0
    folderIndex= 0
    while(True):
        if(currentNum!=0 and currentNum%12 ==0):
            folderIndex+=1
            currentNum = 0
        targetDir = baseDir + lines[folderIndex].strip() + "PNG"  # 目标文件夹
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)
        shutil.copy(r"C:\Users\FYC\Desktop\newColpng/" + lines[folderIndex].strip()+"_"+str(currentNum+1)+".png",
                    targetDir + "/" + lines[folderIndex].strip()+"_"+str(currentNum+1)+".png")  # 执行复制操作
        print("正在复制图片：", lines[folderIndex].strip()+"_"+str(currentNum+1)+".png")
        currentNum += 1
    f.close()

def Generatetxt():
    with open(r"C:\Users\FYC\Desktop\allKinds.txt","r") as f:#读取对应txt文件
        lines = f.readlines()
    for i in range(len(lines)):
        txtName = lines[i].strip()
        print(txtName)
        with open(r".\dataset2/"+txtName+".txt", "w") as f:
            for i in range(1,13):
                num = str(i)
                jpg = txtName + "_" + num + ".jpg;"
                png = txtName  + "_" + num + ".png\n"
                f.write( jpg+png)
        f.close()
    f.close()

Generatetxt()
# movePng()