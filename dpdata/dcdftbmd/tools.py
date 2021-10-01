import dpdata
import numpy as np



def load_dcdftbmd_md_set(
        source_folder, begin, step, train_ratio=0.9):
    
    all_set = dpdata.LabeledSystem(
        source_folder, fmt='dcdftbmd', begin=begin, step=step)
   
    nsets = all_set.get_nframes()
    all_set.shuffle()

    ntrains = int(nsets*train_ratio)

    training_set = all_set.sub_system(np.arange(ntrains))
    valid_set = all_set.sub_system(np.arange(ntrains+1, nsets))
    
    return training_set, valid_set
