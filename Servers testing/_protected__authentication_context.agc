{"version":1,"type":"collection","title":"(Protected) Authentication Context","queries":[{"version":1,"type":"window","query":"mutation refactored6($reason: String) {\n  softDeleteAccount(reason: $reason) {\n    message\n  }\n}\n","apiUrl":"http://104.245.38.245/protected/auth/gateway_graphql","variables":"{\n  \"reason\": \"\"\n}","subscriptionUrl":"","subscriptionConnectionParams":"{}","headers":[{"key":"Authorization","value":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRlbmlzYnVlbHRhbiIsImFjY291bnRfaWQiOjEwLCJleHRlcm5hbF9pZCI6bnVsbCwiaXNfcm9vdCI6ZmFsc2UsImlhdCI6MTcwNjIwNDU0NiwiZXhwIjoxNzEyMjUyNTQ2fQ.gN9lBOnM68dkpFMy0HbvhyzR0yslcg3FoxNgR7NjNk4","enabled":true}],"windowName":"live_softDeleteAccount","preRequestScript":"","preRequestScriptEnabled":false,"postRequestScript":"","postRequestScriptEnabled":false,"id":"8819b3ae-2b0c-4406-9c91-257ba552e116","created_at":1706204837842,"updated_at":1706204837842},{"version":1,"type":"window","query":"query {\n  accounts {\n    edges {\n      node {\n        id\n        userName\n        roleLevelList {\n          edges {\n            node {\n              role {\n                id\n                roleName\n                definition\n              }\n              level{\n                id\n                levelName\n                levelValue\n                definition\n\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n","apiUrl":"http://localhost/protected/auth/gateway_graphql","variables":"{}","subscriptionUrl":"","subscriptionConnectionParams":"{}","headers":[{"key":"Authorization","value":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJvb3RAYXV0aGVudGljYXRpb24iLCJhY2NvdW50X2lkIjpudWxsLCJleHRlcm5hbF9pZCI6bnVsbCwiaXNfcm9vdCI6dHJ1ZSwiaWF0IjoxNzA1NzIwODc0LCJleHAiOjE3MTE3Njg4NzR9.QGZ0gh1_FNjP5Q9rxPE-SrxZUKd_6Y5ft5a-zK-Fc-8","enabled":true}],"windowName":"getAccounts","preRequestScript":"","preRequestScriptEnabled":false,"postRequestScript":"","postRequestScriptEnabled":false,"id":"b33c72d7-1078-4565-b0db-f1258e0ea5d1","created_at":1706555357783,"updated_at":1706555357783},{"version":1,"type":"window","query":"query {\n  accounts {\n    edges {\n      node {\n        id\n        userName\n        roleLevelList {\n          edges {\n            node {\n              role {\n                id\n                roleName\n                definition\n              }\n              level{\n                id\n                levelName\n                levelValue\n                definition\n\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n","apiUrl":"http://104.245.38.245/protected/auth/gateway_graphql","variables":"{}","subscriptionUrl":"","subscriptionConnectionParams":"{}","headers":[{"key":"Authorization","value":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJvb3RAYXV0aGVudGljYXRpb24iLCJhY2NvdW50X2lkIjpudWxsLCJleHRlcm5hbF9pZCI6bnVsbCwiaXNfcm9vdCI6dHJ1ZSwiaWF0IjoxNzA1NzIwODc0LCJleHAiOjE3MTE3Njg4NzR9.QGZ0gh1_FNjP5Q9rxPE-SrxZUKd_6Y5ft5a-zK-Fc-8","enabled":true}],"windowName":"live getAccounts","preRequestScript":"","preRequestScriptEnabled":false,"postRequestScript":"","postRequestScriptEnabled":false,"id":"9e3325d8-c56a-488a-919e-0966342da627","created_at":1706555397700,"updated_at":1706555397700}],"preRequest":{"script":"","enabled":false},"postRequest":{"script":"","enabled":false},"id":"45babc3e-7445-4c69-9121-d68ab9a09a53","parentPath":"","created_at":1706204837799,"updated_at":1706204837799,"collections":[]}