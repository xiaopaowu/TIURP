function [horizontalImage,verticalImage] = gaussianDeriviationComputer(img,sigma,hsize)
    
    if nargin < 3
        hsize = [5 5]; % default parameter value
    end;

    gaussArray = fspecial('gaussian',hsize,sigma);
    filteredImg = conv2(img,gaussArray,'same');

    % calculate the horizontal gradient
    horizontalHSize = [-1 1];
    horizontalImage = conv2(filteredImg,horizontalHSize,'same');

    % calculate the vertical gradient
    verticalHSize = horizontalHSize';
    verticalImage = conv2(filteredImg,verticalHSize,'same');
end
