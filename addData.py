import subprocess
from  random import randint as randi, sample

import sys

def get_user_pass():
    login = 'admin:123123'
    try:
        li = sys.argv.index('-l') + 1
        login = sys.argv[li]
    except:
        print('login:pass not provided for -l option; using default')
    return login

def post_meals(n):
    print(f'posting {n} meals...')
    login = get_user_pass()
    for i in range(n):
        subprocess.run(["http","-a", login,
            "-f", "POST",
            "localhost:8000/meals/",
            f'name=Meal{randi(1,10000)}',
            f'description=Description{i}',
            f'prep_time={randi(5,40)}',
            f'price={randi(3,100)}'])

def post_menus(n,mc):
    print(f'posting {n} menus...')
    login = get_user_pass()
    for i in range(n):
        size = randi(1,mc)-1
        rndmeals = ','.join(map(str,sample(range(1,mc),size)))
        subprocess.run(["http","-a", login,
            "POST",
            "localhost:8000/menus/",
            f'name=Menu{randi(1,10000)}',
            f'description=Description{i}',
            f'meals:=[{rndmeals}]'])


if __name__ == '__main__':
    args = sys.argv
    mealcnt=20
    if "meals" in args:
        mi = args.index("meals")
        try:
            mealcnt = int(args[mi+1])
        except:
            pass
        post_meals(mealcnt)

    if "menus" in args:
        mi = args.index("menus")
        try:
            menucnt = int(args[mi+1])
        except:
            menucnt = 10
        try:
            menumealcnt = int(args[mi+2])
        except:
            menumealcnt = 10            
        post_menus(menucnt,menumealcnt)        

