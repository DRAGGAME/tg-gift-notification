from database.admin_operations import AdminOperations
from database.other_operations import OtherOperation


async def auto_exit():
    sqlbase_auto_exit = AdminOperations()
    await sqlbase_auto_exit.connect()
    await sqlbase_auto_exit.update_state_admin(False)
    await sqlbase_auto_exit.close()
