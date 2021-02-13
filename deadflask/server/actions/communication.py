from datetime import datetime

from deadflask.server.actions import listing
from deadflask.server.actions.context import ContextAction
from deadflask.server.api import characters as characters_api
from deadflask.server.models.buildings import Building
from deadflask.server.models.characters import Character


@listing.register
class SayAction(ContextAction):
    name = "Say"
    requires_freeform_text = True

    @classmethod
    def can_execute(cls, character) -> bool:
        base_result = super().can_execute(character)
        if not base_result:
            return base_result

        return character.health > 0

    @classmethod
    def execute(cls, character, target=None, item=None, text=None):
        # TODO Zombies should have their texts changed to moans
        if not text:
            return False

        building = Building.get_at(character.coord_x, character.coord_y, character.city)
        listeners = filter(
            lambda c: c is not character,
            Character.get_at_building(building, inside=character.is_inside)
        )
        timestamp = datetime.utcnow()
        actor_msg = f"You say '{text}'."
        listener_msg = f"{character.name} says '{text}'."
        characters_api.add_log(character, actor_msg, timestamp=timestamp)
        for listener in listeners:
            characters_api.add_log(listener, listener_msg, timestamp=timestamp)

        return True
