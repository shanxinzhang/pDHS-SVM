:pDHSdata_TIGR_model
# pDHS-SVM: A Prediction Method for Plant DNase I Hypersensitive Sites Based on Support Vector Machine

pDHS-SVM, focused on identifying DNase I Hypersensitive Sites in plant genome based on Support Vector Machine. 
Firstly To integrate the global sequence-order information and local DNA properties, reverse complement kmer and 
dinucleotide-based auto covariance of DNA sequences were applied to construct the feature space. In this work, 
fifteen physicochemical properties of dinucleotides were used and Support Vector Machine classifier was employed.
<br>

<b>Dependcy: </b><br>
1. Pse-in-one: http://bioinformatics.hitsz.edu.cn/Pse-in-One/server/ <br>
2. Libsvm: http://www.csie.ntu.edu.tw/~cjlin/libsvm/  <br>


<b>Input fasta file format(such as test.fas): </b><br>
>TAIR10_Chr5:1086-1272
ATCAATATAAGAACAACCCTCCTCATTTTAATTCCTTCTTGTCTACTTAGTTTAATATTTTCCAGCCGCA
ATGGGCCCATTAGCATCAACACCGGCCTATTTAGACGGCCCGTTATCTCCTCTTTGCCAATTTTCACCTT
CTGCAATGATATTGAAATTGAAGTAAATGCAAACAAAATAGTATGTT

NOTICE: The sequences used to train and test the model are in the file named TAIR10_DHS.rar .<br><br>
<b>How to use the tool, the command as follows: </b><br>
1.DownLoad the file
2.unpack the files
3.cd to the direction of the unpacked files
4. cd to the direction pDHSdata_TIGR_model, and run the command：
cat pDHSdata_TIGR_model_part1.txt pDHSdata_TIGR_model_part2.txt pDHSdata_TIGR_model_part3.txt pDHSdata_TIGR_model_part4.txt pDHSdata_TIGR_model_part5.txt pDHSdata_TIGR_model_part6.txt >../pDHSdata_TIGR_model.txt
cd ../
5.run the following command in command line environment:
  python pDHSSVM.py -inputfile=test.fas -outputfile=test_predict_out.txt -s 0

<br><br>
The output file have corresponding predicting results.
