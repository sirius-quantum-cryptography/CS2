import numpy as np


def gen_matrix(num_params, only_syn_matrix=0,no_data=1): #no_data=1 - give only parities, no_data=0 - give parities with datas
    mat_cod = []
    mat_syn = []
    par_num = []
    dat_num = []

    for i in range(1, 2**(num_params)):
        in_byte = bin(i)[2:]
        bb = [True]
        ik = 0
        for ik in range(num_params - len(in_byte)):
            bb.append(False)
        ik = ik
        for il in range(len(in_byte)):
            bb.append(bool(int(in_byte[il])))
        if in_byte.count('1') == 1:
            par_num.append(i)
        else:
            dat_num.append(i)
        mat_syn.append(bb)
    bb = [True]
    for i in range(num_params):
        bb.append(False)
    mat_syn.append(bb)

    # ------------------------Syndrome Matrix
    Completed_Syndrome = np.matrix(mat_syn).transpose()
    if only_syn_matrix:
        return Completed_Syndrome

    for i in range(1, 2**num_params):
        dd = []
        if no_data:
            if i in par_num:
                for hj in range(2**num_params):
                    if (hj+1) in dat_num:
                        dd.append(Completed_Syndrome.item(num_params-par_num.index(i), hj))
                mat_cod.append(dd)
        else:
            if i in dat_num:
                for mk in range(dat_num.index(i)):
                    dd.append(False)
                dd.append(True)
                for mk in range(len(dat_num)-1-dat_num.index(i)):
                    dd.append(False)
                mat_cod.append(dd)
            else:
                for hj in range(2**num_params):
                    if (hj+1) in dat_num:
                        dd.append(Completed_Syndrome.item(num_params-par_num.index(i), hj))
                mat_cod.append(dd)
    # ------------------------Coder Matrix
    Completed_Coder = np.matrix(mat_cod)
    return (Completed_Coder, Completed_Syndrome)
