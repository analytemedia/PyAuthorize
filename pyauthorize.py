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


"""Module for processing credit card transactions through Authorize.net."""

__author__ = 'jordan.bouvier@analytemedia.com (Jordan Bouvier)'


from urllib import urlencode
import re
import urllib2



class PaymentProcessor(object):
    """Process payments using Authorize.net AIM gateway.
    
    To initialize you must pass your x_login and x_tran_key:
    >>> p = PaymentProcessor(x_login='abcdef', x_tran_key='abc123')
    
    By default, it will always run in test mode. You must explicitely
    enable production mode by passing x_test_request=False:
    >>> p = PaymentProcessor(x_login='abcdef', x_tran_key='abc123',
    ...         x_test_request=True)
    """
    
    def __init__(self, x_login, x_tran_key, x_test_request=True):
        # Configuration
        self.post_url = 'https://secure.authorize.net/gateway/transact.dll'
        self.x_test_request = x_test_request
        self.is_avs_required = False
        self.is_ccv_required = False
        self.configuration = {
                'x_login' : x_login,
                'x_tran_key' : x_tran_key,
                'x_version' : '3.1',
                'x_relay_response' : 'FALSE',
                'x_delim_data' : 'TRUE',
                'x_delim_char' : '|',
                'x_method': 'CC',
        }
        
        # Variable initialization
        self.transaction = None
        self.card_num = None
        self.exp_date = None
        self.amount = None
        self.card_code = None
        self.address = None
        self.zip = None
        self.invoice_number = None
        self.first_name = None
        self.last_name = None
        self.customer_id = None
        self.description = None
        
        self.transaction_data = {}
        self.response_code = None
        self.reason_code = None
        self.reason_text = None
        self.approval_code = None
        self.avs_response = None
        self.trans_id = None
        self.ccv_response = None
        
    def auth_only(self):
        """Setup to process an authorization only."""
        
        self._auth()
        self.transaction_data['x_type'] = 'AUTH_ONLY'
        
    def auth_and_capture(self):
        """Setup to process an authorization and immediate capture."""
        
        self._auth()
        self.transaction_data['x_type'] = 'AUTH_CAPTURE'
        
    def prior_auth_capture(self):
        """Setup to process a previously authorized transaction."""
        
        self.transaction_data['x_type'] = 'PRIOR_AUTH_CAPTURE'
        self.transaction_data['x_trans_id'] = self._transaction()
        
        if self.amount:
            self.transaction_data['amount'] = self._amount()
        else:
            self.transaction_data['amount'] = None
            
    def void(self):
        """Setup for a void transaction."""
        
        self.transaction_data['x_type'] = 'VOID'
        self.transaction_data['x_trans_id'] = self._transaction()
        
    def credit(self):
        """Setup for a credit transaction."""
        
        self.transaction_data['x_type'] = 'CREDIT'
        self.transaction_data['x_trans_id'] = self._transaction()
        self.transaction_data['x_card_num'] = self._card_num()
        self.transaction_data['x_amount'] = self._amount()
        
    def process_void_or_credit(self):
        """Attempt a void and process a full credit if not possible."""
        
        self.void()
        is_processed = self.process()
        if not is_processed:
            self.credit()
            is_processed = self.process()
            transaction_type = 'Credit'
        else:
            transaction_type = 'Void'
            
        return (is_processed, transaction_type)
        
    def process(self):
        """Actually process the transaction.
        
        Returns:
            True if the transaction was successful.
            False in every other case.
        """
        
        # Set transaction type
        self.configuration['x_test_request'] = str(self.x_test_request)
        post_list = ([urlencode(self.configuration),
                      urlencode(self.transaction_data)])
        encoded_post_data = '&'.join(post_list)
        
        request = urllib2.Request(url=self.post_url,
                data=encoded_post_data)
        response = urllib2.urlopen(request)
        response_string = response.read()
        response_list = response_string.split(
                self.configuration['x_delim_char'])
                
        self.response_code = response_list[0]
        self.reason_code = response_list[2]
        self.reason_text = response_list[3]
        self.approval_code = response_list[4]
        self.avs_response = response_list[5]
        self.trans_id = response_list[6]
        self.ccv_response = response_list[39]
        
        if str(self.response_code) == '1':
            return True
        else:
            return False
            
    def _transaction(self):
        """Validate the transaction id and return it if successful."""
        if not self.transaction:
            raise ValueError, 'transaction is required.'
        elif not re.search('^\d+$', self.transaction):
            raise ValueError, ('Invalid transaction format. %s'
                               % self.transaction)
        else:
            return self.transaction
    
    def _address(self):
        """Validate the address and return it if successful."""
        if not self.address:
            raise ValueError, 'address is required.'
        elif not re.search('^[\w. ]{1,60}$', self.address):
            raise ValueError, 'Invalid address format. %s' % self.address
        else:
            return self.address
    
    def _zip(self):
        """Validate the zip code and return it if successful."""
        if not self.zip:
            raise ValueError, 'zip is required.'
        elif not re.search('^\d{5}$|^\d{9}$', str(self.zip)):
            raise ValueError, 'Invalid zip format. %s' % str(self.zip)
        else:
            return str(self.zip)
    
    def _card_num_last_four(self):
        """Validate the credit card last four and return it if successful."""
        if not self.card_num:
            raise ValueError, 'card_num is required.'
        elif not re.search('^\d{4}$|^\d{13,16}$', str(self.card_num)):
            raise ValueError, ('Invalid card_num_last_four format. %s'
                               % str(self.card_num))
        else:
            return str(self.card_num)
    
    def _card_num(self):
        """Validate the credit card number and return it if successful."""
        if not self.card_num:
            raise ValueError, 'card_num is required'
        elif not re.search('^\d{13,16}$', str(self.card_num)):
            raise ValueError, 'Invalid card_num format. %s' % self.card_num
        else:
            return str(self.card_num)
    
    def _card_code(self):
        """Validate the card code and return it if successful."""
        if not self.card_code:
            raise ValueError, 'card_code is required.'
        elif not re.search('^\d{3,4}$', str(self.card_code)):
            raise ValueError, 'Invalid card_code format. %s' % self.card_code
        else:
            return str(self.card_code)
    
    def _exp_date(self):
        """Validate the expiration date and return it if successful."""
        expiration_string = ('^[0-1]{1}[0-9]{1}[-/]{0,1}[0-9]{2}$'
                             '|^[0-1]{1}[0-o{1}][-/]{0,1}20[0-9]{2}$')
        if not self.exp_date:
            raise ValueError, 'exp_date is required.'
        elif not re.search(expiration_string, str(self.exp_date)):
            raise ValueError, 'Invalid exp_date format. %s' % self.exp_date
        else:
            return self.exp_date
    
    def _amount(self):
        """Validate the amount and return it if successful."""
        
        if not self.amount:
            raise ValueError, 'amount is required'
        else:
            # Authorize.net will take anything that can be float-ed
            float(self.amount)
        
        return self.amount
    
    def _auth(self):
        """Setup to process an authorization."""
        
        self.transaction_data['x_card_num'] = self._card_num()
        self.transaction_data['x_exp_date'] = self._exp_date()
        self.transaction_data['x_amount'] = self._amount()
        
        if self.is_avs_required:
            self.transaction_data['x_address'] = self._address()
            self.transaction_data['x_zip'] = self._zip()
        
        if self.is_ccv_required:
            self.transaction_data['x_card_code'] = self._card_code()
        
        if self.invoice_number:
            self.transaction_data['x_invoice_num'] = self.invoice_number
        
        if self.first_name:
            self.transaction_data['x_first_name'] = self.first_name
        
        if self.last_name:
            self.transaction_data['x_last_name'] = self.last_name
        
        if self.customer_id:
            self.transaction_data['x_customer_id'] = self.customer_id
        
        if self.description:
            self.transaction_data['x_description'] = self.description
    
