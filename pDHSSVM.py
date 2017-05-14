__author__ = 'Shanxin Zhang'

import sys
import re
import time
import os
import itertools
import const

from util import frequency, read_k,check_args,read_fasta
from data import index_list
from kmer import make_kmer_vector
from acc  import acc
    

def main(args):
	
    names=[]
    with open(args.inputfile) as af:
        seq_list=read_fasta(af)
        for e in seq_list:
            names.append(e.name)
    #kmer.py -f tab -l +1 -r 1 -k ',num2str(k),' TAIR10_DHSs.fas TAIR10_DHSs_reckmer_',num2str(k),'.txt DNA'
    res_kmer = make_kmer_vector(k=2, alphabet=index_list.DNA, filename=args.inputfile, revcomp=True)  
    #acc.py -e user_indices.txt -f svm -l +1 -lag ',num2str(lag),' TAIR10_DHSs.fas TAIR10_DHSs_dac_',num2str(lag),'.txt DNA DAC'
        if args.s==0:
        model_file='pDHSdata_TAIR_model.txt'
        lag=3
    else:
        model_file='pDHSdata_TIGR_model.txt'
        lag=8
    with open(args.inputfile) as f:
        k = read_k('DNA', 'DAC', 0)
        ind_list=[]
        res_acc = acc(f, k, lag, ind_list, index_list.DNA, extra_index_file='user_indices.txt', all_prop=False, theta_type=1)
    # features= revckmer+dac,formed by add each row
    res=[]
    for i in range(len(res_kmer)):
        res.append(res_kmer[i]+res_acc[i])
    featuresfile=args.inputfile+'_tmp_features.txt'
    # Write correspond res file.
    from util import write_libsvm
    write_libsvm(res, ['+1'] * len(res), featuresfile)

    #predict the result
    tmp_predict_result_file=args.inputfile+'_tmp_result.txt'
    if sys.platform == 'win32':
        options='svm-predict -b 1 -q '+featuresfile+' '+model_file+' '+ tmp_predict_result_file
    else:
        options='./svm-predict -b 1 -q '+featuresfile+' '+model_file+' '+ tmp_predict_result_file
    os.system(options)
    pf=open(args.outputfile,'w')
    with open(tmp_predict_result_file) as nf:
            label, TrueProb, FalseProb= '', '',''
            count = 0
            while True:
                line = nf.readline().strip()
                if not line:
                    break
                if count>len(names):
                    break
                if 0==count:
                     pf.write('ID\t\tLabel\t\tProb\n')
                     count+=1
                     continue
                label=int(line.split()[0])
                TrueProb=line.split()[1]
                FalseProb=line.split()[2]
                if label==-1:
                    pf.write(names[count-1]+'\t\t'+'Non DHS'+'\t\t'+str(FalseProb)+'\n')
                else:                
                    pf.write(names[count-1]+'\t\t'+'DHS'+'\t\t'+str(TrueProb)+'\n')
                count+=1
    pf.close()
    cwd = os.getcwd()
    files = [x for x in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(cwd,x))]
    #print files 
    for file in files:
        if -1 != file.find('tmp'):
            os.remove(file)
        
if __name__ == '__main__':
    import argparse
    from argparse import RawTextHelpFormatter

    parse = argparse.ArgumentParser(description="This is the module for generate DHSs predictor in plant genome based on support vector machine.",
                                    formatter_class=RawTextHelpFormatter)
    parse.add_argument('-inputfile',
                       help="The input file in FASTA format.")
    parse.add_argument('-outputfile', default='predict_out.txt',
                       help="The output file stored results. default output file name is predict_out.txt")
    parse.add_argument('-s', default=0,
                       help="The plant species,0 is Arabidopsis thaliana, 1 is rice (Oryza sativa),default is 0.")
	
    args = parse.parse_args()

    print("Calculating...")
    start_time = time.time()
    main(args)
    print("Done.")
    print("Used time: %ss" % (time.time() - start_time))
