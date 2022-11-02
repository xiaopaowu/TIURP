function myRGBHistogram(programName)


    baseDir = 'E:\ImageBasedReportClasssification\';
    % programName = '2048';

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


    resultVector = cell(length(imgNameList),1);

    for k = 1:1:length(imgPathList)

        img = imread(imgPathList{k});

        % check if image is color
        colorImage = size(img, 3)==3;

        % compute intensity bounds, based either on type or on image data
        if isinteger(img)
            type = class(img);
            minimg = intmin(type);
            maximg = intmax(type);
        else
            minimg = min(img(:));
            maximg = max(img(:));
        end
        
        N = 256; % color size

        % default roi is empty
        roi = [];

        % compute bin centers if they were not specified
        %if ~exist('x', 'var')
            x = linspace(double(minimg), double(maximg), N);
        %end


        %% Main processing 
        % compute image histogram
        if ~colorImage
            % process 2D or 3D grayscale image
            h = calcHistogramUtil(img, x, roi);
        else
            % process color image: compute histogram of each channel
            h = zeros(length(x), 3);
            if ndims(img)==3
                % process 2D color image
                for i=1:3
                    h(:, i) = calcHistogramUtil(img(:,:,i), x, roi);
                end        
            else
                % process 3D color image
                for i=1:3
                    h(:, i) = calcHistogramUtil(img(:,:,i,:), x, roi);
                end
            end
        end

        linear = zeros(1,numel(h));
        linear(:) = h(:);
        resultVector{k} = linear;
    end

    dlmwrite(strcat('RGBFeatureVector-',programName,'.txt'),resultVector,'delimiter',';','precision','%.3f');

    resultArray = cell2mat(resultVector);
    distanceVector = pdist(resultArray,'euclidean');
    distanceMatrix = squareform(distanceVector);

    dlmwrite(strcat('RGBHistDistanceMatrix-',programName,'.txt'),distanceMatrix,'delimiter',';','precision','%.3f');
end




