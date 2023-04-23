import json
import os
import sys
import random
import time


class Generator:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.data = None

    def __generate_timestamp(self, shift=0):
        current_timestamp = int(time.time())
        timestamp = random.randint(current_timestamp - shift * 60 * 60 * 24,
                                   current_timestamp)
        return timestamp

    def __generate_name(self, length):
        lowercase = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        uppercase = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        letters = lowercase + uppercase
        name = ''
        for i in range(length):
            name += random.choice(letters)
        return name

    def __generate_products(self):
        products_count = 400
        products = []
        for i in range(1, products_count + 1):
            products.append({
                'product_id': i,
                'name': self.__generate_name(length=10),
                'price': random.randint(1, 1000),
            })
        return products
    
    def __generate_top_rated_products(self, products):
        top_rated_products = []
        for i in range(1, 101):
            top_rated_products.append([random.choice(products)['product_id'], random.randint(100, 10_000)])
        return top_rated_products

    def __generate_users(self, products):
        users_count = random.randint(100_000, 105_000)
        users = []
        for i in range(users_count):
            users.append({
                'user_id': random.randint(1, 1000_000),
                'name': self.__generate_name(length=6),
                'created': self.__generate_timestamp(shift=4),
                'cart': ["{} {}".format(product['product_id'], random.randint(1, 5)) 
                         for product in random.sample(products, random.randint(4, 6))]
            })
        return users

    def __generate_orders(self, active_users, products):
        users_count = len(active_users)
        active_orders = {}
        active_order_user = {}
        for i in range(1, 3 * users_count + 1):
            order_id = i
            user_id = random.choice(active_users)
            product_id = random.choice(products)['product_id']
            amount = random.randint(5, 10)
            active_orders[str(order_id)] = "{} {}".format(product_id, amount)
            active_order_user[str(order_id)] = user_id
        return active_orders, active_order_user


    def generate(self):
        self.data = {}

        products = self.__generate_products()
        top_rated_products = self.__generate_top_rated_products(products)
        print("Products:", len(products))
        users = self.__generate_users(products)
        print("Users:", len(users))

        active_users = [user['user_id'] for user in users]
        active_orders, active_order_user = self.__generate_orders(active_users, products)
        
        print("Active orders:", len(active_orders))
        
        self.data['products'] = products
        self.data['top_rated_products'] = top_rated_products
        self.data['users'] = users
        self.data['active_orders'] = active_orders
        self.data['active_order_user'] = active_order_user
        self.data['active_users'] = active_users

        print("Size:", sys.getsizeof(json.dumps(self.data)) / (1024 * 1024), "MBs")

    def get_data(self):
        return self.data
    
    def write_in_file(self, path):
        directory, filename = os.path.split(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
       
        with open(os.path.join(directory, filename), 'w') as fp:
            fp.write(json.dumps(self.data))

        print("Generated file size:", os.path.getsize(path) / (1024  * 1024), "megabytes")


def main():
    random.seed(42)

    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')

    generator = Generator()
    generator.generate()
    generator.write_in_file(path)

if __name__ == '__main__':
    main()