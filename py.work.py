import time
import random
import time
import pickle


# 界面类
class View(object):
    def printadminview(self):
        print("*************************************************")
        print("*                   欢迎来到管理员界面             *")
        print("*      请选择                                    *")
        print("*      设置atm总金额（1）       查询金额存取记录（2）*")
        print("*      返回主页（3）                              *")
        print("*************************************************")

    def paView(self):
        print("*************************************************")
        print("*                 欢迎使用本ATM                   *")
        print("*      请选择你需要的服务                          *")
        print("*           日常服务（1）     管理员操作（2）       *")
        print("*                 退出系统（q）                   *")
        print("*************************************************")

    def login(self):
        ina = input("请输入管理员账号：")
        if (  ina!= "root"):
            print("账号输入错误，退出系统...")
            return False
        inaP = input("请输入管理员密码:")
        if (inaP!= "root"):
            print("密码输入错误，退出系统...")
            return False
        print("登录成功，请稍后...")
        time.sleep(0.5)
        return True

    def printSysFunctionView(self):
        print("*************************************************")
        print("*    开户（1）               查询（2）             *")
        print("*    取款（3）               存款（4）             *")
        print("*    转账（5）               改密（6）             *")
        print("*    锁定（7）               解锁（8）             *")
        print("*    补卡（9）               销户（0）             *")
        print("*               返回主页（q）                      *")
        print("*************************************************")
        return 0


class User(object):
    def __init__(self, name, idCard, phone, card):
        self.name = name
        self.idCard = idCard
        self.phone = phone
        self.card = card


class Admin(object):
    jl = 0

    def setallmoney(self, allmoney):
        self.allmoney = allmoney

    def cqjl(self, jilu):
        self.moneyjl = {jl + 1: jilu}

    def __int__(self):
        self.adminpassword = "root"
        self.adminid = "root"
    def getid(self):
        return self.adminid
    def getpwd(self):
        return self.adminpassword
    def getallmoney(self):
        return self.allmoney

    def getjl(self):
        return self.moneyjl


class Card(object):
    def __init__(self, cardId, password, money):
        self.cardId = cardId
        self.password = password
        self.money = money
        self.cardLock = False


