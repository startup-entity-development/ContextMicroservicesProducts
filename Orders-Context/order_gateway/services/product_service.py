import os
import requests

PRODUCT_GATEWAY_HOST_NAME = os.environ.get("PRODUCT_GATEWAY_HOST_NAME")
product_public_service_url = f'{PRODUCT_GATEWAY_HOST_NAME}/public/product/gateway_graphql'

def resolve_getProductById(product_id):
    query = '''
    query {
      productById(productId: "%s") {
      id
      subCategoryId
      name
      title
      brand
      description
      upcBarcode
      unitMeasure
      weight
      size
      unitInPack
      baseIncrement
      wordsTags
      isActive
      retailerEdge {
        edges {
          node {
            id
            retailer{
                name
                description
              }
            retailerId
            productId
            linkUrl
            price
            stock
            isActive
            isInStock
          }
        }
      }
      mediaEdge{
          edges{
            node{
              id
              linkUrl
              isMain
              mediaType
            }
          }
        }
      }
    }
    ''' % product_id

    response = requests.post(product_public_service_url, json={'query': query})
    data = response.json()
    product_data = data.get('data', {}).get('productById', {})
    return product_data

def resolve_getProductsByIds(product_ids):
    query = '''
    query GetProductsByIds($productIds: [ID]!) {
      productsByListIds(listId: $productIds) {
      id
      subCategoryId
      name
      title
      brand
      description
      upcBarcode
      unitMeasure
      weight
      size
      unitInPack
      baseIncrement
      wordsTags
      isActive
      retailerEdge {
        edges {
          node {
            id
            retailerId
            productId
            linkUrl
            price
            stock
            isActive
            isInStock
          }
        }
      }
        mediaEdge{
          edges{
            node{
              id
              linkUrl
              isMain
              mediaType
            }
          }
        }
      }
    }
    '''

    # Prepare the variables dictionary
    variables = {'productIds': [str(product_id) for product_id in product_ids]}

    response = requests.post(product_public_service_url, json={'query': query, 'variables': variables})
    data = response.json()
    product_data = data.get('data', {}).get('productsByListIds', {})
    sorted_products = __sort_products(product_data, product_ids)
    return sorted_products

def __sort_products(product_data, product_ids):
    return sorted(product_data, key=lambda product: product_ids.index(product['id']))
