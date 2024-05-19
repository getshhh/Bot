import logging

from src.database.database import *


def task_to_list(task):
    if task:
        return task.deadline, task.task_text, task.coins_amount, task.owner, task.media
    return None


def user_exists(user_id):
    user = session.query(Users).filter(Users.id == user_id).first()
    return user is not None


def get_user_role(user_id):
    user = session.query(Users).filter(Users.id == user_id).first()
    if user:
        return user.role
    else:
        return None


def grant_admin_rights(user_id):
    user = session.query(Users).filter(Users.id == user_id).first()
    if user:
        if user.role != 'admin':
            user.role = 'admin'
            session.commit()
            return True
        else:
            return False
    else:
        return False


def save_user(user_id, name, balance=0, link=None):
    user = session.query(Users).filter(Users.id == user_id).first()
    if user:
        user.balance = balance
    else:
        new_user = Users(id=user_id, name=name, balance=balance, link=link)
        session.add(new_user)
    session.commit()


def get_is_admin(user_id: int) -> bool:
    try:
        user_role = get_user_role(user_id)
        if user_role is not None:
            return user_role.lower() == 'admin'
        return False
    except Exception as e:
        logging.error(f"Error checking for admin status of {user_id}: {e}")
        return False


def get_user_access_info(user_id):
    user_access = session.query(UserAccess).filter(UserAccess.id == user_id).first()
    return user_access.access if user_access else None


def get_easy_task_info():
    easy_task_info = session.query(EasyTasks).order_by(EasyTasks.id.desc()).first()
    return task_to_list(easy_task_info)


def save_easy_task(deadline, task_text, coins_amount, owner, media):
    new_easy_task = EasyTasks(deadline=deadline, task_text=task_text, coins_amount=coins_amount, owner=owner,
                              media=media)
    session.add(new_easy_task)
    session.commit()


def get_easy_task_info2():
    easy_task_info = session.query(EasyTasksTwo).order_by(EasyTasksTwo.id.desc()).first()
    return task_to_list(easy_task_info)


def save_easy_task2(deadline, task_text, coins_amount, owner, media):
    new_easy_task = EasyTasksTwo(deadline=deadline, task_text=task_text, coins_amount=coins_amount, owner=owner,
                                 media=media)
    session.add(new_easy_task)
    session.commit()


def get_easy_task_info3():
    easy_task_info = session.query(EasyTasksThree).order_by(EasyTasksThree.id.desc()).first()
    return task_to_list(easy_task_info)


def save_easy_task3(deadline, task_text, coins_amount, owner, media):
    new_easy_task = EasyTasksThree(deadline=deadline, task_text=task_text, coins_amount=coins_amount, owner=owner,
                                   media=media)
    session.add(new_easy_task)
    session.commit()


def get_wow_task_info():
    wow_task_info = session.query(WowTasks).order_by(WowTasks.id.desc()).first()
    return task_to_list(wow_task_info)


def save_wow_task(deadline, task_text, coins_amount, owner, media=None):
    new_easy_task = WowTasks(deadline=deadline, task_text=task_text, coins_amount=coins_amount, owner=owner,
                             media=media)
    session.add(new_easy_task)
    session.commit()


def get_user_balance(user_id):
    user = session.query(Users).filter(Users.id == user_id).first()
    return user.balance if user else None


def grant_user_access(user_id, access):
    # Используем сессию для выполнения запроса к базе данных
    new_user_access = UserAccess(id=user_id, access=access)
    session.add(new_user_access)
    session.commit()
