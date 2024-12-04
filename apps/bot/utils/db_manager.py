import asyncpg
from apps.bot.config import config


class DBManager:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Connect to the database"""
        self.pool = await asyncpg.create_pool(dsn=config.DB_DNS)

    async def disconnect(self):
        """Disconnect from the database"""
        if self.pool is not None:
            await self.pool.close()

    async def fetch(self, query: str, *args):
        """Fetch a list of objects from the database"""
        async with self.pool.acquire() as connection:
            results = await connection.fetch(query, *args)
            return [dict(result) for result in results]

    async def fetch_one(self, query: str, *args):
        """Fetch a single object from the database"""
        async with self.pool.acquire() as connection:
            result = await connection.fetchrow(query, *args)
            return dict(result) if result else None

    async def execute(self, query, *args):
        """Execute a SQL command"""
        async with self.pool.acquire() as connection:
            await connection.execute(query, *args)

    async def create_tables(self):
        """Create database tables"""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
                telegram_id BIGINT PRIMARY KEY,
                language VARCHAR(16),
                phone VARCHAR(32),
                name VARCHAR(255),
                username VARCHAR(255),
                city VARCHAR(255) DEFAULT 'Toshkent'
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS branches (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                address VARCHAR(255),
                city VARCHAR(255) DEFAULT 'Toshkent',
                open_time TIME DEFAULT '10:00',
                close_time TIME DEFAULT '04:45',
                latitude FLOAT,
                longitude FLOAT,
                max_delivery_distance FLOAT DEFAULT 10.0
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                image VARCHAR(255)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                category_id BIGINT REFERENCES categories(id),
                name VARCHAR(255),
                description VARCHAR(255),
                price FLOAT,
                size VARCHAR(32),
                image VARCHAR(255)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
                order_type VARCHAR(32),
                branch_id BIGINT REFERENCES branches(id) ON DELETE CASCADE,
                d_longitude FLOAT NULL,
                d_latitude FLOAT NULL,
                status VARCHAR(32) DEFAULT 'created',
                total_price FLOAT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS order_items (
                id SERIAL PRIMARY KEY,
                order_id BIGINT REFERENCES orders(id) ON DELETE CASCADE,
                product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
                quantity INT NOT NULL CHECK (quantity > 0),
                UNIQUE (order_id, product_id)
            );
            """
        ]

        for query in queries:
            await self.execute(query)

        # Create functions and triggers
        # await self.create_triggers()

    # async def create_triggers(self):
    #     """Create necessary triggers and functions"""
    #     queries = [
    #         """
    #         CREATE OR REPLACE FUNCTION update_updated_at()
    #         RETURNS TRIGGER AS $$
    #         BEGIN
    #             NEW.updated_at = CURRENT_TIMESTAMP;
    #             RETURN NEW;
    #         END;
    #         $$ LANGUAGE plpgsql;
    #         """,
    #         """
    #         DO $$
    #         BEGIN
    #             IF NOT EXISTS (
    #                 SELECT 1 FROM pg_trigger WHERE tgname = 'set_updated_at_orders'
    #             ) THEN
    #                 CREATE TRIGGER set_updated_at_orders
    #                 BEFORE UPDATE ON orders
    #                 FOR EACH ROW
    #                 EXECUTE FUNCTION update_updated_at();
    #             END IF;
    #         END;
    #         $$;
    #         """,
    #         """
    #         DO $$
    #         BEGIN
    #             IF NOT EXISTS (
    #                 SELECT 1 FROM pg_trigger WHERE tgname = 'set_updated_at_order_items'
    #             ) THEN
    #                 CREATE TRIGGER set_updated_at_order_items
    #                 BEFORE UPDATE ON order_items
    #                 FOR EACH ROW
    #                 EXECUTE FUNCTION update_updated_at();
    #             END IF;
    #         END;
    #         $$;
    #         """
    #     ]
    #
    #     for query in queries:
    #         await self.execute(query)

    async def get_user(self, telegram_id):
        """Fetch a user by Telegram ID"""
        query = "SELECT * FROM users WHERE telegram_id = $1"
        return await self.fetch_one(query, telegram_id)

    async def get_branches(self):
        query = "SELECT * FROM branches"
        return await self.fetch(query)

    async def create_user(self, *args):
        query = "INSERT INTO users (telegram_id, language, phone, name, username) VALUES ($1, $2, $3, $4, $5)"
        return await self.execute(query, *args)

    async def update_user(self, telegram_id: int, **kwargs):
        fields = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        query = f"UPDATE users SET {fields} WHERE telegram_id = ${len(kwargs) + 1}"
        values = list(kwargs.values()) + [telegram_id]
        return await self.execute(query, *values)

    async def create_branch(self, *args):
        query = "INSERT INTO branches (name, address, open_time, close_time, latitude, longitude, max_delivery_distance) VALUES ($1, $2, $3, $4, $5, $6, $7)"
        return await self.execute(query, *args)

    async def create_category(self, *args):
        query = "INSERT INTO categories (name, image) VALUES ($1, $2)"
        return await self.execute(query, *args)

    async def create_category_product(self, *args):
        query = "INSERT INTO products (category_id, name, description, price, size, image) VALUES ($1, $2, $3, $4, $5, $6)"
        return await self.execute(query, *args)

    async def get_categories(self):
        query = "SELECT * FROM categories"
        return await self.fetch(query)

    async def get_category(self, category_id):
        query = "SELECT * FROM categories WHERE id = $1"
        return await self.fetch_one(query, category_id)

    async def get_products(self, category_id):
        query = "SELECT * FROM products WHERE category_id = $1"
        return await self.fetch(query, category_id)

    async def get_product(self, product_id):
        query = "SELECT * FROM products WHERE id = $1"
        return await self.fetch_one(query, product_id)

    async def create_order(self, *args):
        query = "INSERT INTO orders (user_id, order_type, branch_id, d_longitude, d_latitude) VALUES ($1, $2, $3, $4, $5) RETURNING id"
        return await self.fetch_one(query, *args)

    async def get_current_order(self, user_id):
        query = "SELECT * FROM orders WHERE user_id = $1 AND status = 'created'"
        return await self.fetch_one(query, user_id)

    async def get_my_orders(self, user_id):
        query = "SELECT * FROM orders WHERE user_id = $1"
        return await self.fetch(query, user_id)

    # async def create_or_update_order_item(self, order_id, product_id, quantity):
    #     query = "SELECT * FROM order_items WHERE order_id = $1 AND product_id = $2"
    #     order_item = await self.fetch_one(query, order_id, product_id)
    #     if not order_item:
    #         query = "INSERT INTO order_items (order_id, product_id, quantity) VALUES ($1, $2, $3)"
    #         await self.execute(query, order_id, product_id, quantity)
    #     else:
    #         query = "UPDATE order_items SET quantity = $3 WHERE order_id = $1 AND product_id = $2"
    #         await self.execute(query, order_id, product_id, quantity)

    async def create_or_update_order_item(self, order_id, product_id, quantity):
        query = """
            INSERT INTO order_items (order_id, product_id, quantity)
            VALUES ($1, $2, $3)
            ON CONFLICT (order_id, product_id)
            DO UPDATE SET quantity = $3;
        """
        await self.execute(query, order_id, product_id, quantity)


db = DBManager()
