# TIURP
Mobile_Crowdsourced_Test_Report_Prioritization_based_on_Text_and_Image_Understanding<br>

* Folder "reports": it contains raw crowdsourced test reports on six projects.

* Folder "results": it describes the experiment results, including the APFD values. Each file has 30 rows, and each row is an experimental result. In addition, each column is the results of different comparison methods, ranging from RANDOM, BDDiv, DMBD19, TSE20, to TIURP.

* Folder "src": it contains the source code.
  * SPM(in Matlab): contains Spatial Pyramid Matching(SPM), scale-invariant feature transform(SIFT) descriptors extraction, histograms building, and histogram distance calculation for screenshots
  * e2lsh: the locality-sensitive hashing technique (LSH) to map the image feature vector to an index value
  * baseline_bddiv.py & baseline_dmbd19.py & baseline_tse20.py & baseline_ctrp.py: main functions
  * bddiv.py & clustering.py & lsh_approach.py: feature extractor of baseline methods
  * util_train_data.py：data reading for TextCNN training
  * get_text_feature.py: generate text vector
  * get_image_feature.py & util_image_pca.py & get_fusion_feature.py: generate image vector and reduce the dimension to concatenate teogether
  * birch.py: cluster and prioritize
  * metric.py: the metrics
  * model.py & read_data.py: data reading and report object generation
  * stopwords1893.txt: the stopwords list



* Folder "statistical_analysis": it contains the python scripts to analyze the experimental data.
  * normal_test.py: normality test
  * statistic_tests.py: Kruskal-Wallis test, Wilcoxon signed-rank test, and Cohen's d

* Requirements
  * Matlab:<br>
    1、run the script "mySPMain.m" in the folder "SPM".<br>
    2、extract the image feature in the file "pyramids_all_200_3.mat".<br>
    3、obtain the image distance matrix in the file "SPDistanceMatrix-**.txt".<br>
