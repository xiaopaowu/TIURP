function [hds1,hds2,hds4,hds8,vds1,vds2,vds4,vds8] = myGaussianFilterBank(img)

    hsize = [5 5]; % default parameter value
    res = cell(6);
    sigma = [1,2,4,8]; % required values

    for i = 1:1:length(sigma)
        [hds, vds] = gaussianDeriviationComputer(img,sigma(i));
        res{i} = hds;
        res{i+4} = vds;
    end

    hds1 = res{1};
    hds2 = res{2};
    hds4 = res{3};
    hds8 = res{4};
    vds1 = res{5};
    vds2 = res{6};
    vds4 = res{7};
    vds8 = res{8};
end