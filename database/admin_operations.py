from typing import Optional, Union, Tuple

from database.db import Sqlbase
from logger import logger


class AdminOperations(Sqlbase):

    async def setup_query(self, admin_chat_id: str) -> None:
        await self.execute_query("""UPDATE settings_table
                                    SET admin_chat_id = $1""", (admin_chat_id,))

    async def select_password_and_user(self) -> tuple:
        password_admin = await self.execute_query("""SELECT password_admin, admin_chat_id
                                                     FROM settings_table""")
        return password_admin[0]

    async def update_admin_password(self, admin_chat_id: str) -> None:
        await self.execute_query("""UPDATE settings_table
                                    SET password_admin=$1,
                                        admin_chat_id=$2""",
                                 (None, admin_chat_id))

    async def insert_profile(self) -> Optional[int]:
        profiles = await self.execute_query("""SELECT COUNT(*)
                                               FROM profiles""")
        print(profiles)
        if profiles != 5:
            number_profile = profiles[0][0] + 1
            await self.execute_query("""INSERT INTO profiles(number_profile)
                                        VALUES ($1)""",
                                     (number_profile,))
            return number_profile

        else:
            return None

    async def select_profile_last(self) -> tuple:
        settings_profiles = await self.execute_query("""SELECT type_regime,
                                                               count_one_gift,
                                                               price_min,
                                                               price_max,
                                                               bot_balance,
                                                               channel_for_answer,
                                                               admin_chat_id,
                                                               activate_profile
                                                        FROM settings_table
                                                                 INNER JOIN profiles ON profiles.number_profile = settings_table.activate_profile""")
        return settings_profiles

    async def select_profiles(self) -> tuple:
        settings_profiles = await self.execute_query("""SELECT type_regime,
                                                               count_one_gift,
                                                               price_min,
                                                               price_max,
                                                               number_profile
                                                        FROM profiles""")
        return settings_profiles

    async def select_profile(self, number_profile: int) -> tuple:
        settings_profiles = await self.execute_query("""SELECT *
                                                        FROM profiles
                                                        WHERE number_profile = $1 """,
                                                     (number_profile,))
        print(number_profile)
        print(settings_profiles)

        return settings_profiles[0]

    async def update_gift_price(self, type_price: str, number_profile: int, price: int):
        if type_price == "begin_price":
            await self.execute_query(f"""UPDATE profiles
                                        SET price_min = $1
                                        WHERE number_profile = $2 """, (price, number_profile, ))
        elif type_price == "end_price":
            await self.execute_query(f"""UPDATE profiles
                                        SET price_max = $1
                                        WHERE number_profile = $2 """, (price, number_profile, ))
        else:
            logger.error("Invalid type_price")

    async def update_count_gift(self, count_one_gift: int, number_profile: int):
        await self.execute_query("""UPDATE profiles
                                    SET count_one_gift = $1
                                    WHERE number_profile = $2""", (count_one_gift, number_profile,))

    async def update_description(self, description: str, number_profile: int):
        await self.execute_query("""UPDATE profiles 
                                SET comment_for_gift = $1
                                WHERE number_profile = $2
                                """, (description, number_profile, ))

    async def update_channel_for_answer(self, channel_for_answer: str, number_profile: int):
        await self.execute_query("""UPDATE profiles 
                                    SET channel_for_answer = $1 
                                    WHERE number_profile = $2""", (channel_for_answer, number_profile, ))

    async def update_mode(self, number_profile: int):
        await self.execute_query(
            """
            UPDATE profiles
            SET type_regime = CASE
                                  WHEN type_regime = 'Up' THEN 'Down'
                                  WHEN type_regime = 'Down' THEN 'Up'
                END
            WHERE number_profile = $1
              AND type_regime IN ('Up', 'Down')
            """,
            (number_profile,)
        )

    async def delete_profile(self, number_profile: int):
        await self.execute_query("""DELETE FROM profiles WHERE number_profile = $1""", (number_profile,))
