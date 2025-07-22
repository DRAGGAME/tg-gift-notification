from typing import Optional, Union

from database.db import Sqlbase


class AdminOperations(Sqlbase):
    async def check_login(self) -> bool:
        check_active = await self.execute_query("""SELECT active_admin FROM settings_table""")
        return check_active[0][0]

    async def update_state_admin(self, user_active: bool):
        await self.execute_query("""UPDATE settings_table SET active_admin = $1;""", (user_active,))

    async def update_url_user(self, url: str):
        await self.execute_query("""UPDATE settings_table SET user_politics=$1""", (url,))

    async def update_url_politics(self, url: str):
        await self.execute_query("""UPDATE settings_table SET kond_politics=$1""", (url,))

    async def update_price(self, price: int):
        await self.execute_query("""UPDATE settings_table SET Purchase_price=$1""", (price,))

    async def update_state(self, chat_id: str, action: bool):
        await self.execute_query("""UPDATE user_data SET purchased=$1 WHERE chat_id=$2""", (action, chat_id,))

    async def insert_faq(self, question: str, answer: str):
        await self.execute_query("""INSERT INTO faq_table (Question, Answer) VALUES($1, $2)""", (question, answer,))

    async def delete_faq(self, id_faq: int):
        await self.execute_query("""DELETE FROM faq_table WHERE id=$1""", (id_faq,))

    async def truncate_faq(self):
        await self.execute_query("""TRUNCATE faq_table""")

    async def select_faq(self):
        all_faq = await self.execute_query("""SELECT * FROM faq_table ORDER BY id ASC;""")
        text = ""
        ids_faq = []
        if all_faq:
            for faq in all_faq:
                ids_faq.append(faq[0])
                text += f"\n\n{faq[0]}) Вопрос: {faq[1]}\n{' ' * 4}Ответ: {faq[2]}"

            return text, ids_faq

        else:
            return None, None
