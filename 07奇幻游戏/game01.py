from __future__ import print_function
import random
import sys

if sys.version_info < (3, 0):
    print("此代码需要 Python 3.x 并使用 3.5.x版测试 ")
    print("正在使用的Python版本是"
          ": %d.%d " % (sys.version_info[0], sys.version_info[1]))
    print("退出")
    sys.exit(1)


def weighted_random_selection(obj1, obj2):
    weighted_list = 3 * [id(obj1)] + 7 * [id(obj2)]
    selection = random.choice(weighted_list)

    if selection == id(obj1):
        return obj1
    return obj2


def print_bold(msg, end='\n'):
    print("\033[1m" + msg + "\033[0m", end=end)


class GameUnit:
    """
    创建各种游戏人物的基础类
    """

    def __init__(self, name=''):
        self.max_hp = 0
        self.health_meter = 0
        self.name = name
        self.enemy = None
        self.unit_type = None

    def info(self):
        pass

    def attack(self, enemy):
        """确定受伤单位和伤害值"""
        injured_unit = weighted_random_selection(self, enemy)
        injury = random.randint(10, 15)
        injured_unit.health_meter = max(injured_unit.health_meter - injury, 0)
        print("攻击!", end='')
        self.show_health(end='')
        enemy.show_health(end='')

    def heal(self, heal_by=2, full_healing=True):
        """治疗该单位的生命值"""
        if self.health_meter == self.max_hp:
            return
        if full_healing:
            self.health_meter = self.max_hp
        else:
            self.health_meter += heal_by
        print_bold("你受到治疗!", end=' ')
        self.show_health(bold=True)

    def reset_health_meter(self):
        self.health_meter = self.max_hp

    def show_health(self, bold=False, end='\n'):
        msg = "Heath: %s: %d" % (self.name, self.health_meter)

        if bold:
            print_bold(msg, end=end)
        else:
            print(msg, end=end)


class Knight(GameUnit):
    """
    代表游戏角色'骑士'的类,其他骑士实例由属性'self.unit_type'表示
    """

    def __init__(self, name='阿克蒙德-李维'):
        super().__init__(name=name)
        self.max_hp = 40
        self.health_meter = self.max_hp
        self.unit_type = 'friend'

    def info(self):
        print('我是一个骑士!')

    def acquire_hut(self, hut):
        print_bold("进入房子数量 %d..." % hut.number, end=' ')
        is_enemy = (isinstance(hut.occupant, GameUnit)
                    and hut.occupant.unit_type == 'enemy')
        continue_attack = 'y'
        if is_enemy:
            print_bold("敌人来了!")
            self.show_health(bold=True, end=' ')
            hut.occupant.show_health(bold=True, end=' ')
            while continue_attack:
                continue_attack = input("...继续战斗(y/n):")
                if continue_attack == 'n':
                    self.run_away()
                    break

                self.attack(hut.occupant)

                if hut.occupant.health_meter <= 0:
                    print("")
                    hut.acquire(self)
                    break
                if self.health_meter <= 0:
                    print("")
                    break
        else:
            if hut.get_occupant_type() == 'unoccupied':
                print_bold("房子里没人")
            else:
                print("同伴在房子里")
            hut.acquire(self)
            self.heal()

    def run_away(self):
        print_bold("离开")
        self.enemy = None


class OrcRider(GameUnit):
    def __init__(self, name=''):
        super().__init__(name=name)
        self.max_hp = 30
        self.health_meter = self.max_hp
        self.unit_type = 'enemy'
        self.hut_number = 0

    def info(self):
        print("我是兽人狼骑士,谁来受死?")


class Hut:
    def __init__(self, number, occupant):
        self.occupant = occupant
        self.number = number
        self.is_acquired = False

    def acquire(self, new_occupant):
        self.occupant = new_occupant
        self.is_acquired = True
        print_bold("Hut %d acquired" % self.number)

    def get_occupant_type(self):
        if self.is_acquired:
            occupant_type = 'ACQUIRED'
        elif self.occupant is None:
            occupant_type = "unoccupied"
        else:
            occupant_type = self.occupant.unit_type

        return occupant_type


class AttackOfTheOrcs:
    def __init__(self):
        self.huts = []
        self.player = None

    def get_occupants(self):
        return [x.get_occupant_type() for x in self.huts]

    def show_game_mission(self):
        print_bold("任务:")
        print(" 1 和敌人战斗")
        print(" 2 控制村里所有小屋")
        print("-" * 30, '\n')

    def _process_user_choice(self):
        verifying_choice = True
        idx = 0
        print("当前占据者:%s" % self.get_occupants())
        while verifying_choice:
            user_choice = input("选择一个房间号码(1-5):")
            idx = int(user_choice)
            if self.huts[idx - 1].is_acquired:
                print("你已经获得了这个小屋,重新选择" "<INFO:你不能在已经获的过的小屋进行治疗>")
            else:
                verifying_choice = False
        return idx

    def _occupy_huts(self):
        for i in range(5):
            choice_lst = ['enemy', 'friend', None]
            computer_choice = random.choice(choice_lst)
            if computer_choice == 'enemy':
                name = 'enemy-' + str(i + 1)
                self.huts.append(Hut(i + 1, OrcRider(name)))
            elif computer_choice == 'friend':
                name = 'knight-' + str(i + 1)
                self.huts.append(Hut(i + 1, Knight(name)))
            else:
                self.huts.append(Hut(i + 1, computer_choice))

    def play(self):
        self.player = Knight()
        self._occupy_huts()
        accquired_hut_counter = 0

        self.show_game_mission()
        self.player.show_health(bold=True)

        while accquired_hut_counter < 5:
            idx = self._process_user_choice()
            self.player.acquire_hut(self.huts[idx - 1])

            if self.player.health_meter <= 0:
                print_bold("你输了,下次再来尝试吧")
                break

            if self.huts[idx - 1].is_acquired:
                accquired_hut_counter += 1
        if accquired_hut_counter == 5:
            print_bold("恭喜你,你赢了")


if __name__ == '__main__':
    game = AttackOfTheOrcs()
    game.play()
