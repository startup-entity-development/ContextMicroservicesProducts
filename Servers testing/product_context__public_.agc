{"version":1,"type":"collection","title":"Product Context (Public)","queries":[{"version":1,"type":"window","query":"{\n    productById(productId:\"UHJvZHVjdDoxMDU2\"){\n        id\n        name\n        mediaEdge{\n          edges{\n            node{\n              id\n              linkUrl\n            }\n          }\n        }\n    }\n}\n","apiUrl":"http://209.208.27.55/public/product/gateway_graphql","variables":"{}","subscriptionUrl":"","subscriptionConnectionParams":"{}","headers":[{"key":"","value":"","enabled":true}],"windowName":"remote-productByID","preRequestScript":"","preRequestScriptEnabled":false,"postRequestScript":"","postRequestScriptEnabled":false,"id":"eff4878f-ba96-4035-ae6b-af6baa470a45","created_at":1705586616320,"updated_at":1706037472553},{"version":1,"type":"window","query":"query refactored769($upcBarcode: String!) {\n  productByUpc(upcBarcode: $upcBarcode) {\n    id\n    subCategoryId\n    name\n    title\n    name\n    brand\n    description\n    upcBarcode\n    unitMeasure\n    size\n    linkUrl\n    cost\n    mediaEdge {\n      edges {\n        node {\n          linkUrl\n          isMain\n          mediaType\n        }\n      }\n    }\n  }\n}\n","apiUrl":"http://209.208.27.55/public/product/gateway_graphql","variables":"{\n  \"upcBarcode\": \"9781434103499\"\n}","subscriptionUrl":"","subscriptionConnectionParams":"{}","headers":[{"key":"","value":"","enabled":true}],"windowName":"remote_testing-productByUpcNotInDataBase","preRequestScript":"","preRequestScriptEnabled":false,"postRequestScript":"","postRequestScriptEnabled":false,"id":"663bd1b3-bbdf-44b9-a810-e389d6795b1a","created_at":1705586616320,"updated_at":1705586616320},{"version":1,"type":"window","query":"query {\n  finderProduct(toFind: \"Dressings\", limitResult: 30) {\n    edges {\n      node {\n        id\n        title\n        size\n        brand\n          SubCategory{name}\n      }\n    }\n  }\n}\n","apiUrl":"http://localhost/public/product/gateway_graphql","variables":"{}","subscriptionUrl":"","subscriptionConnectionParams":"{}","headers":[{"key":"","value":"","enabled":true}],"windowName":"finderProduct","preRequestScript":"","preRequestScriptEnabled":false,"postRequestScript":"","postRequestScriptEnabled":false,"id":"c1e5da60-09b4-4f37-8f03-8d1a1dc465bd","created_at":1705586616320,"updated_at":1705586616320}],"preRequest":{"script":"","enabled":false},"postRequest":{"script":"","enabled":false},"id":"2019e45e-8fa8-49ec-a5f3-f41f50c2ebf0","parentPath":"","created_at":1705586616320,"updated_at":1705586616320,"collections":[]}