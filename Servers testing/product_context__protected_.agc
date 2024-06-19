{"version":1,"type":"collection","title":"Product Context (Protected)","queries":[{"version":1,"type":"window","query":"mutation refactored97($productInput: ProductGraphInput!, $mediaInput: [MediaGraphInput]!) {\n  createProduct(productInput: $productInput, mediaInput: $mediaInput) {\n    product {\n      id\n      subCategoryId\n      name\n      title\n      brand\n      retailer\n      description\n      upcBarcode\n      unitMeasure\n      size\n      linkUrl\n      cost\n      mediaEdge {\n        edges {\n          node {\n            id\n            isMain\n            linkUrl  \n            mediaType\n          }\n        }\n      }\n    }\n  }\n}\n","apiUrl":"http://209.208.27.55/protected/product/gateway_graphql","variables":"{\n  \"productInput\": {\n    \"upcBarcode\": \"031142359022uy\",\n    \"subCategoryId\": \"U3ViQ2F0ZWdvcnk6MjU=\",\n    \"title\": \"title\",\n    \"size\": \"\",\n    \"brand\": \"brand\",\n    \"retailer\": \"\",\n    \"description\": \"description\",\n    \"cost\": 1\n  },\n  \"mediaInput\": [\n    {\n      \"linkUrl\": \"xryx.com\",\n      \"isMain\": true,\n      \"mediaType\": \"Image\"\n    },\n    {\n      \"linkUrl\": \"tttttt.com\",\n      \"isMain\": false,\n      \"mediaType\": \"Image\"\n    }\n  ]\n}","subscriptionUrl":"","subscriptionConnectionParams":"{}","headers":[{"key":"Authorization","value":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiYWNjb3VudF9pZCI6MywiaWF0IjoxNzA0NTgyMzM2LCJleHAiOjE3NDA4NzAzMzZ9.IP_1sjLaXAhiyt7E3FleWlagvNwrm75AdKT_bpnUdRc","enabled":true}],"windowName":"createProduct","preRequestScript":"","preRequestScriptEnabled":false,"postRequestScript":"","postRequestScriptEnabled":false,"id":"154ef5a3-9f6e-45f2-a97f-b36c6b4b4586","created_at":1705586621289,"updated_at":1705586621289}],"preRequest":{"script":"","enabled":false},"postRequest":{"script":"","enabled":false},"id":"18a881fc-b8cb-4f1a-8ac4-d4c19859094b","parentPath":"","created_at":1705586621289,"updated_at":1705586621289,"collections":[]}