class ATM(object):
    # ATM存储了所有的用户信息
    def __init__(self, allUser):
        # allUser存用户信息
        self.allUser = allUser
    def getalluser(self):
        return self.allUser

    # 开户
    def createUser(self):
        name = input("请输入你的姓名：")
        idCard = input("请输入你的身份证号码：")
        phone = input("请输入你的电话号码：")

        preMoney = int(input("请输入你的预存款金额："))
        if (preMoney < 0):
            print("你的输入有误，开户失败...")
            return -1
        onePassword = input("请输入你的密码：")

        # 验证密码,密码错误
        if not self.checkPassword(onePassword):
            print("你的输入有误，开户失败...")
            return -1
        strId = self.randomCardId()
        card = Card(strId, onePassword, preMoney)
        user = User(name, idCard, phone, card)
        self.allUser[strId] = user
        print("开卡成功...请牢记卡号(%s)" % (strId))
        time.sleep(1)

    # 查询，包含个人信息以及卡号信息
    def searchUserInfo(self):
        cardId = input("请输入你要查询的卡号：")
        # 验证是否存在卡号
        user = self.allUser.get(cardId)
        if not user:
            print("卡号不存在，查询失败...")
            return -1
        # 判断卡是否被锁定
        if user.card.cardLock:
            print("该卡被锁定！请解锁后在进行其他操作...")
            return -1

        # 有该卡号信息，保护隐私，验证密码之后才能显示个人信息
        if not self.checkPassword(user.card.password):
            user.card.cardLock = True
            print("密码输入错误，该卡被锁定,请解锁后在进行操作...")
            return -1

        # 密码输入正确之后展示个人信息
        print("-----个人信息-----")
        print("姓名：%s" % (user.name))
        print("身份证号：%s" % (user.idCard))
        print("手机号：%s" % (user.phone))
        print("卡号：%s " % (user.card.cardId))
        print("余额：%f" % (user.card.money))
        time.sleep(1)

    # 取款
    def getMoney(self):
        cardNum = input("请输入您的卡号：")
        #  验证是否存在该卡号
        user = self.allUser.get(cardNum)
        if not user:  # 如果有这个用户就不执行下面的语句，没有这个用户就执行
            print("该卡号不存在，取款失败...")
            return -1
        # 判断卡是否被锁定
        if user.card.cardLock:
            print("该卡被锁定，请解锁后在进行其他操作...")
            return -1
        #  验证密码
        if not self.checkPassword(user.card.password):
            print("密码输入错误...该卡已被锁定,请解锁后在进行其他操作...")
            user.card.cardLock = True
            return -1

        # 取款验证
        money = int(input("请输入取款金额："))
        if money > user.card.money:
            print("余额不足,取款失败...")
            return -1
        if money < 0:
            print("余额输入错误,取款失败...")
            return -1
        # 取款
        user.card.money -= money
        print("取款成功,还剩余额： %d" % (user.card.money))
        allmoney = Admin.getallmoney()
        allmoney -= money
        jl = "用户：", user.name, " 卡号：", user.card.cardId, " 取款:", money, "元 余额：", user.card.money, "元 Atm余额：", allmoney
        Admin.cqjl(jl)
        Admin.setallmoney(allmoney)

    def saveMoney(self):
        cardNum = input("请输入您的卡号：")
        #  验证是否存在该卡号
        user = self.allUser.get(cardNum)
        if not user:  # 如果有这个用户就不执行下面的语句，没有这个用户就执行
            print("该卡号不存在,存款失败...")
            return -1

        # 判断卡是否被锁定
        if user.card.cardLock:
            print("该卡被锁定,请解锁后在进行其他操作...")
            return -1

        #  验证密码
        if not self.checkPassword(user.card.password):
            print("密码输入错误,该卡已被锁定,请解锁后在进行其他操作...")
            user.card.cardLock = True
            return -1

        # 存款验证
        money = int(input("验证成功！！请输入您的存款金额："))
        if money < 0:
            print("存款金额有误，存款失败！")
            return -1
        # 开始存款
        user.card.money += money
        print("您存款%d元，最新余额为%d元！" % (money, user.card.money))
        allmoney = Admin.getallmoney()
        allmoney -= money
        Admin.setallmoney(allmoney)
        jl = "用户：", user.name, " 卡号：", user.card.cardId, "元 存款", money, " 余额", user.card.money, "元 总金额 ", allmoney, "元"
        Admin.cqjl(jl)

    #  转账
    def transferMoney(self):
        cardNum = input("请输入您的卡号：")
        #  验证是否存在该卡号
        user = self.allUser.get(cardNum)
        if not user:  # 如果有这个用户就不执行下面的语句，没有这个用户就执行
            print("该卡号不存在,转账失败...")
            return -1

        # 判断卡是否被锁定
        if user.card.cardLock:
            print("该卡被锁定,请解锁后在进行其他操作...")
            return -1

        #  验证密码
        if not self.checkPassword(user.card.password):
            print("密码输入错误,该卡已被锁定!请解锁后在进行其他操作...")
            user.card.cardLock = True
            return -1

        # 转账验证
        money = int(input("验证成功！！请输入您的转账金额："))
        if money > user.card.money or money < 0:
            print("金额有误，转账失败")
            return -1

        # 开始转账
        newcardNum = input("请输入转入账户：")
        toUser = self.allUser.get(newcardNum)
        if not toUser:
            print("该卡号不存在，转账失败！")
            return -1
        # 判断要转的账户是否锁定
        if toUser.card.cardLock:
            print("该卡已被锁定！！请解锁后再使用其功能！")
            return -1
        user.card.money -= money
        toUser.card.money += money
        time.sleep(1)
        print("转账成功，请稍后...")
        time.sleep(1)
        print("转账金额%d元，余额为%d元！" % (money, user.card.money))

    #  改密
    def changePasswd(self):
        cardNum = input("请输入您的卡号：")
        # 验证是否存在该卡号
        user = self.allUser.get(cardNum)
        if not user:
            print("该卡号不存在，改密失败！")
            return -1

        # 判断是否被锁
        if user.card.cardLock:
            print("该卡已锁定，请解锁后在使用其功能...")
            return -1

        # 验证密码
        if not self.checkPassword(user.card.password):
            print("密码输入错误,该卡已被锁定,请解锁后在进行其他操作...")
            user.card.cardLock = True
            return -1

        # 开始改密
        newPasswd = input("请输入新密码：")
        # 如果新密码和原始密码一样就判定为改密失败
        if not self.checkPassword(newPasswd):
            print("密码错误，改密失败")
            return -1
        user.card.password = newPasswd
        print("改密成功！！请稍后...")

    # 锁定
    def lockUser(self):
        cardId = input("请输入你要锁定的卡号：")
        # 验证是否存在卡号
        user = self.allUser.get(cardId)
        if not user:
            print("卡号不存在，锁定失败...")
            return -1
        # 验证卡是否被锁定
        if user.card.cardLock:
            print("该卡已被锁定！请解锁后在使用其他功能...")
            return -1

        # 验证密码,判断是否为本人
        if not self.checkPassword(user.card.password):
            print("密码输入错误！锁定失败...")
            return -1
        # 验证身份证号码
        tempId = input("请输入你的身份证号码：")
        if tempId != user.idCard:
            print("身份证号码输入错误，锁定失败...")
            return -1
        # 锁卡
        user.card.cardLock = True
        print("锁定成功...")

    # 解锁, 跟锁定逻辑相同
    def unlockUser(self):
        cardId = input("请输入你要解锁的卡号：")
        # 验证是否存在卡号
        user = self.allUser.get(cardId)
        if not user:
            print("卡号不存在，解锁失败...")
            return -1
        # 验证卡是否被锁定
        if not user.card.cardLock:
            print("该卡已被解锁！无需解锁...")
            return -1

        # 验证密码,判断是否为本人
        if not self.checkPassword(user.card.password):
            print("密码输入错误！解锁失败...")
            return -1
        # 验证身份证号码
        tempId = input("请输入你的身份证号码：")
        if tempId != user.idCard:
            print("身份证号码输入错误，解锁失败...")
            return -1
            # 锁卡
        user.card.cardLock = False
        print("解锁成功...")

    #  补卡
    def newCard(self):
        cardNum = input("请输入您的卡号：")
        # 验证是否存在该卡号
        # user = self.allUser.get(cardNum)
        user = self.allUser.get(cardNum)
        if not user:
            print("该卡号不存在")
            return -1

        tempname = input("请输入您的姓名：")
        tempidcard = input("请输入您的省份证号码：")
        tempphone = input("请输入您的手机号：")
        if tempname != self.allUser[cardNum].name \
                or tempidcard != self.allUser[cardNum].idCard \
                or tempphone != self.allUser[cardNum].phone:
            print("信息输入有误，补卡失败！")
            return -1
        newPasswd = input("请输入您的新密码：")
        if not self.checkPassword(newPasswd):
            print("密码错误，补卡失败！")
            return -1
        self.allUser[cardNum].card.cardPasswd = newPasswd
        time.sleep(1)
        print("补卡成功，请牢记您的新密码...")

    #  销户
    def killUser(self):
        cardNum = input("请输入您的卡号：")
        # 验证是否存在该卡号
        user = self.allUser.get(cardNum)
        if not user:
            print("该卡号不存在，销户！")
            return -1
        # 判断是否锁定
        if user.card.cardLock:
            print("该卡已锁定，请解锁后再使用其功能...")
            return -1

        # 验证密码
        if not self.checkPassword(user.card.password):
            print("密码输入有误，该卡已锁定,请解锁后再使用其功能...")
            user.card.cardLock = True
            return -1

        del self.allUser[cardNum]
        time.sleep(1)
        print("销户成功，请稍后！")

    # 判断密码是否输入正确
    def checkPassword(self, realPassword):
        # 输入正确，直接返回，输入错误，有三次判断机会
        for i in range(3):
            password = input("请输入你的密码：")
            if password == realPassword:
                return True
        return False

    # 随机生成6位数的卡号，并且保证了卡号唯一性
    def randomCardId(self):
        while True:
            str = ""
            for i in range(6):
                ch = chr(random.randrange(ord('0'), ord('9') + 1))
                str += ch
            # 判断是否重复,假如在字典里面能够根据卡号取到值，则说明卡号存在
            if not self.allUser.get(str):
                return str


