"""
Desktop Pet - ASCII desktop pet that follows your VS Code window.
Supports multiple pets (Duck, Cat) with switching.
Author: Claude Code
"""

import tkinter as tk
import random
import time
import win32gui


# ============================================================
# Pet Data Definitions
# ============================================================

PETS = {
    "duck": {
        "name": "🦆 嘎嘎 the Duck",
        "color": "#f0c040",
        "icon": "🦆",
        "idle": [
            (
                "    __      \n"
                " <(o )___   \n"
                "  ( ._> /   \n"
                "   `---'    \n"
            ),
            (
                "    __      \n"
                " <(- )___   \n"
                "  ( ._> /   \n"
                "   `---'    \n"
            ),
        ],
        "blink": (
            "    __      \n"
            " <(- )___   \n"
            "  ( ._> /   \n"
            "   `---'    \n"
        ),
        "happy": (
            "    __   ♥  \n"
            " <(^ )___   \n"
            "  ( ._> /   \n"
            "   `---'    \n"
        ),
        "excited": (
            "    __  !!  \n"
            " <(★ )___   \n"
            "  ( ._> /   \n"
            "   `---'    \n"
        ),
        "sleepy": (
            "    __  z Z \n"
            "  (- )___   \n"
            "  ( ._> /   \n"
            "   `---'    \n"
        ),
        "angry": (
            "    __   💢 \n"
            " <(> )___   \n"
            "  ( ._> /   \n"
            "   `---'    \n"
        ),
        "shocked": (
            "    __  !?  \n"
            " <(O )___   \n"
            "  ( ._> /   \n"
            "   `---'    \n"
        ),
        "eating": (
            "    __ ~🍞  \n"
            " <(o )___   \n"
            "  ( .~> /   \n"
            "   `---'    \n"
        ),
        "dancing_1": (
            "    __   ♪  \n"
            " <(^ )___   \n"
            "  ( ._>/    \n"
            "   `-~-'    \n"
        ),
        "dancing_2": (
            "    __  ♫   \n"
            " <(^ )___   \n"
            "   \\<._ )   \n"
            "    `-~-'   \n"
        ),
        "thinking": (
            "    __   ?  \n"
            "  (- )___ ° \n"
            "  ( ._> /   \n"
            "   `---'    \n"
        ),
        "love": (
            "    __ ♥♥♥  \n"
            " <(♥ )___   \n"
            "  ( ._> /   \n"
            "   `---'    \n"
        ),
        "special": (
            "    __      \n"
            " <(o )___   \n"
            "~~( .~>~~~~~\n"
            "~~~~~~~~~~~~\n"
        ),
        "wave_1": (
            "    __  /   \n"
            " <(o )_/_   \n"
            "  ( ._> /   \n"
            "   `---'    \n"
        ),
        "wave_2": (
            "    __ |    \n"
            " <(o )_/_   \n"
            "  ( ._> /   \n"
            "   `---'    \n"
        ),
        "dizzy": (
            "    __ @_@  \n"
            " <(@ )___   \n"
            "  ( ._> /   \n"
            "   `---'    \n"
        ),
        "cool": (
            "    __  😎  \n"
            " <(■ )___   \n"
            "  ( ._> /   \n"
            "   `---'    \n"
        ),
        "sad": (
            "    __  💧  \n"
            "  (; )___   \n"
            "  ( ._> /   \n"
            "   `---'    \n"
        ),
        "shout": (
            "    __ 嘎!! \n"
            " <(O )___   \n"
            "  ( .O> /   \n"
            "   `---'    \n"
        ),
        "drink": (
            "    __      \n"
            " <(- )___   \n"
            " 🧋( ._> /   \n"
            "   `---'    \n"
        ),
        "thoughts": [
            "写bug呢？", "该喝水了！🥤", "你好厉害！", "这代码能跑？",
            "休息一下吧~", "嘎嘎嘎！🦆", "我饿了...", "又在加班？",
            "代码写得不错嘛", "别忘了git commit!", "有bug的味道...",
            "要不要重构一下？", "我好无聊啊", "测试写了吗？",
            "摸鱼时间到！🐟", "陪你写代码~", "打个盹..zzz",
            "今天也辛苦了",              "你是最棒的！", "有面包吗？🍞", "我在看你写代码",
            "真的能编译过？", "周五了吗...",             "想去游泳~🏊", "嘎？", "要不试试重启？",
            "我是一只小鸭子🦆", "奶茶！奶茶！🧋", "太阳好大~☀",
            "下雨了要打伞🌧", "嘎嘎~跟我走！",
        ],
        "clicks": [
            "别戳我！>_<", "嘎？怎么了？", "嘎嘎！！",             "好痒~",   "我在呢~",
            "需要帮忙吗？", "摸摸头~",  "干活去！",
            "别摸了别摸了", "🦆 嘎嘎！", "我不是按钮！", "给我面包🍞",
            "嘎！吓我一跳", "你手好冰...", "翅膀都被你戳歪了",
            "轻点轻点~", "我又不是debug按钮", "求你了给口面包吧",
            "嘎嘎...好舒服", "我要告诉其他鸭子！",
            "你是在rubber duck debugging吗", "戳我能加薪吗？",
        ],
        "shout_text": "嘎嘎嘎嘎嘎!! 🦆",
        "feed_item": "🍞",
        "feed_text": "好吃好吃！🍞",
        "feed_done": "吃饱了~ 嘎！",
        "special_text": "游泳好开心~ 🏊",
        "special_label": "🏊 游泳",
        "cool_text": "我是最酷的鸭子 😎",
        "dance_text": "♪ 嘎嘎舞！♫",
        "bye_text": "拜拜~ 嘎！👋",
        "drag_text": "🦆 自由模式 (右键→跟随)",
    },
    "cat": {
        "name": "🐱 喵喵 the Cat",
        "color": "#c8a0ff",
        "icon": "🐱",
        "idle": [
            (
                "  /\\_/\\    \n"
                " ( o.o )   \n"
                "  > ^ <    \n"
                " /|   |\\   \n"
                "(_|   |_)  \n"
            ),
            (
                "  /\\_/\\    \n"
                " ( -._ )   \n"
                "  > ^ <    \n"
                " /|   |\\   \n"
                "(_|   |_)  \n"
            ),
        ],
        "blink": (
            "  /\\_/\\    \n"
            " ( -.- )   \n"
            "  > ^ <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "happy": (
            "  /\\_/\\  ♥ \n"
            " ( ^.^ )   \n"
            "  > ^ <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "excited": (
            "  /\\_/\\ !! \n"
            " ( ★.★ )   \n"
            "  > w <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "sleepy": (
            "  /\\_/\\ zZ \n"
            " ( -.- )   \n"
            "  > ω <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "angry": (
            "  /\\_/\\ 💢 \n"
            " ( >.< )   \n"
            "  > △ <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "shocked": (
            "  /\\_/\\ !? \n"
            " ( O.O )   \n"
            "  > o <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "eating": (
            "  /\\_/\\~🐟 \n"
            " ( >.< )   \n"
            "  >~w~<    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "dancing_1": (
            "  /\\_/\\  ♪ \n"
            " ( ^.^ )   \n"
            "  > ^ < /  \n"
            " /|   |    \n"
            "(_|   |_)  \n"
        ),
        "dancing_2": (
            "  /\\_/\\ ♫  \n"
            " ( ^.^ )   \n"
            "\\  > ^ <   \n"
            "    |   |\\ \n"
            " (_|   |_) \n"
        ),
        "thinking": (
            "  /\\_/\\  ? \n"
            " ( -.- ) ° \n"
            "  > ~ <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "love": (
            "  /\\_/\\♥♥♥ \n"
            " ( ♥.♥ )   \n"
            "  > ^ <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "special": (
            "     /\\_/\\ \n"
            "  ~ ( o.o )\n"
            "~~~~~> ^ < \n"
            "  ~ /| |\\  \n"
            "   (_|_|_) \n"
        ),
        "wave_1": (
            "  /\\_/\\    \n"
            " ( o.o )/  \n"
            "  > ^ <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "wave_2": (
            "  /\\_/\\ |  \n"
            " ( o.o )/  \n"
            "  > ^ <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "dizzy": (
            "  /\\_/\\@_@ \n"
            " ( @.@ )   \n"
            "  > ~ <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "cool": (
            "  /\\_/\\    \n"
            " ( ■.■ ) 😎\n"
            "  > ^ <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "sad": (
            "  /\\_/\\ 💧 \n"
            " ( ;.; )   \n"
            "  > n <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "shout": (
            "  /\\_/\\喵!!\n"
            " ( O.O )   \n"
            "  >!w!<    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "drink": (
            "  /\\_/\\    \n"
            " ( -.- )   \n"
            "  >🧋 <    \n"
            " /|   |\\   \n"
            "(_|   |_)  \n"
        ),
        "thoughts": [
            "写bug呢？", "该喝水了！🥤", "你好厉害！", "这代码能跑？",
            "休息一下吧~", "喵呜~🐱", "我饿了...", "又在加班？",
            "代码写得不错嘛", "别忘了git commit!", "有bug的味道...",
            "要不要重构一下？", "我好无聊啊", "测试写了吗？",
            "摸鱼时间到！🐟", "陪你写代码~", "打个盹..zzz",
            "今天也辛苦了",              "你是最棒的！", "有小鱼干吗？🐟", "我在看你写代码",
            "真的能编译过？", "周五了吗...",             "想晒太阳~☀", "喵？", "要不试试重启？",
            "我是一只小猫咪🐱", "奶茶！奶茶！🧋", "键盘好暖和~",
            "毛球要掉了...", "喵喵~蹭蹭你！",
        ],
        "clicks": [
            "别戳我！>_<", "喵？怎么了？", "喵喵！！",             "好痒~",   "我在呢~",
            "需要帮忙吗？", "摸摸头~",  "干活去！",
            "别摸了别摸了", "🐱 喵喵！", "我不是按钮！", "给我小鱼干🐟",
            "喵！吓我一跳", "你手好暖...", "耳朵都被你戳歪了",
            "轻点轻点~", "我又不是debug按钮", "求你了给口小鱼干吧",
            "呼噜噜...好舒服", "我要告诉其他猫咪！",
            "你是在rubber cat debugging吗", "戳我能加薪吗？",
        ],
        "shout_text": "喵喵喵喵喵!! 🐱",
        "feed_item": "🐟",
        "feed_text": "好吃好吃！🐟",
        "feed_done": "吃饱了~ 喵！",
        "special_text": "毛线球好好玩~ 🧶",
        "special_label": "🧶 玩毛线",
        "cool_text": "我是最酷的猫咪 😎",
        "dance_text": "♪ 喵喵舞！♫",
        "bye_text": "拜拜~ 喵！👋",
        "drag_text": "🐱 自由模式 (右键→跟随)",
    },
    "owl": {
        "name": "🦉 咕咕 the Owl",
        "color": "#c09060",
        "icon": "🦉",
        "idle": [
            " ,___,  \n (o,o)  \n /)  )  \n--\"-\"-- \n",
            " ,___,  \n (-,o)  \n /)  )  \n--\"-\"-- \n",
        ],
        "blink":    " ,___,  \n (-,-)  \n /)  )  \n--\"-\"-- \n",
        "happy":    " ,___,♥ \n (^,^)  \n /)  )  \n--\"-\"-- \n",
        "excited":  " ,___,!!\n (★,★)  \n /)  )  \n--\"-\"-- \n",
        "sleepy":   " ,___,zZ\n (-,-)  \n /)  )  \n--\"-\"-- \n",
        "angry":    " ,___,💢\n (>,<)  \n /)  )  \n--\"-\"-- \n",
        "shocked":  " ,___,!?\n (O,O)  \n /)  )  \n--\"-\"-- \n",
        "eating":   " ,___,🐛\n (o,o)~ \n /)  )  \n--\"-\"-- \n",
        "dancing_1":" ,___,♪ \n (^,^)  \n /) )/  \n--\"-\"-- \n",
        "dancing_2":" ,___,♫ \n (^,^)  \n\\(  (\\  \n--\"-\"-- \n",
        "thinking": " ,___,? \n (-,-)° \n /)  )  \n--\"-\"-- \n",
        "love":     " ,___,  \n (♥,♥)♥ \n /)  )  \n--\"-\"-- \n",
        "special":  " ,___,  \n (o,o)  \n~/)  )~ \n~\"-\"\"~~ \n",
        "wave_1":   " ,___,/ \n (o,o)  \n /)  )  \n--\"-\"-- \n",
        "wave_2":   " ,___,| \n (o,o)/ \n /)  )  \n--\"-\"-- \n",
        "dizzy":    " ,___,  \n (@,@)@ \n /)  )  \n--\"-\"-- \n",
        "cool":     " ,___,  \n (■,■)😎\n /)  )  \n--\"-\"-- \n",
        "sad":      " ,___,💧\n (;,;)  \n /)  )  \n--\"-\"-- \n",
        "shout":    " ,___,  \n (O,O)! \n /)>>) !\n--\"-\"-- \n",
        "drink":    " ,___,  \n (-,-)  \n /)🧋)  \n--\"-\"-- \n",
        "thoughts": [
            "写bug呢？", "该喝水了！🥤", "你好厉害！", "这代码能跑？",
            "休息一下吧~", "咕咕！🦉", "我饿了...", "又在加班？",
            "代码写得不错嘛", "别忘了git commit!", "有bug的味道...",
            "要不要重构一下？", "我好无聊啊", "测试写了吗？",
            "夜猫子报到！🌙", "陪你写代码~", "打个盹..zzz",
            "今天也辛苦了",              "你是最棒的！", "有虫子吗？🐛", "我在看你写代码",
            "真的能编译过？", "周五了吗...",             "月亮好圆~🌕", "咕？", "要不试试重启？",
            "我是一只猫头鹰🦉", "奶茶！奶茶！🧋", "夜深了~",
            "谁在叫我？", "咕咕~转头360°！",
        ],
        "clicks": [
            "别戳我！>_<", "咕？怎么了？", "咕咕！！",             "好痒~",   "我在呢~",
            "需要帮忙吗？", "摸摸头~",  "干活去！",
            "别摸了别摸了", "🦉 咕咕！", "我不是按钮！", "给我虫子🐛",
            "咕！吓我一跳", "你手好冰...", "羽毛都被你戳乱了",
            "轻点轻点~", "我又不是debug按钮", "戳我能加薪吗？",
        ],
        "shout_text": "咕~呜~咕~呜~!! 🦉",
        "feed_item": "🐛",
        "feed_text": "好吃好吃！🐛",
        "feed_done": "吃饱了~ 咕！",
        "special_text": "夜巡好刺激~ 🌙",
        "special_label": "🌙 夜巡",
        "cool_text": "我是最酷的猫头鹰 😎",
        "dance_text": "♪ 咕咕舞！♫",
        "bye_text": "拜拜~ 咕！👋",
        "drag_text": "🦉 自由模式 (右键→跟随)",
    },
    "shiba": {
        "name": "🐕 柴柴 the Shiba",
        "color": "#e8a040",
        "icon": "🐕",
        "idle": [
            " ∧＿∧   \n( ·ω· )  \n/ つ つ  \nしーＪ   \n",
            " ∧＿∧   \n( -ω- )  \n/ つ つ  \nしーＪ   \n",
        ],
        "blink":    " ∧＿∧   \n( -ω- )  \n/ つ つ  \nしーＪ   \n",
        "happy":    " ∧＿∧ ♥ \n( ^ω^ )  \n/ つ つ  \nしーＪ   \n",
        "excited":  " ∧＿∧ !!\n( ★ω★ )  \n/ つ つ  \nしーＪ   \n",
        "sleepy":   " ∧＿∧ zZ\n( -ω- )  \n/ つ つ  \nしーＪ   \n",
        "angry":    " ∧＿∧ 💢\n( >ω< )  \n/ つ つ  \nしーＪ   \n",
        "shocked":  " ∧＿∧ !?\n( Oω O)  \n/ つ つ  \nしーＪ   \n",
        "eating":   " ∧＿∧ 🍖\n( ·ω· )~ \n/ つ つ  \nしーＪ   \n",
        "dancing_1":" ∧＿∧ ♪ \n( ^ω^ )  \n/ つ つ/ \nしーＪ   \n",
        "dancing_2":" ∧＿∧ ♫ \n( ^ω^ )  \n\\つ つ\\  \nしーＪ   \n",
        "thinking": " ∧＿∧ ? \n( -ω- )° \n/ つ つ  \nしーＪ   \n",
        "love":     " ∧＿∧♥♥ \n( ♥ω♥ )  \n/ つ つ  \nしーＪ   \n",
        "special":  " ∧＿∧   \n( ^ω^ )  \n/ つ🦴つ \nしーＪ   \n",
        "wave_1":   " ∧＿∧ / \n( ·ω· )/ \n/ つ つ  \nしーＪ   \n",
        "wave_2":   " ∧＿∧ | \n( ·ω· )/ \n/ つ つ  \nしーＪ   \n",
        "dizzy":    " ∧＿∧   \n( @ω@ )@ \n/ つ つ  \nしーＪ   \n",
        "cool":     " ∧＿∧ 😎\n( ■ω■ )  \n/ つ つ  \nしーＪ   \n",
        "sad":      " ∧＿∧ 💧\n( ;ω; )  \n/ つ つ  \nしーＪ   \n",
        "shout":    " ∧＿∧   \n( Oω O)汪\n/ つ つ!!\nしーＪ   \n",
        "drink":    " ∧＿∧   \n( -ω- )  \n/ つ🧋つ \nしーＪ   \n",
        "thoughts": [
            "写bug呢？", "该喝水了！🥤", "你好厉害！", "这代码能跑？",
            "休息一下吧~", "汪汪！🐕", "我饿了...", "又在加班？",
            "代码写得不错嘛", "别忘了git commit!", "有bug的味道...",
            "要不要重构一下？", "我好无聊啊", "测试写了吗？",
            "摸鱼时间到！🐟", "陪你写代码~", "打个盹..zzz",
            "今天也辛苦了",              "你是最棒的！", "有骨头吗？🦴", "我在看你写代码",
            "真的能编译过？", "周五了吗...",             "想去散步~🌳", "汪？", "要不试试重启？",
            "我是一只柴犬🐕", "奶茶！奶茶！🧋", "尾巴摇摇~",
            "球球呢？🎾", "汪汪~蹭蹭你！",
        ],
        "clicks": [
            "别戳我！>_<", "汪？怎么了？", "汪汪！！",             "好痒~",   "我在呢~",
            "需要帮忙吗？", "摸摸头~",  "干活去！",
            "别摸了别摸了", "🐕 汪汪！", "我不是按钮！", "给我骨头🦴",
            "汪！吓我一跳", "你手好暖...", "耳朵都被你戳歪了",
            "轻点轻点~", "我又不是debug按钮", "戳我能加薪吗？",
            "尾巴摇起来了！", "呼噜噜...好舒服",
        ],
        "shout_text": "汪汪汪汪汪!! 🐕",
        "feed_item": "🍖",
        "feed_text": "好吃好吃！🍖",
        "feed_done": "吃饱了~ 汪！",
        "special_text": "捡骨头好开心~ 🦴",
        "special_label": "🦴 捡骨头",
        "cool_text": "我是最酷的柴犬 😎",
        "dance_text": "♪ 汪汪舞！♫",
        "bye_text": "拜拜~ 汪！👋",
        "drag_text": "🐕 自由模式 (右键→跟随)",
    },
    "dango": {
        "name": "🍡 团子 the Dango",
        "color": "#f0b0c0",
        "icon": "🍡",
        "idle": [
            "  .---.  \n ( ·_· ) \n (     ) \n  '---'  \n",
            "  .---.  \n ( -_- ) \n (     ) \n  '---'  \n",
        ],
        "blink":    "  .---.  \n ( -_- ) \n (     ) \n  '---'  \n",
        "happy":    "  .---. ♥\n ( ^_^ ) \n (     ) \n  '---'  \n",
        "excited":  "  .---.!!\n ( ★_★ ) \n (     ) \n  '---'  \n",
        "sleepy":   "  .---.zZ\n ( -_- ) \n (     ) \n  '---'  \n",
        "angry":    "  .---.💢\n ( >_< ) \n (     ) \n  '---'  \n",
        "shocked":  "  .---.!?\n ( O_O ) \n (     ) \n  '---'  \n",
        "eating":   "  .---.🍰\n ( ·_· )~\n (     ) \n  '---'  \n",
        "dancing_1":"  .---. ♪\n ( ^_^ ) \n ( / \\ ) \n  '-~-'  \n",
        "dancing_2":"  .---.♫ \n ( ^_^ ) \n ( \\ / ) \n  '-~-'  \n",
        "thinking": "  .---. ?\n ( -_- )°\n (     ) \n  '---'  \n",
        "love":     "  .---.  \n ( ♥_♥ )♥\n (     ) \n  '---'  \n",
        "special":  "  .---.  \n ( ^_^ ) \n ( 弹~ ) \n  '-^-'  \n",
        "wave_1":   "  .---./\n ( ·_· ) \n (     ) \n  '---'  \n",
        "wave_2":   "  .---.|\n ( ·_· )/\n (     ) \n  '---'  \n",
        "dizzy":    "  .---.  \n ( @_@ )@\n (     ) \n  '---'  \n",
        "cool":     "  .---.  \n ( ■_■ )😎\n (     ) \n  '---'  \n",
        "sad":      "  .---.💧\n ( ;_; ) \n (     ) \n  '---'  \n",
        "shout":    "  .---.  \n ( O_O )!\n ( !! ) !\n  '---'  \n",
        "drink":    "  .---.  \n ( -_- ) \n (🧋   ) \n  '---'  \n",
        "thoughts": [
            "写bug呢？", "该喝水了！🥤", "你好厉害！", "这代码能跑？",
            "休息一下吧~", "弹弹弹~🍡", "我饿了...", "又在加班？",
            "代码写得不错嘛", "别忘了git commit!", "有bug的味道...",
            "要不要重构一下？", "我好无聊啊", "测试写了吗？",
            "摸鱼时间到！🐟", "陪你写代码~", "打个盹..zzz",
            "今天也辛苦了",              "你是最棒的！", "有蛋糕吗？🍰", "我在看你写代码",
            "真的能编译过？", "周五了吗...",             "我是软的~", "弹？", "要不试试重启？",
            "我是一只团子🍡", "奶茶！奶茶！🧋", "好想被吃掉...",
            "别咬我！", "软软糯糯~",
        ],
        "clicks": [
            "别戳我！>_<", "弹？怎么了？", "弹弹！！",             "好痒~",   "我在呢~",
            "需要帮忙吗？", "摸摸头~",  "干活去！",
            "别摸了别摸了", "🍡 弹弹！", "我不是按钮！", "给我蛋糕🍰",
            "弹！吓我一跳", "你手好冰...", "被你戳扁了！",
            "轻点轻点~", "我又不是debug按钮", "戳我能加薪吗？",
            "弹弹弹...好舒服", "我好软你好狠",
        ],
        "shout_text": "弹弹弹弹弹!! 🍡",
        "feed_item": "🍰",
        "feed_text": "好吃好吃！🍰",
        "feed_done": "吃饱了~ 弹！",
        "special_text": "弹弹弹~ 好好玩！🍡",
        "special_label": "🍡 弹弹",
        "cool_text": "我是最酷的团子 😎",
        "dance_text": "♪ 弹弹舞！♫",
        "bye_text": "拜拜~ 弹！👋",
        "drag_text": "🍡 自由模式 (右键→跟随)",
    },
    "slime": {
        "name": "🟢 果冻 the Slime",
        "color": "#80e080",
        "icon": "🟢",
        "idle": [
            "  .~~~.  \n ( ·_· ) \n(       )\n `~~~~~' \n",
            "  .~~~.  \n ( -_- ) \n(       )\n `~~~~~' \n",
        ],
        "blink":    "  .~~~.  \n ( -_- ) \n(       )\n `~~~~~' \n",
        "happy":    "  .~~~. ♥\n ( ^_^ ) \n(       )\n `~~~~~' \n",
        "excited":  "  .~~~.!!\n ( ★_★ ) \n(       )\n `~~~~~' \n",
        "sleepy":   "  .~~~.zZ\n ( -_- ) \n(       )\n `~~~~~' \n",
        "angry":    "  .~~~.💢\n ( >_< ) \n(       )\n `~~~~~' \n",
        "shocked":  "  .~~~.!?\n ( O_O ) \n(       )\n `~~~~~' \n",
        "eating":   "  .~~~.🍬\n ( ·_· )~\n(       )\n `~~~~~' \n",
        "dancing_1":"  .~~~. ♪\n ( ^_^ ) \n(  / \\  )\n `~-~-~' \n",
        "dancing_2":"  .~~~.♫ \n ( ^_^ ) \n(  \\ /  )\n `~-~-~' \n",
        "thinking": "  .~~~. ?\n ( -_- )°\n(       )\n `~~~~~' \n",
        "love":     "  .~~~.  \n ( ♥_♥ )♥\n(       )\n `~~~~~' \n",
        "special":  "  .~~~.  \n ( ^_^ ) \n( 分裂! )\n `~~ ~~' \n",
        "wave_1":   "  .~~~./ \n ( ·_· ) \n(       )\n `~~~~~' \n",
        "wave_2":   "  .~~~.| \n ( ·_· )/\n(       )\n `~~~~~' \n",
        "dizzy":    "  .~~~.  \n ( @_@ )@\n(       )\n `~~~~~' \n",
        "cool":     "  .~~~.  \n ( ■_■ )😎\n(       )\n `~~~~~' \n",
        "sad":      "  .~~~.💧\n ( ;_; ) \n(       )\n `~~~~~' \n",
        "shout":    "  .~~~.  \n ( O_O )!\n( !!!! )\n `~~~~~' \n",
        "drink":    "  .~~~.  \n ( -_- ) \n(  🧋   )\n `~~~~~' \n",
        "thoughts": [
            "写bug呢？", "该喝水了！🥤", "你好厉害！", "这代码能跑？",
            "休息一下吧~", "咕噜噜~🟢", "我饿了...", "又在加班？",
            "代码写得不错嘛", "别忘了git commit!", "有bug的味道...",
            "要不要重构一下？", "我好无聊啊", "测试写了吗？",
            "摸鱼时间到！🐟", "陪你写代码~", "打个盹..zzz",
            "今天也辛苦了",              "你是最棒的！", "有糖果吗？🍬", "我在看你写代码",
            "真的能编译过？", "周五了吗...",             "我会分裂哦~", "咕噜？", "要不试试重启？",
            "我是一只果冻🟢", "奶茶！奶茶！🧋", "好黏好黏~",
            "别踩我！", "Q弹Q弹~",
        ],
        "clicks": [
            "别戳我！>_<", "咕噜？怎么了？", "咕噜噜！！",             "好痒~",   "我在呢~",
            "需要帮忙吗？", "摸摸头~",  "干活去！",
            "别摸了别摸了", "🟢 咕噜！", "我不是按钮！", "给我糖果🍬",
            "咕噜！吓我一跳", "你手好冰...", "被你戳变形了！",
            "轻点轻点~", "我又不是debug按钮", "戳我能加薪吗？",
            "黏黏的...好舒服", "我要分裂了！",
        ],
        "shout_text": "咕噜噜噜噜!! 🟢",
        "feed_item": "🍬",
        "feed_text": "好吃好吃！🍬",
        "feed_done": "吃饱了~ 咕噜！",
        "special_text": "分裂好好玩~ ✨",
        "special_label": "✨ 分裂",
        "cool_text": "我是最酷的果冻 😎",
        "dance_text": "♪ 咕噜舞！♫",
        "bye_text": "拜拜~ 咕噜！👋",
        "drag_text": "🟢 自由模式 (右键→跟随)",
    },
    "firefly": {
        "name": "✦ 萤萤 the Firefly",
        "color": "#e0e060",
        "icon": "✦",
        "idle": [
            " (\\  /)  \n ( ·· ) ✦\n  (  )   \n  /  \\   \n",
            " (\\  /)  \n ( ·· ) ·\n  (  )   \n  /  \\   \n",
        ],
        "blink":    " (\\  /)  \n ( -- ) ·\n  (  )   \n  /  \\   \n",
        "happy":    " (\\  /) ♥\n ( ^^ ) ✦\n  (  )   \n  /  \\   \n",
        "excited":  " (\\  /)!!\n ( ★★ ) ✦\n  (  )   \n  /  \\   \n",
        "sleepy":   " (\\  /)zZ\n ( -- ) ·\n  (  )   \n  /  \\   \n",
        "angry":    " (\\  /)💢\n ( >< ) ✦\n  (  )   \n  /  \\   \n",
        "shocked":  " (\\  /)!?\n ( OO ) ✦\n  (  )   \n  /  \\   \n",
        "eating":   " (\\  /) 🍯\n ( ·· )~✦\n  (  )   \n  /  \\   \n",
        "dancing_1":" (\\  /) ♪\n ( ^^ ) ✦\n  (  )/  \n  / \\    \n",
        "dancing_2":" (\\  /)♫ \n ( ^^ )✦ \n\\  (  )  \n  / \\    \n",
        "thinking": " (\\  /) ?\n ( -- ) °\n  (  )   \n  /  \\   \n",
        "love":     " (\\  /)  \n ( ♥♥ )✦♥\n  (  )   \n  /  \\   \n",
        "special":  " (\\  /)  \n ( ^^ )  \n  (✦✦)   \n ✦/  \\✦  \n",
        "wave_1":   " (\\  /) /\n ( ·· ) ✦\n  (  )   \n  /  \\   \n",
        "wave_2":   " (\\  /)| \n ( ·· )/✦\n  (  )   \n  /  \\   \n",
        "dizzy":    " (\\  /)  \n ( @@ )@✦\n  (  )   \n  /  \\   \n",
        "cool":     " (\\  /)  \n ( ■■ )😎\n  (  ) ✦ \n  /  \\   \n",
        "sad":      " (\\  /)💧\n ( ;; ) ·\n  (  )   \n  /  \\   \n",
        "shout":    " (\\  /)  \n ( OO )!!\n  (  )✦✦ \n  /  \\   \n",
        "drink":    " (\\  /)  \n ( -- ) ✦\n  (🧋)   \n  /  \\   \n",
        "thoughts": [
            "写bug呢？", "该喝水了！🥤", "你好厉害！", "这代码能跑？",
            "休息一下吧~", "闪闪闪~✦", "我饿了...", "又在加班？",
            "代码写得不错嘛", "别忘了git commit!", "有bug的味道...",
            "要不要重构一下？", "我好无聊啊", "测试写了吗？",
            "摸鱼时间到！🐟", "陪你写代码~", "打个盹..zzz",
            "今天也辛苦了",              "你是最棒的！", "有蜂蜜吗？🍯", "我在看你写代码",
            "真的能编译过？", "周五了吗...",             "夜里最亮的~✦", "闪？", "要不试试重启？",
            "我是一只萤火虫✦", "奶茶！奶茶！🧋", "一闪一闪~",
            "黑夜里的光！", "发光发光~✨",
        ],
        "clicks": [
            "别戳我！>_<", "闪？怎么了？", "闪闪！！",             "好痒~",   "我在呢~",
            "需要帮忙吗？", "摸摸头~",  "干活去！",
            "别摸了别摸了", "✦ 闪闪！", "我不是按钮！", "给我蜂蜜🍯",
            "闪！吓我一跳", "你手好暖...", "翅膀被你戳歪了",
            "轻点轻点~", "我又不是debug按钮", "戳我能加薪吗？",
            "亮晶晶...好舒服", "灯灭了灯灭了！",
        ],
        "shout_text": "闪闪闪闪闪!! ✦",
        "feed_item": "🍯",
        "feed_text": "好吃好吃！🍯",
        "feed_done": "吃饱了~ 闪！",
        "special_text": "全力发光~ ✨✨✨",
        "special_label": "✨ 发光",
        "cool_text": "我是最亮的萤火虫 😎",
        "dance_text": "♪ 闪闪舞！♫",
        "bye_text": "拜拜~ 闪！👋",
        "drag_text": "✦ 自由模式 (右键→跟随)",
    },
}


