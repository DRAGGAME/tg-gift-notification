
from database.db import Sqlbase


class AdminOperations(Sqlbase):

    async def setup_query(self, admin_chat_id: str) -> None:
        await self.execute_query("""UPDATE settings_table
                                    SET admin_chat_id = $1""", (admin_chat_id,))

    async def select_password_try(self, password: str) -> tuple:
        """
        Проверка хэша пароля
        :param password:
        :return:
        """
        password = await self.execute_query("""
                                            SELECT password_admin = crypt($1, password_admin)
                                            FROM settings_table;
                                            """, (password,))
        return password

    async def select_admin_chat_id(self) -> tuple:
        """
        Извлечение админа
        :return:
        """
        chat_id_tuple = await self.execute_query("""SELECT admin_chat_id
                                                    FROM settings_table""")
        return chat_id_tuple

    async def update_admin_password(self, admin_chat_id: str) -> None:
        await self.execute_query("""UPDATE settings_table
                                    SET password_admin=$1,
                                        admin_chat_id=$2""",
                                 (None, admin_chat_id))

    async def insert_profile(self, channel_for_answer: str):

        id_profile = await self.execute_query("""INSERT INTO profiles (channel_for_answer)
                                                 VALUES ($1)
                                                 RETURNING id;""",
                                              (channel_for_answer,))

        count_profile = await self.execute_query("""SELECT COUNT(*) FROM profiles""")
        return id_profile[0][0], count_profile[0][0]


    async def select_profile_last(self) -> tuple:
        settings_profiles = await self.execute_query("""SELECT type_regime,
                                                               count_one_gift,
                                                               price_min,
                                                               price_max,
                                                               comment_for_gift,
                                                               channel_for_answer,
                                                               admin_chat_id
                                                        FROM settings_table
                                                                 INNER JOIN profiles ON profiles.id = settings_table.activate_profile""")
        return settings_profiles

    async def select_profiles(self) -> tuple:
        settings_profiles = await self.execute_query("""WITH info_profiles AS (
                                                        SELECT
                                                            p.id,
                                                            p.type_regime,
                                                            p.count_one_gift,
                                                            p.price_min,
                                                            p.price_max
                                                        FROM profiles AS p
                                                        ORDER BY id ASC
                                                        )
                                                        SELECT
                                                            inf_prof.id,
                                                            inf_prof.type_regime,
                                                            inf_prof.count_one_gift,
                                                            inf_prof.price_min,
                                                            inf_prof.price_max,
                                                            s.activate_profile      
                                                        FROM info_profiles AS inf_prof
                                                        LEFT JOIN settings_table AS s
                                                            ON s.activate_profile = inf_prof.id;
                                                        """)
        print(settings_profiles)
        return settings_profiles

    async def select_profile(self, id_profile: int) -> tuple:
        settings_profiles = await self.execute_query("""
            WITH foreign_key_check AS (
                SELECT 
                    tc.constraint_name, 
                    kcu.table_name AS foreign_table_name,
                    kcu.column_name AS foreign_column_name,
                    ccu.table_name AS referenced_table,
                    ccu.column_name AS referenced_column
                FROM 
                    information_schema.table_constraints AS tc 
                JOIN 
                    information_schema.key_column_usage AS kcu 
                    ON tc.constraint_name = kcu.constraint_name
                JOIN 
                    information_schema.constraint_column_usage AS ccu 
                    ON ccu.constraint_name = tc.constraint_name
                WHERE 
                    tc.constraint_type = 'FOREIGN KEY'
                    AND ccu.table_name = 'profiles'
                    AND ccu.column_name = 'id'
                    AND kcu.table_name = 'settings'
                    AND kcu.column_name = 'activate_profile'
            )
            SELECT 
                p.id,
                p.type_regime,
                p.count_one_gift,
                p.price_min,
                p.price_max,
                p.auto_upgrade,
                p.comment_for_gift,
                p.channel_for_answer,
                s.id AS settings_id,
                s.activate_profile,
                fkc.constraint_name AS foreign_key_constraint,
                fkc.foreign_table_name,
                fkc.foreign_column_name
            FROM 
                profiles p
            LEFT JOIN 
                settings_table s 
                ON s.activate_profile = p.id
            LEFT JOIN 
                foreign_key_check fkc 
                ON true
            WHERE 
                p.id = $1;
        """, (id_profile,))

        print(settings_profiles[0])
        return settings_profiles[0]

    async def update_gift_price(self, type_price: str, number_profile: int, price: int, last_price: tuple=[], price_dict: dict={}):
        if type_price == "begin_price":
            await self.execute_query(f"""UPDATE profiles 
                                        SET price_min = $1
                                        WHERE id = $2;
                                        """,
                                     (price, number_profile,))

        elif type_price == "end_price":
            await self.execute_query(f"""UPDATE profiles
                                        SET price_max = $1
                                        WHERE id = $2 """, (price, number_profile,))


        return price_dict

    async def update_count_gift(self, count_one_gift: int, number_profile: int):
        await self.execute_query("""UPDATE profiles
                                    SET count_one_gift = $1
                                    WHERE id = $2""", (count_one_gift, number_profile,))

    async def update_description(self, description: str, number_profile: int):
        await self.execute_query("""UPDATE profiles
                                    SET comment_for_gift = $1
                                    WHERE id = $2
                                 """, (description, number_profile,))

    async def update_channel_for_answer(self, channel_for_answer: str, number_profile: int):
        await self.execute_query("""UPDATE profiles
                                    SET channel_for_answer = $1
                                    WHERE id = $2""", (channel_for_answer, number_profile,))

    async def update_mode(self, number_profile: int):
        await self.execute_query(
            """
            UPDATE profiles
            SET type_regime = CASE
                                  WHEN type_regime = 'Up' THEN 'Down'
                                  WHEN type_regime = 'Down' THEN 'Up'
                END
            WHERE id = $1
              AND type_regime IN ('Up', 'Down')
            """,
            (number_profile,)
        )

    async def insert_new_transaction(self, type_transaction: str, transaction_id, amount: int):
        """
        При новой транзакции, обязателен chat_id из user_data
        :param type_transaction:
        :param transaction_id:
        :param amount:
        :return:
        """
        await self.execute_query("""INSERT INTO all_transaction (type_transaction, transaction_id, amount)
                                    VALUES ($1, $2, $3);""", (type_transaction, transaction_id, amount))

    async def delete_profile(self, number_profile: int):
        await self.execute_query("""DELETE
                                    FROM profiles
                                    WHERE id = $1""", (number_profile,))

    async def activate_profile(self, new_number_profile: int):
        await self.execute_query("""UPDATE settings_table
                                    SET activate_profile = $1""", (new_number_profile,))

    async def select_admin_chat(self) -> str:
        """
        Извлечение админского айди
        :return:
        """
        admin_chat = await self.execute_query("""SELECT admin_chat_id
                                                 FROM settings_table""")

        return admin_chat[0][0]

    async def select_password_and_user(self) -> tuple:
        """
        Данные, что существует пароль
        :return:
        """
        password_admin = await self.execute_query("""SELECT password_admin, admin_chat_id
                                                     FROM settings_table""")
        return password_admin[0]
