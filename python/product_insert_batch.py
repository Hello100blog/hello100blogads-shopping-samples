#!/usr/bin/python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Adds several products to the specified account, in a single batch."""

from __future__ import print_function
import json
import sys

import product_sample
import shopping_common

# Number of products to insert.
BATCH_SIZE = 5


def main(argv):
  # Authenticate and construct service.
  service, config, _ = shopping_common.init(argv, __doc__)
  merchant_id = config['merchantId']

  batch = {
      'entries': [{
          'batchId': i,
          'merchantId': merchant_id,
          'method': 'insert',
          'product': product_sample.create_product_sample(
              config,
              'book#%s' % shopping_common.get_unique_id(),
              title='This is book number %d' % i,
              price={
                  'value': '%d.50' % i,
                  'currency': 'USD',
              }),
          } for i in range(BATCH_SIZE)],
  }

  request = service.products().custombatch(body=batch)
  result = request.execute()

  if result['kind'] == 'content#productsCustomBatchResponse':
    entries = result['entries']
    for entry in entries:
      if not shopping_common.json_absent_or_false(entry, 'product'):
        product = entry['product']
        print('Product "%s" with offerId "%s" and title "%s" was created.' %
              (product['id'], product['offerId'], product['title']))
      elif not shopping_common.json_absent_or_false(entry, 'errors'):
        print('Errors for batch entry %d:' % entry['batchId'])
        print(json.dumps(entry['errors'], sort_keys=True, indent=2,
                         separators=(',', ': ')))
  else:
    print('There was an error. Response: %s' % result)


if __name__ == '__main__':
  main(sys.argv)
