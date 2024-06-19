{"version":1,"type":"collection","title":"Email Context (Protected)","queries":[{"version":1,"type":"window","query":"\nmutation SendCartOrderEmail($orderInput: CartOrderInput!) {\n  sendCartOrderEmail(\n    orderInput: $orderInput\n  ) {\n    response {\n      message\n    }\n  }\n}\n","apiUrl":"http://localhost:3052/protected/email/gateway_graphql","variables":"{\n  \"orderInput\": {\n      \"orderId\": \"1234\",\n      \"createdDate\": \"24/02/01\",\n      \"createdTime\": \"10:00\",\n      \"total\": 50.00,\n      \"siteName\": \"Target\",\n      \"customerDetails\": { \n        \"email\": \"tomidelizia@gmail.com\",\n        \"name\": \"Tomás Delizia\",\n        \"tenantId\": \"12345\",\n        \"phone\": \"123456789\"\n      },\n      \"deliveryDetails\": {\n        \"address\": \"62 Crisol\",\n        \"unitId\": 123,\n        \"amp\": \"120\",\n        \"deliverydate\": \"24/02/02\",\n        \"timerange\": \"18:00 - 21:00\"\n      },\n      \"orderDetails\": [\n        {\n          \"productName\": \"Frosted Flakes\",\n          \"brand\": \"Kellogs\",\n          \"description\": \"Not very healthy\",\n          \"image\":\n      \"https://http2.mlstatic.com/D_NQ_NP_943368-MLA69858199815_062023-O.webp\",\n          \"size\": \"Large\",\n          \"quantity\": 1,\n          \"price\": 2.00\n        }\n      ]\n  }\n}","subscriptionUrl":"","subscriptionConnectionParams":"{}","headers":[{"key":"","value":"","enabled":true}],"windowName":"sendCartOrderEmail","preRequestScript":"","preRequestScriptEnabled":false,"postRequestScript":"","postRequestScriptEnabled":false,"id":"d4b4abe6-4e2b-4e9d-8b82-71d6f59736e6","created_at":1706810482976,"updated_at":1706811308623}],"preRequest":{"script":"","enabled":false},"postRequest":{"script":"","enabled":false},"id":"b3b2e634-150d-42eb-9fa4-30b9c2337da2","parentPath":"","created_at":1706810439652,"updated_at":1706810439652,"collections":[]}