load C:\Users\dywang\Desktop\Cluster\galac.txt
'Cazyase=Cazyase';
genes={'Noe'
    'Sulfate'
    'Both'
    'O2'};
times={'0' '2' '9' '16' '23' '30'};
cg_s=clustergram(galac, 'Cluster','column','Standardize','none','Colormap',redbluecmap,'Rowlabels',genes,'Columnlabels',times);
set(cg_s,'Symmetric', 'false', 'DisplayRange',0.15);
%cg_s=clustergram(Acetate,'Cluster','Column','Standardize','row','Colormap', redbluecmap,'Rowlabels',genes,'Columnlabels',times);