from deadflask.server.app import app
from deadflask.server.models.characters import CharacterType


def describe_characters_by_type(humans, zombies, corpses):
    inflect = app.inflect
    category_strings = []
    for category_list, noun in ((humans, 'human'), (zombies, 'zombie'), (corpses, 'corpse')):
        amount = len(category_list)
        if not amount:
            continue

        verb_is = inflect.plural_verb('is', amount)
        word_amount = inflect.number_to_words(amount)
        plural_noun = inflect.plural_noun(noun)
        category_strings.append(f"There {verb_is} {word_amount} {plural_noun}")

    return "\n".join(category_strings)


def split_by_category(characters):
    humans = []
    zombies = []
    corpses = []
    for character in characters:
        character_type = app.db_session.query(CharacterType).get(character.type)
        if character.health <= 0:
            corpses.append(character)
        elif character_type.name == "Zombie":  # TODO Maybe we'll have more than one?
            zombies.append(character)
        else:
            humans.append(character)

    return humans, zombies, corpses
