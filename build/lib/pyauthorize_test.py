#!/usr/bin/env python
#Copyright (C) 2010 Analyte Media
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
#conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""Test suite for PyAuthorize."""

__author__ = 'jordan.bouvier@analytemedia.com (Jordan Bouvier)'

from nose.tools import with_setup
from nose import tools
import datetime
import random
import unittest

import pyauthorize



class PyAuthorizeTest(unittest.TestCase):
    
    def setUp(self):
        """Setup fixture."""
        
        x_login = 'your login'
        x_tran_key = 'your transaction key'
        self.pp = pyauthorize.PaymentProcessor(x_login, x_tran_key)
        self.pp.x_post_url = 'https://test.authorize.net/gateway/transact.dll'
        
        # Default card number and exp date
        self.pp.card_num = '4111111111111111'
        self.pp.exp_date = datetime.date.today().strftime('%m%Y')
        

class PyAuthorize_transactionTest(PyAuthorizeTest):
    """Tests pertaining to _transaction."""
    
    def test__transaction(self):
        """Check that _transaction recognizes a valid transaction number."""
        
        trans_id = str(random.randint(10000000,99999999))
        self.pp.transaction = trans_id
        response = self.pp._transaction()
        tools.assert_equal(trans_id, response)
    
    @tools.raises(ValueError)
    def test__transaction_fails_when_uninitialized(self):
        """Check that _transaction fails when transaction hasn't been set."""
        
        response = self.pp._transaction()
    
    @tools.raises(ValueError)
    def test__transaction_fails_with_letters(self):
        """_transaction raises ValueError when letters are in transaction."""
        
        self.pp.transaction = '389fejk90'
        response = self.pp._transaction()
    
    @tools.raises(ValueError)
    def test__transaction_fails_with_symbols(self):
        """_transaction raises ValueError when symbols are in transaction."""
        
        self.pp.transaction = '238932409432&893209'
        response = self.pp._transaction()
        

class PyAuthorize_addressTest(PyAuthorizeTest):
    """Tests pertaining to _address."""
    
    def test__address(self):
        """_address recognizes a valid address."""
        
        address = '351 W Hubbard St. Suite 500'
        self.pp.address = address
        response = self.pp._address()
        tools.assert_equal(address, response)
    
    @tools.raises(ValueError)
    def test__address_fails_when_uninitialized(self):
        """_address fails when address hasn't been set."""
        
        self.pp._address()
    
    @tools.raises(ValueError)
    def test__address_fails_with_invalid_characters(self):
        """_address fails when the address has invalid chars."""
        
        self.address = '*'
        self.pp._address()
    

class PyAuthorize_zipTest(PyAuthorizeTest):
    """Tests pertaining to _zip."""
    
    def test__zip(self):
        """_zip recognizes a valid zip."""
        
        zip_code = '60654'
        self.pp.zip = zip_code
        response = self.pp._zip()
        tools.assert_equal(zip_code, response)
        
        zip_code = '606541234'
        self.pp.zip = zip_code
        response = self.pp._zip()
        tools.assert_equal(zip_code, response)
    
    @tools.raises(ValueError)
    def test__zip_fails_when_uninitialized(self):
        """_zip fails when the zip code hasn't been set."""
        
        self.pp._zip()
    
    @tools.raises(ValueError)
    def test__zip_fails_with_invalid_characters(self):
        """_zip fails if it encounters a non-number"""
        
        self.zip = 'a1234'
        self.pp._zip()
    
    @tools.raises(ValueError)
    def test__zip_fails_with_invalid_length(self):
        """_zip fails if it is not 5 or 9 digits long."""
        
        self.zip = '123456'
        self.pp._zip()
    

class PyAuthorize_card_num_last_fourTest(PyAuthorizeTest):
    """Tests pertaining to _card_num_last_four."""
    
    def test__card_num_last_four(self):
        """_card_num_last_four recognizes a valid final four cc digits."""
        
        last_four = '7890'
        self.pp.card_num = last_four
        response = self.pp._card_num_last_four()
        tools.assert_equal(last_four, response)
    
    @tools.raises(ValueError)
    def test__card_num_last_four_fails_when_uninitialized(self):
        """_card_num_last_four fails if card_num isn't set."""
        
        self.pp.card_num = None
        self.pp._card_num_last_four()
    
    @tools.raises(ValueError)
    def test__card_num_last_four_fails_with_invalid_characters(self):
        """_card_num_last_four fails if it encounters a non-number."""
        
        self.pp.card_num = '76%8'
        self.pp._card_num_last_four()
    
    @tools.raises(ValueError)
    def test__card_num_last_four_fails_with_invalid_length(self):
        """_card_num_last_four fails if it is not four digits long."""
        
        self.pp.card_num = '123456'
        self.pp._card_num_last_four()
    

