from database.db import Sqlbase


class CreateTable(Sqlbase):

    async def create_user_table(self):
        await self.execute_query("""CREATE TABLE IF NOT EXISTS user_data (
        id SERIAL PRIMARY KEY,
        chat_id TEXT UNIQUE NOT NULL,
        purchased BOOLEAN DEFAULT TRUE,
        date_pay TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow'),
        transaction_id TEXT UNIQUE NOT NULL,
        amount INTEGER NOT NULL,
        FOREIGN KEY (chat_id) REFERENCES accepted_users (chat_id) ON DELETE RESTRICT
        );""")

    async def create_accepted_users_table(self):
        await self.execute_query("""CREATE TABLE IF NOT EXISTS accepted_users (
        id SERIAL PRIMARY KEY,
        chat_id TEXT UNIQUE NOT NULL,
        date_accept_politics TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow'));""")

    async def create_faq_table(self):
        await self.execute_query("""CREATE TABLE IF NOT EXISTS faq_table (
        id SERIAL PRIMARY KEY,
        Question TEXT NOT NULL,
        Answer TEXT NOT NULL);""")

    async def create_settings_table(self):
        await self.execute_query("""CREATE TABLE IF NOT EXISTS settings_table (
        id SERIAL PRIMARY KEY,
        Purchase_price BIGINT DEFAULT 150,
        admin_id TEXT,
        password_admin TEXT DEFAULT vFDJSldsfCEldsSA123_#i, 
        user_politics TEXT,
        kond_politics TEXT);""")

        if await self.execute_query("""SELECT Purchase_price FROM settings_table LIMIT 1"""):
            pass
        else:
            await self.execute_query("""INSERT INTO settings_table (Purchase_price) VALUES (DEFAULT)""")

    async def delete_all(self):
        await self.execute_query("""DROP TABLE user_data""")
        await self.execute_query("""DROP TABLE accepted_users""")
        await self.execute_query("""DROP TABLE faq_table""")
        await self.execute_query("""DROP TABLE settings_table""")