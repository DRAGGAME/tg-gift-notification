from database.db import Sqlbase


class CreateTable(Sqlbase):


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
        type_regime TEXT DEFAULT 'down',
        count_gifts INTEGER DEFAULT 0,
        count_one_gift INTEGER DEFAULT 0,
        price_min INTEGER DEFAULT 0,
        price_max INTEGER DEFAULT 40,
        bot_balance INTEGER DEFAULT 0,
        default_channel TEXT DEFAULT 'default',
        admin_chat_id TEXT DEFAULT '0',
        password_admin TEXT DEFAULT 'vFDJSldsfCEldsSA1317Opd', 
        active_admin BOOLEAN DEFAULT FALSE);""")

        if await self.execute_query("""SELECT password_admin FROM settings_table LIMIT 1"""):
            pass
        else:
            await self.execute_query("""INSERT INTO settings_table (type_regime, price_min, price_max,
                                                                    password_admin, active_admin) 
                                        VALUES (DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT)""")

    async def delete_all(self):
        await self.execute_query("""DROP TABLE user_data""")
        await self.execute_query("""DROP TABLE accepted_users""")
        await self.execute_query("""DROP TABLE faq_table""")
        await self.execute_query("""DROP TABLE settings_table""")