function mySPMain()

    addpath('./histogram_distance');
    addpath('./SpatialPyramid')
    result_data_dir = 'result';
    mapObj = containers.Map
    
    baseDir = 'D:\data\report\';

    programName = 'Wonderland'

    % load in all images
    imgBaseDir = strcat(baseDir, programName);
%     imgList = mydir(imgBaseDir);
    imgListDir=strcat('ImageNames-',programName,'.txt')
    
    imgList = {};
    fid=fopen(imgListDir,'r');
    L=1;
    while ~feof(fid)
        str=fgetl(fid);
        imgList = regexp(str, ',', 'split')
    end
    fclose(fid);

    width = 480;
    height = 480;

    resizedFolder = strcat(baseDir,programName,'-resizedImgs')

    if exist(resizedFolder,'dir') ~= 7
        mkdir(resizedFolder)
    end

    fileList = {};
    for i = 1:1:length(imgList)
        fileList{i} = imgList{i}
        imgPath = strcat(imgBaseDir,'\',fileList{i});
        imgOutputPath = strcat(resizedFolder,'\',fileList{i});
        img = imread(imgPath);
        resizedImg = imresize(img, [width, height]);
        imwrite(resizedImg, imgOutputPath);
    end;

    % We need resize the images 

    resizedImgBaseDir = strcat(resizedFolder,'\');

    % Specify the parameters
    params.maxImageSize = 1000 %1920
    params.gridSpacing = 1
    params.patchSize = 16
    params.dictionarySize = 200  % M value, according to the paper, set this value into 400 could get a good results.
    params.numTextonImages = 100 
    params.pyramidLevels = 3  % level

    % we should define the distance between the reports;
    pyramid_all = BuildPyramid(fileList,resizedImgBaseDir,[result_data_dir '2'],params,1,1);
    
    T = cell2table(fileList)
    writetable(T,strcat('ImageNames-',programName,'.txt'));

    distM = pdist2(pyramid_all,pyramid_all,@chi_square_statistics);
    csvwrite(strcat('SPDistanceMatrix-',programName,'.txt'),distM);
end
