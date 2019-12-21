# coding: utf-8

import numpy as np

def find_add_erows(lst_no_anno, check_inds, k):
    """
    Finds pairs of repeated structures, representated as diagonals of a 
    certain length, k, that end at the same time step as 
    previously found pairs of repeated structures of the same length. 

    Args
    ----
    lst_no_anno: np.array
        list of pairs of repeats
        
    check_inds: np.array
        list of ending indices for repeats of length k that we use 
        to check lst_anno_no for more repeats of length k
        
    k: int
        length of repeats that we are looking for 

    Returns
    -------
    add_rows: np.array
        list of newly found pairs of repeats of length k that are 
        contained in larger repeats in lst_no_anno
    """

    L = lst_no_anno
    # Logical, which pairs of repeats have length greater than k?
    search_inds = (L[:,4] > k)

    #If there are no pairs of repeats that have a length greater than k
    if sum(search_inds) == 0:
        add_rows = np.full(1, False)
        return add_rows

    # Multiply ending index of all repeats "I" by search_inds
    EI = np.multiply(L[:,1], search_inds)
    # Multipy ending index of all repeats "J" by search_inds
    EJ = np.multiply(L[:,3], search_inds)

    #Loop over check_inds
    for i in range(check_inds.size): 

        ci = check_inds[i]

        # To check if the end index of the repeat "I" equals CI
        lnds = (EI == ci) 
        # To check if the end index of the right repeat of the pair equals CI
        rnds = (EJ == ci)

        #Left Check: Check for CI on the left side of the pairs
        if lnds.sum(axis = 0) > 0: #If the sum across (row) is greater than 0 
            # Find the 3rd entry of the row (lnds) whose starting index of 
            # repeat "J" equals CI
            EJ_li = L[lnds,3]
            
            # Number of rows in EJ_li 
            l_num = EJ_li.shape[0] 
            
            
            # Found pair of repeats on the left side
            one_lsi = L[lnds,1] - k + 1     #Starting index of found repeat i
            one_lei = L[lnds,1]             #Ending index of found repeat i
            one_lsj = EJ_li - k + 1         #Starting index of found repeat j
            one_lej = EJ_li                 #Ending index of found repeat j
            one_lk = k*np.ones((l_num,1))   #Length of found pair of repeats
            l_add = np.concatenate((one_lsi, one_lei, one_lsj, one_lej, one_lk), axis = None)

            
            # Found pair of repeats on the right side
            two_lsi = L[lnds,0]             #Starting index of found repeat i 
            two_lei = L[lnds,1] - k         #Ending index of ofund repeat i
            two_lsj = L[lnds,2]             #Starting index of found repeat j 
            two_lej = EJ_li - k             #Ending index of found repeat j
            two_lk = L[lnds, 4] - k         #Length of found pair of repeats 
            l_add_left = np.concatenate((two_lsi, two_lei, two_lsj, two_lej, two_lk), axis = None)
            
            # Stack the found rows vertically 
            add_rows = np.vstack((l_add, l_add_left))
            
            # Stack all the rows found on the left side of the pairs 
            add_rows = np.concatenate((add_rows, add_rows), axis = 0)
            
    
        #Right Check: Check for CI on the right side of the pairs
        elif rnds.sum(axis = 0) > 0:
            # Find the 1st entry of the row whose ending index of repeat 
            # "I" equals CI
            EI_ri = L[rnds, 1]
            # Number of rows in EJ_ri                    
            r_num = EI_ri.shape[0]
                               
            # Found pair of repeats on the left side 
            one_rsi = EI_ri - k + 1         #Starting index of found repeat i 
            one_rei = EI_ri                 #Ending index of found repeat i 
            one_rsj = L[rnds, 3] - k + 1    #Starting index of found repeat j
            one_rej = L[rnds,3]             #Ending index of found repeat j 
            one_rk = k*np.ones((r_num, 1))  #Length of found pair or repeats
            r_add = np.concatenate((one_rsi, one_rei, one_rsj, one_rej, one_rk), axis = None)
            
            # Found pairs on the right side 
            two_rsi = L[rnds, 0]            #Starting index of found repeat i  
            two_rei = EI_ri - k             #Ending index of found repeat i 
            two_rsj = L[rnds, 2]            #Starting index of found repeat j
            two_rej = L[rnds, 3] - k        #Ending index of found repeat j 
            two_rk = L[rnds, 4] - k         #Length of found pair or repeats
            r_add_right = np.concatenate((two_rsi, two_rei, two_rsj, two_rej, two_rk), axis = None) 
            
            # Stack the found rows vertically 
            add_rows = np.vstack((r_add, r_add_right))
            
            # Stack all the rows found on the right side of the pairs 
            add_rows = np.concatenate((add_rows, add_rows), axis = 0).astype(int)
            
            if add_rows.any() == None: 
                add_rows = np.full(1, False)
                return add_rows 
            else: 
                return add_rows
                
        #If there are no found pairs 
        else:
            add_rows = np.full(1, False)
            return add_rows 
