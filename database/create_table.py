from database.admin_operations import AdminOperations
from database.db import Sqlbase


class CreateTable(AdminOperations):

    async def create_profiles_table(self):
        await self.execute_query("""CREATE TABLE IF NOT EXISTS profiles (
                                    id SERIAL PRIMARY KEY,
                                    number_profile INTEGER UNIQUE NOT NULL,
                                    type_regime TEXT DEFAULT 'down',
                                    count_one_gift INTEGER DEFAULT 2,
                                    price_min INTEGER DEFAULT 0,
                                    price_max INTEGER DEFAULT 1000,
                                    auto_upgrade BOOLEAN DEFAULT FALSE,
                                    comment_for_gift TEXT DEFAULT '',
                                    channel_for_answer TEXT DEFAULT ''
                                    )""")
        if await self.execute_query("""SELECT * FROM profiles"""):
            pass
        else:
            await self.insert_profile(number_profile=1)

    async def create_transaction_donat(self):
        await self.execute_query("""CREATE TABLE IF NOT EXISTS all_transaction (
        id SERIAL PRIMARY KEY,
        type_transaction TEXT,
        date_pay TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow'),
        transaction_id TEXT UNIQUE NOT NULL,
        amount INTEGER NOT NULL
        );""")

    async def create_settings_table(self):
        await self.execute_query("""CREATE TABLE IF NOT EXISTS settings_table (
        id SERIAL PRIMARY KEY,
        bot_balance INTEGER DEFAULT 0,
        default_channel TEXT DEFAULT 'default',
        admin_chat_id TEXT DEFAULT '0',
        password_admin TEXT DEFAULT 'vFDJSldsfCEldsSA1317Opd', 
        activate_profile INTEGER DEFAULT 1,
        FOREIGN KEY (activate_profile) REFERENCES profiles (number_profile) ON DELETE RESTRICT
        );""")

        if await self.execute_query("""SELECT password_admin FROM settings_table LIMIT 1"""):
            pass
        else:
            await self.execute_query("""INSERT INTO settings_table (default_channel)
                                        VALUES (DEFAULT)""")

    async def delete_all(self):
        await self.execute_query("""DROP TABLE user_data""")
        await self.execute_query("""DROP TABLE accepted_users""")
        await self.execute_query("""DROP TABLE faq_table""")
        await self.execute_query("""DROP TABLE settings_table""")