# ============================================================
# Themes
# ============================================================

THEMES = {
    "dark": {
        "bg": "#1e1e1e",
        "fg": "#cccccc",
        "status_fg": "#808080",
        "bubble_bg": "#333333",
        "bubble_fg": "#e0e0e0",
        "bubble_border": "#666666",
        "menu_bg": "#252526",
        "menu_fg": "#cccccc",
        "menu_active": "#094771",
        "entry_bg": "#333333",
        "entry_fg": "#ffffff",
        "btn_ok_bg": "#094771",
        "btn_cancel_bg": "#333333",
        "btn_fg": "#ffffff",
    },
    "light": {
        "bg": "#ffffff",
        "fg": "#222222",
        "status_fg": "#666666",
        "bubble_bg": "#f0f0f0",
        "bubble_fg": "#222222",
        "bubble_border": "#999999",
        "menu_bg": "#f5f5f5",
        "menu_fg": "#222222",
        "menu_active": "#cce4ff",
        "entry_bg": "#ffffff",
        "entry_fg": "#222222",
        "btn_ok_bg": "#0078d4",
        "btn_cancel_bg": "#e0e0e0",
        "btn_fg": "#ffffff",
    },
}


# ============================================================
# Main Pet Application
# ============================================================

class DesktopPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Desktop Pet")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.92)
        self.theme_name = "dark"
        self.theme = THEMES[self.theme_name]
        self.root.configure(bg=self.theme["bg"])

        # State
        self.current_pet = random.choice(list(PETS.keys()))
        self.current_mood = "idle"
        self.auto_switch_interval = 5 * 60 * 1000  # 5 min in ms
        self.auto_switch_enabled = True
        self.idle_frame = 0
        self.drag_data = {"x": 0, "y": 0}
        self.is_dragging = False
        self.offset_x = -20
        self.offset_y = -60
        self.manual_position = False
        self.vscode_hwnd = None
        self.last_vscode_check = 0
        self.bubble_visible = False
        self.click_count = 0
        self.last_click_time = 0

        t = self.theme
        # Main frame
        self.frame = tk.Frame(self.root, bg=t["bg"], padx=4, pady=2)
        self.frame.pack()

        # Speech bubble (hidden initially)
        self.bubble_frame = tk.Frame(self.frame, bg=t["bubble_bg"],
                                     highlightbackground=t["bubble_border"],
                                     highlightthickness=1, padx=6, pady=3)
        self.bubble_label = tk.Label(self.bubble_frame, text="",
                                     font=("Consolas", 9), fg=t["bubble_fg"],
                                     bg=t["bubble_bg"], wraplength=160,
                                     justify="left")
        self.bubble_label.pack()

        # Pet display
        self.pet_label = tk.Label(self.frame, text="",
                                  font=("Consolas", 12, "bold"),
                                  fg="#f0c040", bg=t["bg"],
                                  justify="left")
        self.pet_label.pack()

        # Status bar
        self.status_label = tk.Label(self.frame, text="",
                                     font=("Consolas", 8), fg=t["status_fg"],
                                     bg=t["bg"])
        self.status_label.pack()

        # Bind events
        self.pet_label.bind("<ButtonPress-1>", self.on_drag_start)
        self.pet_label.bind("<B1-Motion>", self.on_drag)
        self.pet_label.bind("<ButtonRelease-1>", self.on_release)
        self.pet_label.bind("<Button-3>", self.on_right_click)
        self.pet_label.bind("<Double-Button-1>", self.on_double_click)

        # Build menu and apply pet
        self.menu = tk.Menu(self.root, tearoff=0, bg=t["menu_bg"],
                            fg=t["menu_fg"], activebackground=t["menu_active"],
                            font=("Consolas", 9))
        self.apply_pet()

        # Start loops
        self.animate_idle()
        self.random_mood()
        self.random_thought()
        self.follow_vscode()
        self.auto_switch_loop()

        self.root.mainloop()

    @property
    def pet(self):
        return PETS[self.current_pet]

    def apply_pet(self):
        """Apply current pet's appearance and rebuild menu."""
        p = self.pet
        self.pet_label.config(text=p["idle"][0], fg=p["color"])
        self.status_label.config(text=p["name"])
        self.current_mood = "idle"
        self.rebuild_menu()

    def rebuild_menu(self):
        self.menu.delete(0, "end")
        p = self.pet
        feed_icon = p["feed_item"]
        self.menu.add_command(label=f"{feed_icon} 喂食", command=self.feed)
        self.menu.add_command(label="🧋 喝奶茶", command=self.drink)
        self.menu.add_command(label="💤 睡觉", command=self.sleep)
        self.menu.add_command(label=p["special_label"], command=self.special)
        self.menu.add_command(label="💃 跳舞", command=self.dance)
        self.menu.add_command(label="😎 耍酷", command=self.be_cool)
        self.menu.add_separator()

        t = self.theme
        # Switch pet submenu
        switch_menu = tk.Menu(self.menu, tearoff=0, bg=t["menu_bg"],
                              fg=t["menu_fg"], activebackground=t["menu_active"],
                              font=("Consolas", 9))
        for key, data in PETS.items():
            if key != self.current_pet:
                switch_menu.add_command(
                    label=data["name"],
                    command=lambda k=key: self.switch_pet(k))
        self.menu.add_cascade(label="🔄 切换宠物", menu=switch_menu)

        # Theme submenu
        theme_menu = tk.Menu(self.menu, tearoff=0, bg=t["menu_bg"],
                             fg=t["menu_fg"], activebackground=t["menu_active"],
                             font=("Consolas", 9))
        theme_menu.add_command(label="⚫ 黑色背景",
                               command=lambda: self.set_theme("dark"))
        theme_menu.add_command(label="⚪ 白色背景",
                               command=lambda: self.set_theme("light"))
        cur_theme_label = "⚫ 黑色" if self.theme_name == "dark" else "⚪ 白色"
        self.menu.add_cascade(label=f"🎨 背景 ({cur_theme_label})",
                              menu=theme_menu)

        if self.auto_switch_enabled:
            interval_min = self.auto_switch_interval // 60000
            self.menu.add_command(
                label=f"⏱ 自动切换 ({interval_min}分钟)",
                command=self.set_switch_interval)
        else:
            self.menu.add_command(
                label="⏱ 自动切换 (已关闭)",
                command=self.set_switch_interval)

        self.menu.add_separator()
        self.menu.add_command(label="📌 跟随VS Code",
                              command=self.reset_follow)
        self.menu.add_command(label="❌ 退出", command=self.quit_pet)

    def switch_pet(self, pet_key):
        self.current_pet = pet_key
        self.apply_pet()
        self.show_bubble(f"变身！我是{self.pet['name']}！", 3000)

    def set_theme(self, theme_name):
        if theme_name not in THEMES or theme_name == self.theme_name:
            self.rebuild_menu()
            return
        self.theme_name = theme_name
        self.theme = THEMES[theme_name]
        t = self.theme
        self.root.configure(bg=t["bg"])
        self.frame.configure(bg=t["bg"])
        self.bubble_frame.configure(bg=t["bubble_bg"],
                                    highlightbackground=t["bubble_border"])
        self.bubble_label.configure(bg=t["bubble_bg"], fg=t["bubble_fg"])
        self.pet_label.configure(bg=t["bg"])
        self.status_label.configure(bg=t["bg"], fg=t["status_fg"])
        self.menu.configure(bg=t["menu_bg"], fg=t["menu_fg"],
                            activebackground=t["menu_active"])
        self.rebuild_menu()
        label = "黑色" if theme_name == "dark" else "白色"
        self.show_bubble(f"已切换到{label}背景~", 2000)

    def auto_switch_loop(self):
        if self.auto_switch_enabled:
            others = [k for k in PETS if k != self.current_pet]
            self.switch_pet(random.choice(others))
        self.root.after(self.auto_switch_interval, self.auto_switch_loop)

    def set_switch_interval(self):
        t = self.theme
        dialog = tk.Toplevel(self.root)
        dialog.title("设置切换间隔")
        dialog.configure(bg=t["bg"])
        dialog.attributes("-topmost", True)
        dialog.geometry("260x150")
        dialog.resizable(False, False)

        tk.Label(dialog, text="自动切换间隔（分钟）：",
                 font=("Consolas", 10), fg=t["fg"], bg=t["bg"]
                 ).pack(pady=(15, 5))

        entry = tk.Entry(dialog, font=("Consolas", 12), width=8,
                         bg=t["entry_bg"], fg=t["entry_fg"],
                         insertbackground=t["entry_fg"],
                         justify="center")
        entry.insert(0, str(self.auto_switch_interval // 60000))
        entry.pack(pady=5)
        entry.focus_set()
        entry.select_range(0, "end")

        def apply():
            try:
                val = int(entry.get())
                if val <= 0:
                    self.auto_switch_enabled = False
                    self.show_bubble("自动切换已关闭", 2000)
                else:
                    self.auto_switch_interval = val * 60 * 1000
                    self.auto_switch_enabled = True
                    self.show_bubble(f"每 {val} 分钟自动切换~", 2000)
            except ValueError:
                pass
            dialog.destroy()
            self.rebuild_menu()

        entry.bind("<Return>", lambda e: apply())

        btn_frame = tk.Frame(dialog, bg=t["bg"])
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="确定", command=apply,
                  font=("Consolas", 9), bg=t["btn_ok_bg"], fg=t["btn_fg"],
                  width=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="取消", command=dialog.destroy,
                  font=("Consolas", 9), bg=t["btn_cancel_bg"], fg=t["btn_fg"],
                  width=8).pack(side="left", padx=5)

    # ----------------------------------------------------------
    # VS Code window tracking
    # ----------------------------------------------------------

    def find_vscode_window(self):
        result = []

        def enum_cb(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if "Visual Studio Code" in title or "VSCodium" in title:
                    result.append(hwnd)

        win32gui.EnumWindows(enum_cb, None)
        return result[0] if result else None

    def follow_vscode(self):
        if not self.manual_position:
            now = time.time()
            if now - self.last_vscode_check > 5 or self.vscode_hwnd is None:
                self.vscode_hwnd = self.find_vscode_window()
                self.last_vscode_check = now

            if self.vscode_hwnd:
                try:
                    rect = win32gui.GetWindowRect(self.vscode_hwnd)
                    x = rect[2] + self.offset_x - self.root.winfo_width()
                    y = rect[3] + self.offset_y - self.root.winfo_height()
                    sw = self.root.winfo_screenwidth()
                    sh = self.root.winfo_screenheight()
                    x = max(0, min(x, sw - self.root.winfo_width()))
                    y = max(0, min(y, sh - self.root.winfo_height()))
                    self.root.geometry(f"+{x}+{y}")
                except Exception:
                    self.vscode_hwnd = None

        self.root.after(500, self.follow_vscode)

    def reset_follow(self):
        self.manual_position = False
        self.status_label.config(text=f"{self.pet['icon']} 跟随VS Code")

    # ----------------------------------------------------------
    # Animation & Mood
    # ----------------------------------------------------------

    def set_art(self, art, color=None):
        self.pet_label.config(text=art)
        if color:
            self.pet_label.config(fg=color)

    def animate_idle(self):
        if self.current_mood == "idle":
            p = self.pet
            self.idle_frame = (self.idle_frame + 1) % len(p["idle"])
            if random.random() < 0.2:
                self.set_art(p["blink"], p["color"])
            else:
                self.set_art(p["idle"][self.idle_frame], p["color"])
        self.root.after(random.randint(800, 2000), self.animate_idle)

    def random_mood(self):
        p = self.pet
        if self.current_mood == "idle" and random.random() < 0.3:
            moods = [
                (p["happy"], p["color"], "happy", 3000),
                (p["thinking"], "#c586c0", "thinking", 4000),
                (p["love"], "#f44747", "love", 3000),
                (p["excited"], "#dcdcaa", "excited", 2500),
                (p["wave_1"], p["color"], "wave", 2000),
                (p["cool"], "#569cd6", "cool", 3000),
                (p["sleepy"], "#808080", "sleepy", 5000),
            ]
            art, color, mood, duration = random.choice(moods)
            self.current_mood = mood
            self.set_art(art, color)

            if mood == "wave":
                self.root.after(500, lambda: self.set_art(p["wave_2"], color))
                self.root.after(1000, lambda: self.set_art(p["wave_1"], color))

            self.root.after(duration, self.reset_mood)

        self.root.after(random.randint(8000, 20000), self.random_mood)

    def reset_mood(self):
        self.current_mood = "idle"
        p = self.pet
        self.set_art(p["idle"][0], p["color"])

    def random_thought(self):
        if not self.bubble_visible and random.random() < 0.25:
            self.show_bubble(random.choice(self.pet["thoughts"]))
        self.root.after(random.randint(15000, 40000), self.random_thought)

    # ----------------------------------------------------------
    # Speech bubble
    # ----------------------------------------------------------

    def show_bubble(self, text, duration=4000):
        self.bubble_label.config(text=text)
        self.bubble_frame.pack(before=self.pet_label, pady=(0, 2))
        self.bubble_visible = True
        self.root.after(duration, self.hide_bubble)

    def hide_bubble(self):
        self.bubble_frame.pack_forget()
        self.bubble_visible = False

    # ----------------------------------------------------------
    # Interactions
    # ----------------------------------------------------------

    def on_click(self, event):
        now = time.time()
        self.click_count += 1

        if now - self.last_click_time < 1.0:
            if self.click_count >= 5:
                self.current_mood = "dizzy"
                self.set_art(self.pet["dizzy"], "#ce9178")
                self.show_bubble("头好晕...别戳了！")
                self.click_count = 0
                self.root.after(3000, self.reset_mood)
                self.last_click_time = now
                return
        else:
            self.click_count = 1

        self.last_click_time = now
        self.show_bubble(random.choice(self.pet["clicks"]), 3000)

    def on_right_click(self, event):
        self.menu.post(event.x_root, event.y_root)

    def on_double_click(self, event):
        p = self.pet
        self.current_mood = "shout"
        self.set_art(p["shout"], p["color"])
        self.show_bubble(p["shout_text"], 2000)
        self.root.after(2000, self.reset_mood)

    def on_drag_start(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.is_dragging = False

    def on_drag(self, event):
        self.is_dragging = True
        self.manual_position = True
        x = self.root.winfo_x() + (event.x - self.drag_data["x"])
        y = self.root.winfo_y() + (event.y - self.drag_data["y"])
        self.root.geometry(f"+{x}+{y}")
        self.status_label.config(text=self.pet["drag_text"])

    def on_release(self, event):
        if not self.is_dragging:
            self.on_click(event)
        self.is_dragging = False

    # ----------------------------------------------------------
    # Actions (from context menu)
    # ----------------------------------------------------------

    def feed(self):
        p = self.pet
        self.current_mood = "eating"
        self.set_art(p["eating"], "#dcdcaa")
        self.show_bubble(p["feed_text"], 3000)
        self.root.after(3000, lambda: (
            self.set_art(p["happy"], p["color"]),
            self.show_bubble(p["feed_done"], 2000)
        ))
        self.root.after(5000, self.reset_mood)

    def drink(self):
        p = self.pet
        self.current_mood = "drinking"
        self.set_art(p["drink"], "#dcdcaa")
        self.show_bubble("吸溜~ 奶茶好喝！🧋", 3000)
        self.root.after(3000, lambda: (
            self.set_art(p["happy"], p["color"]),
            self.show_bubble("满足~ ♥", 2000)
        ))
        self.root.after(5000, self.reset_mood)

    def sleep(self):
        p = self.pet
        self.current_mood = "sleeping"
        self.set_art(p["sleepy"], "#808080")
        self.show_bubble("晚安...zzZ", 5000)
        self.root.after(8000, lambda: (
            self.show_bubble("睡醒了！", 2000),
        ))
        self.root.after(10000, self.reset_mood)

    def special(self):
        p = self.pet
        self.current_mood = "special"
        self.set_art(p["special"], "#4ec9b0")
        self.show_bubble(p["special_text"], 3000)
        self.root.after(4000, self.reset_mood)

    def dance(self):
        p = self.pet
        self.current_mood = "dancing"
        self.set_art(p["dancing_1"], "#c586c0")

        def dance_step(step):
            if step >= 6 or self.current_mood != "dancing":
                self.reset_mood()
                return
            art = p["dancing_1"] if step % 2 == 0 else p["dancing_2"]
            self.set_art(art, "#c586c0")
            self.root.after(400, lambda: dance_step(step + 1))

        self.show_bubble(p["dance_text"], 3000)
        dance_step(0)

    def be_cool(self):
        p = self.pet
        self.current_mood = "cool"
        self.set_art(p["cool"], "#569cd6")
        self.show_bubble(p["cool_text"], 3000)
        self.root.after(4000, self.reset_mood)

    def quit_pet(self):
        self.show_bubble(self.pet["bye_text"], 1000)
        self.root.after(1200, self.root.destroy)


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    DesktopPet()
