from models import PikaChu, HaCat

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    pc = PikaChu(True)
    bl = HaCat(True)

    pc.set_enemy(bl)
    bl.set_enemy(pc)

    while True:
        pc.start_turn()
        if pc.check_dead():
            break
        if bl.check_dead():
            break

        bl.start_turn()
        if pc.check_dead():
            break
        if bl.check_dead():
            break
