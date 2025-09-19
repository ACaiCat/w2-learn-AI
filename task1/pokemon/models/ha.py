from enums import Type
from models import Pokemon, Skill


class HaCat(Pokemon):
    def __init__(self, bot: bool):
        self.ha_progress: int = 0
        # noinspection PyTypeChecker
        super().__init__(name="哈基米",
                         health_point=114514,
                         damage=10,
                         defense=0,
                         type_=Type.DARK,
                         evasion_rate=30,
                         skills=
                         [
                             Skill(name="猫猫普攻",
                                   action=scratch),
                             Skill(name="哈气",
                                   action=ha),
                         ],
                         bot=bot)


def scratch(pokemon: Pokemon, enemy: Pokemon) -> None:
    enemy.attacked(pokemon, int(pokemon.damage * 1.4))


def ha(pokemon: HaCat, enemy: Pokemon) -> None:
    if pokemon.ha_progress == 3:
        enemy.attacked(pokemon, 1145141919810)
        pokemon.ha_progress = 0
    else:
        pokemon.ha_progress += 1
        print(f"[{pokemon.name}]正在为「哈气」蓄力 ({pokemon.ha_progress}/3)...")
