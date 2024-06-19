import os
from typing import List
from flask import request
import requests

PRICING_GATEWAY_HOST_NAME = os.environ.get("PRICING_GATEWAY_HOST_NAME","http://pricing_gateway:3054")
pricing_protected_service_url = f'{PRICING_GATEWAY_HOST_NAME}/protected/pricing/gateway_graphql'

def resolve_cartPricingCalculation(sub_total:float, total_pounds:float, coupon_codes: List[str] = ["1111"]) :
    query = '''
   query cartPricingCalculation($subTotal: Float!, $totalPounds: Float, $couponCodes: [String]) {
  cartPricingCalculation(
    subTotal: $subTotal
    totalPounds: $totalPounds
    couponCodes: $couponCodes
    
  ) {

    id
    subTotal
    minimumSubtotal
    tax
    taxPercent
    tips
    total

    accountPromotionEdge{
      edges{
        node{
          id
          isActive
          promotionsCounter
        }
      }
    }

    deliveryService{
      deliveryFee
      discountDelivery
      typePromotion
      totalDelivery
      idPromotion
      idAccountPromotion
    }

    serviceFee{
      serviceFee
      discountService
      typePromotion
      totalService
      idPromotion
      idAccountPromotion
    }

    }
}
    
''' 
    account_name = request.headers.get('X-Auth-User')
    bearer_token = request.headers.get('Authorization')
    headers = {
        'Authorization': bearer_token,
        'X-Auth-User': account_name
    }
    variables = {'subTotal': sub_total, 'totalPounds': total_pounds, 'couponCodes': coupon_codes}

    response = requests.post(pricing_protected_service_url, json={'query': query,'variables': variables}, headers=headers)
    data = response.json()
    pricing_data = data.get('data', {}).get('cartPricingCalculation', {})
    return pricing_data


def mutation_updateCounterPromotion(account_promotion_id:str):
    assert isinstance(account_promotion_id, str), "account_promotion_id must be a string"
    mutation = '''
      mutation updateCounterPromotion($accountPromotionId: ID!) {
      updateCounterPromotion(accountPromotionId: $accountPromotionId) {
        availableUsageTimes
        accountPromotionContinuesActive
        counterUses
      }
    }

''' 
    account_name = request.headers.get('X-Auth-User')
    bearer_token = request.headers.get('Authorization')
    headers = {
        'Authorization': bearer_token,
        'X-Auth-User': account_name
    }
    variables ={"accountPromotionId": account_promotion_id}

    response = requests.post(pricing_protected_service_url, json={'mutation': mutation,'variables': variables}, headers=headers)
    data = response.json()
    pricing_data = data.get('data', {}).get('updateCounterPromotion', {})
    return pricing_data