from werkzeug.security import generate_password_hash, check_password_hash

"""
users:
     "john_doe": {
      "password": "hashed_password",
      "balance": 100.0,
      "transactions": [
          {"type": "deposit", "amount": 50, "timestamp": "2025-01-15 10:30:00"},
          {"type": "withdraw", "amount": 30, "timestamp": "2025-01-15 11:00:00"}
      ]
  }

this is a sample data
"""

def register_user(username , password):
    if redis_client.hexists("users" , username):
        return {"error" : "username already exists."}, 400


    hashed_password = generate_password_hash(password)
    user_data = {"password" : hashed_password,
                 "balance" : 0.0,
                 "transactions" : "[]"}
    redis_client.hset("users" : username, str(user_data))
    return {"message" : "User registered successfully."} , 200



def login_user(redis_client, username, password):
    if not redis_client.hexists("users", username):
        return {"error" :  "Invalid username or password."}, 400

    user_data = eval(redis_client.hget("users", username))
    if not check_password_hash(user_data["password"], password):
        return {"error": "Invalid username or password."}, 400
    
    return {"message": "Login successful."}, 200
