from __future__ import print_function
import random
import textwrap
import sys

if sys.version_info < (3, 0):
    print("此代码需要 Python 3.x 并使用 3.5.x版测试 ")
    print("正在使用的Python版本是"
          ": %d.%d " % (sys.version_info[0], sys.version_info[1]))
    print("退出")
    sys.exit(1)


def show_theme_message(width=76):
    """Print the game theme in the terminal window"""
    print_dotted_line()
    print_bold("兽人天灾 v0.0.5:")
    msg = ("人类将要与他们的敌人——兽人展开争夺萨林卡大陆霸权的命运之战"
           "一位勇敢的骑士：阿克蒙德-李维离开了他的家乡前往西部兽人聚集地——黑暗之林."
           "在途中,他发现了一个小小的孤立的定居点.当他走近村庄时，他看到了五个小屋,他决定进入..")

    print(textwrap.fill(msg, width=width))


def show_game_mission():
    """Print the game mission in the terminal window"""
    print_bold("任务:")
    print("\t选择李维可以休息的小屋...")
    print_bold("TIP:")
    print("保持警惕,周围有敌人!")
    print_dotted_line()


def reveal_occupants(idx, huts):
    """Print the occupants of the hut"""
    msg = ""
    print("展示小屋内部情况...")
    for i in range(len(huts)):
        occupant_info = "<%d:%s>" % (i + 1, huts[i])
        if i + 1 == idx:
            occupant_info = "\033[1m" + occupant_info + "\033[0m"
        msg += occupant_info + " "

    print("\t" + msg)
    print_dotted_line()


def occupy_huts():
    """Randomly populate the `huts` list with occupants"""
    huts = []
    occupants = ['enemy', 'friend', 'unoccupied']
    while len(huts) < 5:
        computer_choice = random.choice(occupants)
        huts.append(computer_choice)
    return huts


def process_user_choice():
    """Accepts the hut number from the user"""
    msg = "\033[1m" + "选择一个小屋进去,请输入 (1-5): " + "\033[0m"
    user_choice = input("\n" + msg)
    idx = int(user_choice)
    return idx


def show_health(health_meter, bold=False):
    """Show the remaining hit points of the player and the enemy"""
    msg = "Health: 阿克蒙德——李维: %d, 敌人: %d" \
          % (health_meter['player'], health_meter['enemy'])

    if bold:
        print_bold(msg)
    else:
        print(msg)


def reset_health_meter(health_meter):
    """Reset the values of health_meter dict to the original ones"""
    health_meter['player'] = 40
    health_meter['enemy'] = 30


def print_bold(msg, end='\n'):
    """Print a string in 'bold' font"""
    print("\033[1m" + msg + "\033[0m", end=end)


def print_dotted_line(width=72):
    """Print a dotted (rather 'dashed') line"""
    print('-' * width)


def attack(health_meter):
    """The main logic to determine injured unit and amount of injury"""
    hit_list = 4 * ['player'] + 6 * ['enemy']
    injured_unit = random.choice(hit_list)
    hit_points = health_meter[injured_unit]
    injury = random.randint(10, 15)
    health_meter[injured_unit] = max(hit_points - injury, 0)
    print("ATTACK! ", end='')
    show_health(health_meter)


def play_game(health_meter):
    """The main control function for playing the game"""
    huts = occupy_huts()
    idx = process_user_choice()
    reveal_occupants(idx, huts)

    if huts[idx - 1] != 'enemy':
        print_bold("恭喜! 你赢了!!!")
    else:
        print_bold('发现敌人! ', end='')
        show_health(health_meter, bold=True)
        continue_attack = True

        # Loop that actually runs the combat if user wants to attack
        while continue_attack:
            continue_attack = input(".......继续战斗? (y/n): ")
            if continue_attack == 'n':
                print_bold("敌我状态如下...")
                show_health(health_meter, bold=True)
                print_bold("GAME OVER!")
                break

            attack(health_meter)

            # Check if either one of the opponents is defeated
            if health_meter['enemy'] <= 0:
                print_bold("幸运的家伙,你赢的了胜利女神的光顾!")
                break

            if health_meter['player'] <= 0:
                print_bold("你输了,快逃,下次继续吧")
                break


def run_application():
    """Top level control function for running the application."""
    show_theme_message()
    keep_playing = 'y'
    health_meter = {}
    reset_health_meter(health_meter)
    show_game_mission()

    while keep_playing == 'y':
        reset_health_meter(health_meter)
        play_game(health_meter)
        keep_playing = input("\nPlay again? Yes(y)/No(n): ")


if __name__ == '__main__':
    run_application()