from typing import Optional

from database.db import Sqlbase


class OtherOperation(Sqlbase):

    async def select_faq(self) -> Optional[str]:
        text = 'FAQ'
        all_faq = await self.execute_query("""SELECT * FROM faq_table ORDER BY id ASC;""")
        if all_faq:
            for count, faq in enumerate(all_faq):
                text += f"\n\n{count+1}) Вопрос: {faq[1]}\n{' ' * 4}Ответ: {faq[2]}"

            return text

        else:
            return None

    async def select_price(self) -> int:
        price = await self.execute_query("""SELECT Purchase_price FROM settings_table""")

        if isinstance(price[0][0], int):
            return price[0][0]
        else:
            raise "Ошибка, это не int"

    async def select_user(self, chat_id: str) -> bool:
        result = await self.execute_query("""SELECT chat_id FROM accepted_users WHERE chat_id=$1""", (chat_id,))

        return not bool(result)

    async def select_user_for_pay(self, chat_id: str) -> bool:
        result = await self.execute_query("""SELECT chat_id FROM user_data WHERE chat_id=$1""", (chat_id,))

        return not bool(result)

    async def accept_politics(self, chat_id: str):
        await self.execute_query(
            """INSERT INTO accepted_users (chat_id, date_accept_politics) VALUES ($1, DEFAULT)""",
            (chat_id,))

    async def insert_new_user(self, chat_id: str, transaction_id: str, amount: int):
        await self.execute_query(
            """INSERT INTO user_data (chat_id, transaction_id, amount, date_pay, purchased) 
            VALUES ($1, $2, $3, DEFAULT, DEFAULT)""",
            (chat_id, transaction_id, amount))

    async def insert_transaction_donat(self, chat_id: str, transaction_id: str, amount: int):
        await self.execute_query(
            """INSERT INTO all_transaction (chat_id, transaction_id, amount, date_pay) 
            VALUES ($1, $2, $3, DEFAULT)""",
            (chat_id, transaction_id, amount))

    async def select_url(self):
        url = await self.execute_query("""SELECT user_politics, kond_politics FROM settings_table""")
        return url[0][0], url[0][1]

