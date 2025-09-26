from typing import Optional, Union

from database.db import Sqlbase


class AdminOperations(Sqlbase):

    async def setup_query(self, admin_chat_id: str) -> None:
        await self.execute_query("""UPDATE settings_table SET admin_chat_id = $1""", (admin_chat_id, ))

    async def select_password_and_user(self) -> tuple:
        password_admin = await self.execute_query("""SELECT password_admin, admin_chat_id FROM settings_table""")
        return password_admin[0]

    async def update_admin_password(self, admin_chat_id: str) -> None:
        await self.execute_query("""UPDATE settings_table SET password_admin=$1, admin_chat_id=$2""",
                                 (None, admin_chat_id))

    async def insert_profile(self, number_profile: int):
        profiles = await self.execute_query("""SELECT COUNT(*) FROM profiles""")
        if len(profiles) != 5:
            await self.execute_query("""INSERT INTO profiles(number_profile) 
                                    VALUES ($1)""",
                                    (number_profile, ))

    async def select_all_profiles(self) -> tuple:
        settings_profiles = await self.execute_query("""SELECT 
                                type_regime, 
                                count_one_gift, 
                                price_min, 
                                price_max, 
                                bot_balance,
                                channel_for_answer,
                                admin_chat_id
                                activate_profile
                                FROM settings_table
                                INNER JOIN profiles ON profiles.number_profile = settings_table.activate_profile""")
        return settings_profiles