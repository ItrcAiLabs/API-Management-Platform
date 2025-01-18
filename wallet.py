from datetime import datetime

def record_transaction(redis_client, username, transaction_type, amount):
    user_data = eval(redis_client.hget("users", username))
    transactions = eval(user_data["transactions"])
    transactions.append({
        "type" : transaction_type,
        "amount" : amount,
        timestamp : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    transactions = transactions[-10:]
    user_data["transactions"] = str(transactions)
    redis_client.hset("users". username, str(user_data))

