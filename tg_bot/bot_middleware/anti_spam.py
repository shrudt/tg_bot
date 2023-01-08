import redis

from datetime import timedelta
from tg_bot.db.db_controller import db_user_block_update, db_select_blocked


r = redis.Redis(host='redis')


async def spam_catcher(event):
    if r.get(f'{event.from_user.id}') is None:
        r.setex(f'{event.from_user.id}', time=timedelta(minutes=5), value=event.date.strftime("%H%M%S"))
        r.setex(f"{event.from_user.id}_mess_count", time=timedelta(minutes=5), value=0)
    if abs(int(event.date.strftime("%H%M%S")) - int(r.get(event.from_user.id))) <= 3:
        r.incr(f"{event.from_user.id}_mess_count")
        r.setex(f'{event.from_user.id}', time=timedelta(seconds=15), value=event.date.strftime("%H%M%S"))
        if int(r.get(f"{event.from_user.id}_mess_count")) == 5:
            r.setex(f'{event.from_user.id}_blocked', time=timedelta(seconds=20), value=1)
            db_user_block_update(event.from_user.id)


def check_blocked(user_id):
    if r.get(f'{user_id}_blocked') is None:
        if db_select_blocked(user_id) is None:
            r.set(f'{user_id}_blocked', value=0)
        else:
            r.set(f'{user_id}_blocked', value=db_select_blocked(user_id)[0])
    if int(r.get(f'{user_id}_blocked')) == 0:
        return True
    else:
        return False




