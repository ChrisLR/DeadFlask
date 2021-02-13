actions_by_name = {}


def register(action_class):
    actions_by_name[action_class.name] = action_class
    return action_class


def get_all():
    return actions_by_name.values()


def get_by_name(name):
    return actions_by_name.get(name)


def get_for_character(character):
    actions = [action for action in get_all() if action.can_execute(character)]

    return actions
