# -*- coding: utf-8 -*-
import os

import numpy as np
import pandas as pd


def getIDs():
    def getData(ss):
        items = ss[8].split(';')
        data = {'ID': items[0].split('=')[1], 'product': np.nan, 'ko': np.nan}
        for item in items:

            for key in data:
                if item.startswith(key + '='):
                    data[key] = item.split('=')[1]
        return data

    # Note splite different columns
    df = pd.read_table(r'D:\Program\Python\homeworkpython\Test\Combine\Ga0526687_functional_annotation.gff',
                       header=None)
    df2 = df.apply(lambda x: getData(x), axis=1, result_type='expand')
    df2.to_pickle(r'D:\Program\Python\homeworkpython\Test\Combine\Ga0526687_functional_annotationIDs.dat')


def combineText():
    dfFinal = None
    for i in range(12):
        file = os.path.join(
            r'D:\Program\Python\HomeWorkPython\Test\Combine\Annotation_B1', 'PanC_082922_N3_SF{0:02d}.SE.pro.txt'.format(i + 1)
        )
        if os.path.exists(file):
            df = pd.read_table(file, comment='#').loc[:, ['ProteinID', 'Run1_NormalizedBalancedSpectrumCounts']]
            df['ProteinID'] = df['ProteinID'].str.replace('[\{\}]', '', regex=True).apply(lambda x:x.split(',')[0])
            df = df.reset_index(drop=True)
            df.columns = ['ProteinID', 'SpectrumCounts@SF{0:02d}'.format(i + 1)]
            if dfFinal is None:
                dfFinal = df
            else:
                dfFinal = pd.merge(dfFinal, df, on='ProteinID', how='outer')

    df = pd.read_pickle(r'D:\Program\Python\homeworkpython\Test\Combine\Ga0526687_functional_annotationIDs.dat')
    dfFinal = pd.merge(dfFinal, df, left_on='ProteinID', right_on='ID', how='left')
    df2 = pd.read_table(r'D:\Program\Python\homeworkpython\Test\Combine\gene_phylogeny.tsv',header=None)
    df2.columns=['ID2','A','B','C','Info']
    df2=df2.loc[:,['ID2','Info']]
    dfFinal = pd.merge(dfFinal, df2, left_on='ProteinID', right_on='ID2', how='left')
    dfFinal.to_csv('final.csv', index=False)
    print(dfFinal)


if __name__ == '__main__':
    # getIDs()
    combineText()
