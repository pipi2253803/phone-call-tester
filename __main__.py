"""
应用入口点
使用: python -m phone_tester
"""
from phone_tester.app import main

if __name__ == '__main__':
    app = main()
    app.main_loop()