class PyAuthorize_card_numTest(PyAuthorizeTest):
    """Tests pertaining to _card_num."""
    
    def test__card_num(self):
        """_card_num recognizes a valid card number."""
        
        card_num = '4111111111111111'
        self.pp.card_num = card_num
        response = self.pp._card_num()
        tools.assert_equal(card_num, response)
        
        card_num = '511111111111111'
        self.pp.card_num = card_num
        response = self.pp._card_num()
        tools.assert_equal(card_num, response)
        
    @tools.raises(ValueError)
    def test__card_num_fails_when_uninitialized(self):
        """_card_num fails if card_num isn't set."""
        
        self.pp.card_num = None
        self.pp._card_num()
        
    @tools.raises(ValueError)
    def test__card_num_fails_with_invalid_characters(self):
        """_card_num fails if it encounters a non-number."""
        
        self.pp.card_num = '41111111111176%8'
        self.pp._card_num()
        
    def test__card_num_fails_with_invalid_length(self):
        """_card_num fails if it is not between 13 and 16 digits long."""
        
        # Check lengths 1 to 12
        self.pp.card_num = '4'
        while len(self.pp.card_num) < 13:
            tools.assert_raises(ValueError, self.pp._card_num)
            self.pp.card_num = '%s2' % self.pp.card_num
            
        # Check lengths over 16
        self.pp.card_num = '42222222222222222'
        tools.assert_raises(ValueError, self.pp._card_num)
    

class PyAuthorize_card_num_or_last_fourTest(PyAuthorizeTest):
    """Tests pertaining to _card_num_or_last_four."""
    
    def test__card_num_or_last_four(self):
        """_card_num_or_last_four recognizes a valid card number."""
        
        card_nums = ['4111111111111111', '511111111111111', '1111']
        for card_num in card_nums:
            self.pp.card_num = card_num
            response = self.pp._card_num_or_last_four()
            tools.assert_equal(card_num, response)
    
    @tools.raises(ValueError)
    def test__card_num_or_last_four_fails_when_uninitialized(self):
        """_card_num_or_last_four fails if card_num isn't set."""
        
        self.pp.card_num = None
        self.pp._card_num_or_last_four()
    
    @tools.raises(ValueError)
    def test__card_num_or_last_four_fails_with_invalid_characters(self):
        """_card_num_or_last_four fails if it encounters a non-number."""
        
        self.pp.card_num = '41111111111176%8'
        self.pp._card_num_or_last_four()
    
    def test__card_num_or_last_fourm_fails_with_invalid_length(self):
        """_card_num_or_last_four fails if it is not a valid length.
        
        Valid lengths are 4, 13, 14, 15, or 16 characters."""
        
        # Check all lengths 1 to 20
        self.pp.card_num = '4'
        
        while len(self.pp.card_num) <= 20:
            if len(self.pp.card_num) in [4, 13, 14, 15, 16]:
                response = self.pp._card_num_or_last_four()
                tools.assert_equal(self.pp.card_num, response)
            else:
                tools.assert_raises(ValueError,
                        self.pp._card_num_or_last_four)
                
            self.pp.card_num = '%s2' % self.pp.card_num
            

class PyAuthorize_card_codeTest(PyAuthorizeTest):
    """Tests pertaining to _card_code."""
    
    def test__card_code(self):
        """_card_num has 3 or 4 integers."""
        
        card_code = '123'
        self.pp.card_code = card_code
        response = self.pp._card_code()
        tools.assert_equal(card_code, response)
        
        card_code = '1234'
        self.pp.card_code = card_code
        response = self.pp._card_code()
        tools.assert_equal(card_code, response)
    
    @tools.raises(ValueError)
    def test__card_code_fails_when_uninitialized(self):
        """_card_code fails if card_code is not set."""
        
        self.pp._card_code()
    
    @tools.raises(ValueError)
    def test__card_code_fails_with_invalid_characters(self):
        """_card_code fails if it encounters a non-number."""
        
        self.pp.card_code = '12a'
        self.pp._card_code()
    
    @tools.raises(ValueError)
    def test__card_code_fails_with_invalid_length(self):
        """_card_code fails if it is not 3 or 4 characters."""
        
        self.pp.card_code = '12345'
        self.pp._card_code()
    

