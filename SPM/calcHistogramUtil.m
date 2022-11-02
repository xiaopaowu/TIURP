function h = calcHistogramUtil(img, x, roi)
    if isempty(roi)
        h = hist(double(img(:)), x);
    else
        h = hist(double(img(roi)), x);
    end    
end