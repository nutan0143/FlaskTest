# FlaskTest

### *Tool , Technologies and Version*

Install Python3.8 or any version of Python

Flask==1.1.1
stripe==2.49.0

### *Step for setup Project*

1.Clone FlaskTest by using 
    
    git clone -b Test https://github.com/nutan0143/FlaskTest.git

2.Make environment in your project
    
    virtualenv environment_name.

3.Activate your environment
    
    a. source environment_name/bin/activate   #for mac and ubuntu
    
    b. environment_name\Scripts\activate      #for window

4.Install requirement
    
    pip install -r requiremnets.txt

3.Run flask from commandline using 
    
    flask run
 
### *Test Cases:*

1.{
    "card_number":"4242424242424242",
    "card_holder":"Nutan Gupta",
    "expiry_date":"11/23",
    "amount":19,
    "cvc":""
}

2.{
    "card_number":"4242424242424242",
    "card_holder":"Nutan Gupta",
    "expiry_date":"11/23",
    "amount":200,
    "cvc":"314"
}

3.{
    "card_number":"4242424242424242",
    "card_holder":"Nutan Gupta",
    "expiry_date":"11/23",
    "amount":501,
    "cvc":""
}
