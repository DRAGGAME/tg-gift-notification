from config import PASSWORD_ADMIN
from database.admin_operations import AdminOperations
from database.db import Sqlbase


class CreateTable(AdminOperations):

    async def init_pgcrypto(self):
        """
        Инициализация pgcrypto
        :return:
        """
        await self.execute_query("""CREATE EXTENSION IF NOT EXISTS pgcrypto;""")

    async def create_profiles_table(self):
        await self.execute_query("""CREATE TABLE IF NOT EXISTS profiles (
                                    id SERIAL PRIMARY KEY,
                                    type_regime TEXT DEFAULT 'Down',
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
            id_profile = await self.execute_query("""INSERT INTO profiles (channel_for_answer)
                                                     VALUES ($1)
                                                     RETURNING id;""",
                                                  ('',))
            return id_profile[0][0]

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
        admin_chat_id TEXT DEFAULT '0',
        password_admin TEXT,
        activate_profile INTEGER DEFAULT 1,
        FOREIGN KEY (activate_profile) REFERENCES profiles (id) ON DELETE RESTRICT
        );""")

        if await self.execute_query("""SELECT password_admin FROM settings_table LIMIT 1"""):
            pass
        else:
            await self.execute_query("""INSERT INTO settings_table (password_admin)
                                        VALUES (crypt($1, gen_salt('bf')));""", (PASSWORD_ADMIN,))

    async def delete_all_table(self):
        await self.execute_query("""DROP TABLE IF EXISTS all_transaction;""")
        await self.execute_query("""DROP TABLE IF EXISTS settings_table;""")
        await self.execute_query("""DROP TABLE IF EXISTS profiles;""")
