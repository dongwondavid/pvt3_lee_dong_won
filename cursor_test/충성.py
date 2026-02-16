import os
import time


def clear():
    # 화면 지우기 (Windows PowerShell 기준)
    os.system("cls")


frames = [
    r"   o   충성!",
    r"  \o   충성!",
    r"   o/  충성!",
    r"   o\  충성!",
]


def main():
    try:
        idx = 0
        while True:
            clear()
            print()
            print("    이병 ASCII 충성 애니메이션")
            print()
            print(frames[idx])
            print()
            print("  [Ctrl + C] 를 누르면 종료됩니다.")

            idx = (idx + 1) % len(frames)
            time.sleep(0.15)
    except KeyboardInterrupt:
        clear()
        print("충성! 수고하셨습니다.")


if __name__ == "__main__":
    main()

