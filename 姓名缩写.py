import pypinyin


# 不带声调的(style=pypinyin.NORMAL)
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s


# 带声调的(默认)
def yinjie(word):
    s = ''
    # heteronym=True开启多音字
    for i in pypinyin.pinyin(word, heteronym=True):
        s = s + ''.join(i) + " "
    return s


if __name__ == "__main__":
    print(pinyin("""李妍
饶瑞
马敬华
夏静
付金凤
李国英
步红
董蕾
李小华
孟令贺
倪准
耿艳
袁媛
胡艳青
郭红利
王晶晶
毕小丽
夏瑞娟
祁丽丽
王颖颖
马亚丽
王君
张雪阳
曹娟
石倩
王倩倩
王付丽
张春荣
程静静
李二阳
李婷
田秀丽
苏锦
班亚萍
崔紫娟
由利平
冯盼盼
马军琴
胡珊珊
张艳丽
郝青青
常盈
左士娜
冯子娟
王蕊
冉静静
张海利
李娟
娄林林
王卫霞
谢西宁
鲁莉莉
李秀芳
黄丽
白杨
翟利军
翟利鸽
王艳霞
齐焕
胡静
李春霞
郭梦真
王依
张怡晴
张泽颖
厉岩
刘艳杰
段园华
刘春雨
刘银
杨静静
沈彤
赵磊
王海艳
牛亚杰
徐娜
岳玲艳
马先唱
柏瑞
刘琳
刘素紧
李龙嫚
祁卫华
荣玥
赵军霞
王悦
王莹
赵华
崔凯悦
张甜甜
秦雅洁
段洛风
武梦奇
马丽平
孙敬元
宋月
李子妍
张亚丽
李夏青
赵欣梦
张玉洁
苏彩月
张倩
王杰
卞利芳
闫艳彩
徐白玉
卢真
朱双
张祎昕
赵蕊
杨灿灿
"""))