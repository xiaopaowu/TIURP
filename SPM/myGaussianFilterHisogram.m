function myGaussianFilterHisogram(programName)
    
    baseDir = 'E:\ImageBasedReportClasssification\';
    programName = '2048';

    imgBaseDir = strcat(baseDir,programName);

    fid = fopen(strcat('ImageNames-',programName,'.txt'),'r');

    imgNum = length(mydir(imgBaseDir));
    imgNameList = cell(imgNum,1);

    tline = fgets(fid);
    lineCounter = 1;
    while ischar(tline)
        disp(tline)
        imgNameList{lineCounter} = tline;
        lineCounter = lineCounter + 1;
        tline = fgets(fid);
    end
    fclose(fid);

    imgPathList = cell(length(imgNameList),1);

    for i = 1:1:length(imgNameList)
        imgPathList{i} = strcat(imgBaseDir,'\',imgNameList{i});
    end;

    resultVector = cell(length(imgNameList),8);

    for i = 1:1:length(imgPathList)
        values = cell(8);
        imgTmp = im2double(rgb2gray(imread(imgPathList{i})));
        [values{1},values{2},values{3},values{4},values{5},values{6},values{7},values{8}] = myGaussianFilterBank(imgTmp);
        for j=1:8
            resultVector{i,j} = mean(mean(abs(values{j})));
        end 
    end

    dlmwrite(strcat('HistFeatureVector-',programName,'.txt'),resultVector,'delimiter',';','precision','%.3f');

    resultArray = cell2mat(resultVector);
    distanceVector = pdist(resultArray,'euclidean');
    distanceMatrix = squareform(distanceVector);

    dlmwrite(strcat('HistDistanceMatrix-',programName,'.txt'),distanceMatrix,'delimiter',';','precision','%.3f');

end
