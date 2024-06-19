# Backend Development

### How to clone all  Backend, including the submodule


[Watch Video](https://youtu.be/_aZB5xT-IEw)

### 2. How to run the project in the local host (Docker Development environment)

Requirements: Docker Compose.
[Watch Video](https://youtu.be/rpQj86oyWA0)

## Authentication Context

### 3. How to create the authentication database

[Watch Video](https://youtu.be/Q-ekAkPcn6E)

```bash
# curl UPDATE "Product" SET upc_barcode = NULL WHERE upc_barcode = '';

curl --location --request GET 'http://localhost/public/auth/login_auth_root' \
--form 'username="root@authentication"' \
--form 'password="ghp!123"'

# curl login_auth
curl --location 'http://localhost/public/auth/login' \
--form 'username="denisbueltan"' \
--form 'password="pass123"'
```

```bash
# curl create_database (required a root user (create token with : login_auth  ))
curl --location --request POST 'http://localhost/protected/auth/create_database' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJvb3RAYXV0aGVudGljYXRpb24iLCJhY2NvdW50X2lkIjpudWxsLCJleHRlcm5hbF9pZCI6bnVsbCwiaXNfcm9vdCI6dHJ1ZSwiaWF0IjoxNzA1NTEzMzk5LCJleHAiOjE3MTE1NjEzOTl9.HJeRl0VMNIvywkKNF2akhj9CoKt9NqtuvdjlVE9w75g'
```

### How to create an account

Requirement: Altair Client Graphql

- Run the authentication service (previous video)
- Create the database authentication database

[Watch Video](https://youtu.be/1DgAZhqUNQM)

Collection Altair: BACKEND/Servers testing/authentication_context__public_.agc

### Authentication and Ngnix

[Watch Video](https://youtu.be/wsdKhe-8keA)

### Create a Role and Level and assign those to an account

[Watch Video](https://youtu.be/_RuZUE8pooc)

Authentication context documentation :  https://docs.google.com/document/d/1iSmanzLyp6cmSghT-6rcUdmHQQ_sXVMnpIUGVEo9JhE/edit

Product context documentation :  https://docs.google.com/document/d/1Ub_Az7AKJFkk2I7-r8-5lViUWp5M-AhmuJOA1wcVnAI/edit



# Microservices-Products-GraphQl
