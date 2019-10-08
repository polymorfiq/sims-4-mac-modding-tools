import traceback
import services
import sims4.commands
from functools import wraps

def logger(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        client_id = services.client_manager().get_first_client_id()
        output = sims4.commands.CheatOutput(client_id)

        try:
            return fn(*args, **kwargs)
        except Exception as ex:
            output(traceback.format_exc())


    return wrapped
