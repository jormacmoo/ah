# -*- coding: utf-8 -*-
"""
Unit tests for Aligned Hierarchies, utilities.py

"""

import os
import sys
sys.path.insert(0, os.path.abspath('../ah/aligned-hierarchies'))
import unittest
import assemble
from assemble import breakup_overlaps_by_intersect
from assemble import check_overlaps
from assemble import __compare_and_cut as compare_and_cut
from assemble import __num_of_parts as num_of_parts
from assemble import __inds_to_rows as inds_to_rows
from assemble import __merge_based_on_length as merge_based_on_length
from assemble import __merge_rows as merge_rows
from assemble import hierarchical_structure
import numpy as np


class test_utilities(unittest.TestCase):

    def test_breakup_overlaps_by_intersect(self):
        input_pattern_obj = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                              [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                              [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]])
        bw_vec = np.array([[3],
                        [5],
                        [8],
                        [8]])
        thresh_bw = 0

        output = breakup_overlaps_by_intersect(input_pattern_obj, bw_vec, thresh_bw)

        expect_output0 = np.array([[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0],
                                [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]])

        expect_output1 = np.array([[3],
                                   [5]])
        
        self.assertIs(type(output), tuple)
        self.assertEqual(output[0].tolist(),expect_output0.tolist())
        self.assertEqual(output[1].tolist(),expect_output1.tolist())


    def test_check_overlaps(self):
        input_mat = np.array([[1, 1, 0, 1, 0, 0,],
                             [1, 1, 1, 0, 1, 0],
                             [0, 1, 1, 0, 0, 1],
                             [1, 0, 0, 1, 0, 0], 
                             [0, 1, 0, 0, 1, 0], 
                             [0, 0, 1, 0, 0, 1]])
        
        expect_output = np.array([[0,1,1,1,1,0],
                                [0,0,1,1,1,1],
                                [0,0,0,0,1,1],
                                [0,0,0,0,0,0],
                                [0,0,0,0,0,0],
                                [0,0,0,0,0,0]])
        
        output = check_overlaps(input_mat)

        self.assertIs(type(output), np.ndarray)
        self.assertEqual(np.size(output),np.size(expect_output))
        self.assertEqual(output.tolist(),expect_output.tolist())


    def test_compare_and_cut(self):
        red = np.array([1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        red_len = np.array([5])
        blue = np.array([1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0])
        blue_len = np.array([3])

        output = compare_and_cut(red, red_len, blue, blue_len)

        expect_output0  =np.array ([[1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,0,0],
                                [1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,0,0],
                                [0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0]])

        expect_output1 = np.array([[1],
                                [1],
                                [2]])


        self.assertIs(type(output), tuple)
        self.assertEqual(output[0].tolist(),expect_output0.tolist())
        self.assertEqual(output[1].tolist(),expect_output1.tolist())


    def test_num_of_parts_if_statement(self):
        input_vec = np.array([3, 4])
        input_start = np.array([0])
        input_all_starts = np.array([3, 7, 10])

        expect_output0 = np.array([ 6, 10, 13])
        expect_output1 = 2

        output = num_of_parts(input_vec,input_start,input_all_starts)

        self.assertIs(type(output), tuple)
        self.assertEqual(output[0].tolist(),expect_output0.tolist())
        self.assertEqual(output[1],expect_output1)
    

    def test_num_of_parts_else_statement(self):
        input_vec = np.array([3, 5])
        input_start = np.array([3])
        input_all_starts = np.array([3, 7, 10])

        expect_output0 = np.array([[3,7,10],
                                 [ 5,9,12]])
        expect_output1 = np.array([[1],
                                   [1]])

        output = num_of_parts(input_vec,input_start,input_all_starts)

        self.assertIs(type(output), tuple)
        self.assertEqual(output[0].tolist(),expect_output0.tolist())
        self.assertEqual(output[1].tolist(),expect_output1.tolist())


    def test_inds_to_rows(self):
        start_mat = np.array([0, 1, 6, 7])
        row_length = 10

        expect_output = np.array([[1,1,0,0,0,0,1,1,0,0]])

        output = inds_to_rows(start_mat,row_length)

        self.assertIs(type(output), np.ndarray)
        self.assertEqual(np.size(output),np.size(expect_output))
        self.assertEqual(output.tolist(),expect_output.tolist())


    def test_merge_based_on_length(self):
        full_mat = np.array([[0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0]])
        full_bw = np.array([[2],
                            [2]])
        target_bw = np.array([[2],
                            [2]])

        output = merge_based_on_length(full_mat,full_bw,target_bw)

        expect_output0 = np.array([[1,1,1,1,1,1,1,1,0,0,1,1,1,0,1,1,0,0,0,0]])
        expect_output1 = np.array([2])

        self.assertIs(type(output), tuple)
        self.assertEqual(output[0].tolist(),expect_output0.tolist())
        self.assertEqual(output[1].tolist(),expect_output1.tolist())


    def test_merge_rows(self):
        input_mat = np.array([[0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
                      [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0]])
        input_width = np.array([1])

        output = merge_rows(input_mat,input_width)

        expect_output = np.array([[1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,0,0]])

        self.assertIs(type(output), np.ndarray)
        self.assertEqual(np.size(output),np.size(expect_output))
        self.assertEqual(output.tolist(),expect_output.tolist())


    def test_hierarchical_structure(self):
        input_matrix_no = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        input_key_no = np.array([[5],
                                [10]])
        input_sn = 20

        output = hierarchical_structure(input_matrix_no,input_key_no,input_sn)

        expect_output0 = np.array([[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]])
        expect_output1 = np.array([[5]])
        expect_output2 = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]])

        self.assertIs(type(output), tuple)
        self.assertEqual(output[0].tolist(),expect_output0.tolist())
        self.assertEqual(output[1].tolist(),expect_output1.tolist())
        self.assertEqual(output[2].tolist(),expect_output2.tolist())



        
        
    
    
               
         
if __name__ == '__main__':
    unittest.main()