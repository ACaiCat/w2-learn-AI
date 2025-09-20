import time

from models import PikaChu, HaCat

if __name__ == '__main__':
    a = PikaChu(True)
    b = HaCat(True)

    a.set_enemy(b)
    b.set_enemy(a)

    while True:
        time.sleep(1)

        a.start_turn()
        if a.check_dead():
            break
        if b.check_dead():
            break

        time.sleep(1)
        b.start_turn()
        if a.check_dead():
            break
        if b.check_dead():
            break