class PyAuthorize_exp_dateTest(PyAuthorizeTest):
    """Tests pertaining to _exp_date."""
    
    def test__exp_date(self):
        """_exp_date matches a valid format.
        
        Valid formats:
            MMYY, MMYYYY, MM/YY, MM-YY, MM/YYYY, MM-YYYY
        """
        
        exp_dates = ['0112', '012012', '01/12', '01/2012', '01-12', '01-2012']
        
        for exp_date in exp_dates:
            self.pp.exp_date = exp_date
            response = self.pp._exp_date()
            tools.assert_equal(exp_date, response)
    
    @tools.raises(ValueError)
    def test__exp_date_fails_when_uninitialized(self):
        """_exp_date fails when exp_date isn't set."""
        
        self.pp.exp_date = None
        self.pp._exp_date()
    
    @tools.raises(ValueError)
    def test__exp_date_fails_with_invalid_characters(self):
        """_exp_date fails if it encounters an invalid character."""
        
        self.pp.exp_date = 'September 2012'
        self.pp._exp_date()
    

class PyAuthorize_amountTest(PyAuthorizeTest):
    """Tests pertaining to _amount."""
    
    def test__amount(self):
        """Test that _amount recognizes a valid amount."""
        
        amount = '12.00'
        self.pp.amount = amount
        response = self.pp._amount()
    
    @tools.raises(ValueError)
    def test__amount_fails_when_uninitialized(self):
        """_amount fails when amount isn't set."""
        
        self.pp._amount()
    
    @tools.raises(ValueError)
    def test__amount_fails_with_invalid_characters(self):
        """_amount fails when amount is an invalid value."""
        
        self.pp.amount = '12 dollars'
        self.pp._amount()
    

