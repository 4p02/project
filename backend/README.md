
# Team

- Jonathan Coletti
- Michael noyes 
- Mike 
- Meet 

# Backend

- Auth
  - Email and password 
  - Google auth 
  - JWT tokens
- Python package
  - Fastapi (requests and )
- Database
   - Postgresql
- 

## Naming convention
- methods
    - snake_case
- class 
    - UpperCase (MyClass)
- variables 
    - snake_case
- files
    - snake_case


## DATABASE

table users:

id auto increment;
full_name text;
email text;
password encrypted;


table shortlinks:
uid;
old_link text;
new_link text;

table summerization
uid;
summerization blob;
isPrivate boolean;

Everything but register gets the x-api-key
API key same as postgresql 

GET

- /summerization
    - Gets
      - Link
    - Returns
      - Summerization
- /shorten 
    - Gets
      - Link
    - Returns
      - New link
POST
- 
- /auth/login
   - username
   - password
- /auth/register
   - email
   - password
   - full_name
- 

DELETE 

UPDATE


