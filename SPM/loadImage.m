function imgCell = loadAllImages(picPath)

    picDir = mydir(picPath);
    imgCell = cell(1,length(picDir));
    
    for i = 1:1:length(picDir)
        imgPath = strcat(picPath, '\', picDir(i).name);
        imgTmp = imread(imgPath);
        imgCell{i} = imgTmp;
    end;

end