class PyAuthorizeProcessingTest(PyAuthorizeTest):
    """Tests related to actual processing of transactions."""
    
    def test_auth_only_success(self):
        """auth_only can successfully submit a transaction."""
        
        self.pp.amount = '1.00'
        self.pp.auth_only()
        response = self.pp.process()
        tools.eq_(response, True)
    
    def test_auth_only_fails_without_amount(self):
        """auth_only fails if amount is not set or is invalid."""
        
        self.pp.amount = None
        tools.assert_raises(ValueError, self.pp.auth_only)
        
        self.pp.amount = 'A lot of money'
        tools.assert_raises(ValueError, self.pp.auth_only)
    
    def test_auth_only_fails_without_exp_date(self):
        """auth_only fails if exp_date is not set or is invalid."""
        
        self.pp.exp_date = None
        tools.assert_raises(ValueError, self.pp.auth_only)
        
        self.pp.exp_date = 'This card never expires!'
        tools.assert_raises(ValueError, self.pp.auth_only)
    
    def test_auth_only_fails_without_card_num(self):
        """auth_only failse if card_num is not set or is invalid."""
        
        self.pp.card_num = None
        tools.assert_raises(ValueError, self.pp.auth_only)
        
        self.pp.card_num = '42'
        tools.assert_raises(ValueError, self.pp.auth_only)
    
    
    def test_auth_and_capture_success(self):
        """auth_and_capture can successfully submit a transaction."""
        
        self.pp.amount = '1.00'
        self.pp.auth_and_capture()
        response = self.pp.process()
        tools.eq_(response, True)
    
    def test_auth_and_capture_fails_without_amount(self):
        """auth_and_capture fails if amount is not set or is invalid."""
        
        self.pp.amount = None
        tools.assert_raises(ValueError, self.pp.auth_and_capture)
        
        self.pp.amount = 'A lot of money'
        tools.assert_raises(ValueError, self.pp.auth_and_capture)
    
    def test_auth_and_capture_fails_without_exp_date(self):
        """auth_and_capture fails if exp_date is not set or is invalid."""
        
        self.pp.exp_date = None
        tools.assert_raises(ValueError, self.pp.auth_and_capture)
        
        self.pp.exp_date = 'This card never expires!'
        tools.assert_raises(ValueError, self.pp.auth_and_capture)
    
    def test_auth_and_capture_fails_without_card_num(self):
        """auth_and_capture failse if card_num is not set or is invalid."""
        
        self.pp.card_num = None
        tools.assert_raises(ValueError, self.pp.auth_and_capture)
        
        self.pp.card_num = '42'
        tools.assert_raises(ValueError, self.pp.auth_and_capture)
    
    
    def test_prior_auth_capture_success(self):
        """prior_auth_capture can successfully complete."""
        
        # Authorize.net actually does not provide a mechanism for testing
        # this functionality.
        # TODO: Mock this
        pass
    
    def test_prior_auth_capture_fails_without_transaction(self):
        """prior_auth_capture fails without transaction."""
        
        # Fails without any transaction id
        tools.assert_raises(ValueError, self.pp.prior_auth_capture)
        
        # Fails with an invalid transaction id
        self.pp.transaction = 'Tom foolery!'
        tools.assert_raises(ValueError, self.pp.prior_auth_capture)
    
    def test_prior_auth_capture_fails_with_invalid_amount(self):
        """prior_auth_capture fails if amount is specified but is invalid."""
        
        self.pp.amount = 'five trillion dollars'
        self.pp.transaction = '123123'
        tools.assert_raises(ValueError, self.pp.prior_auth_capture)
    
    def test_prior_auth_capture_handles_none_amount(self):
        """prior_auth_capture should handle unset amount correctly."""
        
        self.pp.amount = None
        self.pp.transaction = '123123'
        self.pp.prior_auth_capture()
        assert 'x_amount' not in self.pp.transaction_data
    
    
    def test_void_success(self):
        """void can successfully complete"""
        
        # Authorize.net doesn't provide any mechanism for testing void.
        # TODO: Mock this
        pass
    
    def test_void_fails_without_transaction(self):
        """void fails if transaction is invalid or not set."""
        
        tools.assert_raises(ValueError, self.pp.void)
        
        self.pp.transaction = '&^#@*()'
        tools.assert_raises(ValueError, self.pp.void)
    
    
    def test_credit_success(self):
        """credit can successfully complete."""
        
        # Authorize.net doesn't provide any mechanism for testing credit
        # TODO: Mock it
        pass
    
    def test_credit_fails_without_transaction(self):
        """credit fails if transaction is unset or invalid."""
        
        self.pp.amount = '12.00'
        
        tools.assert_raises(ValueError, self.pp.credit)
        
        self.pp.transaction = '&^#@*()'
        tools.assert_raises(ValueError, self.pp.credit)
    
    def test_credit_fails_without_amount(self):
        """credit fails if amount is unset or invalid."""
        
        self.pp.transaction = '123123'
        
        tools.assert_raises(ValueError, self.pp.credit)
        
        self.pp.amount = '&^#@*()'
        tools.assert_raises(ValueError, self.pp.credit)
    
    def test_credit_fails_without_card_num(self):
        """credit fails if card_num is unset or invalid."""
        
        self.pp.card_num = None
        self.pp.transaction = '123123'
        self.pp.amount = '12.00'
        
        tools.assert_raises(ValueError, self.pp.credit)
        
        self.pp.card_num = 'IOU'
        tools.assert_raises(ValueError, self.pp.credit)
    
    def test_auth_fails_with_avs_fields_missing(self):
        """processing fails if avs is enabled and avs fields are missing."""
        
        self.pp.amount = '12.00'
        self.pp.is_avs_required = True
        
        self.pp.address = None
        self.pp.zip = '60654'
        tools.assert_raises(ValueError, self.pp.auth_only)
        
        self.pp.zip = None
        self.pp.address = '1600 Pennsylvania Ave'
        tools.assert_raises(ValueError, self.pp.auth_only)
    
    def test_auth_fails_with_ccv2_fields_missing(self):
        """processing fails if ccv2 is enabled and card_code is invalid."""
        
        self.pp.amount = '12.00'
        self.pp.is_ccv_required = True
        
        self.card_code = 'this is totally wrong'
        tools.assert_raises(ValueError, self.pp.auth_only)
    

