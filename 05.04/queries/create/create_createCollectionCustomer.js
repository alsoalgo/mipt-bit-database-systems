db.createCollection("customers")

db.customers.insertOne({
    "CustomerID": 1,
    "Name": "John Smith",
    "Email": "john.smith@example.com",
    "Phone": "123-456-7890"
})