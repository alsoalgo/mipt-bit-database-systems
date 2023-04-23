class RedisDataInserter:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def __insert_users(self, users):
        for user in users:
            self.redis_client.hset('user:{}'.format(user['user_id']), "name", user['name'])
            self.redis_client.hset('user:{}'.format(user['user_id']), "created", user['created'])
            for item in user['cart']:
                self.redis_client.lpush('user:{}:cart'.format(user['user_id']), item)
        
    def __insert_products(self, products):
        for product in products:
            self.redis_client.hset('product:{}'.format(product['product_id']), "name", product['name'])
            self.redis_client.hset('product:{}'.format(product['product_id']), "price", product['price'])
    
    def __insert_top_rated_products(self, top_rated_products):
        for product_id, rating in top_rated_products:
            self.redis_client.zadd('top_rated_products', {product_id: rating})

    def __insert_active_users(self, users):
        for user in users:
            self.redis_client.sadd('active_users', user['user_id'])

    def __insert_active_orders(self, active_orders):
        for order_id, order in active_orders.items():
            self.redis_client.hset('active_orders', order_id, order)
    
    def __insert_active_order_user(self, active_order_user):
        for order_id, user_id in active_order_user.items():
            self.redis_client.hset('active_order_user', order_id, user_id)

    def insert(self, data):
        users = data['users']
        products = data['products']
        top_rated_products = data['top_rated_products']
        active_orders = data['active_orders']
        active_order_user = data['active_order_user']

        self.redis_client.flushall()

        self.__insert_users(users)
        self.__insert_active_users(users)
        self.__insert_products(products)
        self.__insert_top_rated_products(top_rated_products)
        self.__insert_active_orders(active_orders)
        self.__insert_active_order_user(active_order_user)
