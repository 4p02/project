import requests
#test file
#used to see if the database was working
test_data= {
    "full_name":"Jose_h",
    "email": "test@123.com",
    "password" : "thisissecure"
}
test_login_data= {
    "full_name":"Jose_h3",
    "email": "test@123.com",
    "password" : "thisisNOTsecure"
}

req =requests.post("http://simplify.com:8080/register",json=test_data)
print(req.text)
req1 = requests.post("http://simplify.com:8080/login",json=test_login_data)
print(req1.text)