# 主方法
def main():
    view = View()

    while True:
        view.paView()
        choice1 = input("请输入你的选择:")
        if choice1 == "1":
            atm = ATM()
            while True:
                # 每次执行操作前，先展示功能页面
                view.printSysFunctionView()
                # 等待用户选择操作
                option = input("请选择你的操作：")
                # 展示操作
                if option == "1":  # 当用户选择选项后调用ATM类
                    #  开户
                    atm.createUser()
                elif option == "2":
                    #  查询
                    atm.searchUserInfo()
                elif option == "3":
                    #  取款
                    atm.getMoney()
                elif option == "4":
                    #  存款
                    atm.saveMoney()
                elif option == "5":
                    #  转账
                    atm.transferMoney()
                elif option == "6":
                    #  改密码
                    atm.changePasswd()
                elif option == "7":
                    #  锁定
                    atm.lockUser()
                elif option == "8":
                    #  解锁
                    atm.unlockUser()
                elif option == "9":
                    #  补卡
                    atm.newCard()
                elif option == "0":
                    #  销户
                    atm.killUser()
                elif option == "q":
                    # 退出，将user信息保存在allusers.txt中，方面下次使用
                    f = open(filePath, "wb")
                    # 写入文件
                    pickle.dump(atm.allUser, f, 0)
                    f.close()
                    print("退出成功...")
                    break
                time.sleep(1)
        elif choice1 == "2":
            if view.login():
                while True:
                    view.printadminview()
                    choice = input("请选择你的操作")
                    if choice == "1":
                        allmoney = int(input("请输入总金额"))
                        admin.setallmoney(allmoney)
                    elif cjoice == "2":
                        jl = Admin.getjl()
                        for id, jl in jl:
                            print("序号：", id, " ----- 记录: ", jl)
                    elif choice == "3":
                        exit("已退出")

            else:
                print("错误")


main()
