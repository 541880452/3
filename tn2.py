import streamlit as st
import random
import time
import requests
import json

st.set_page_config(page_title="植物大战僵尸", page_icon=None)

st.markdown("""
<style>
    .stButton > button {
        background-color: #add8e6 !important;
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

if "stage" not in st.session_state:
    st.session_state.stage = "menu"
    st.session_state.o = 0
    st.session_state.q = 0
    st.session_state.t = 0
    st.session_state.h = 0
    st.session_state.c = 0
    st.session_state.game_over = False
    st.session_state.win = False
    st.session_state.dev_mode = False
    st.session_state.dev_webhook = "https://oapi.dingtalk.com/robot/send?access_token=b05a06b5abe66c3a03d9f2c651c70b7a539176131c3030fa1309798aa4969dc3"
    st.session_state.dev_message = ""
    st.session_state.dev_at_all = False
    st.session_state.dev_count = 1
    st.session_state.bad_read = "你做阅读理解是只阅读不理解吗"
    st.session_state.exit_text = "怂了"
    st.session_state.bye_text = "跑路了兄弟们跑路了，跑就完了，慢点都得cos臊子"
    st.session_state.round_event = None
    st.session_state.round_step = None
    st.session_state.event_choice_6_7 = None

def send_dingtalk(webhook, message, at_all):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {"msgtype": "text", "text": {"content": message}, "at": {"isAtAll": at_all}}
    try:
        r = requests.post(webhook, data=json.dumps(data), headers=headers)
        return r.json()
    except:
        return {"error": "发送失败"}

def start_game(difficulty):
    mapping = {'1': (10, 1), '2': (7, 2), '3': (5, 3), '4': (2, 4), '5': (0, 5)}
    if difficulty in mapping:
        st.session_state.c, st.session_state.h = mapping[difficulty]
        st.session_state.o = 0
        st.session_state.q = 0
        st.session_state.t = 0
        st.session_state.game_over = False
        st.session_state.win = False
        st.session_state.round_event = None
        st.session_state.round_step = None
        st.session_state.event_choice_6_7 = None
        st.session_state.stage = "game"
    else:
        st.error(st.session_state.bad_read)

def describe_event(choice):
    if choice == 0:
        st.write("头牛：我帮你种个僵尸")
    elif choice == 1:
        st.write("头牛：我帮你铲个植物")
    elif choice == 2:
        st.write("头牛：我帮你给一个植物扣血")
    elif choice == 3:
        st.write("头牛：我给僵尸加点血")
    elif choice == 4:
        st.write("头牛：我帮你种个植物")
    elif choice == 5:
        st.write("头牛：我多帮你种几个")
    elif choice == 6:
        st.write("头牛：给我100阳光，我帮你铲几个植物")
    elif choice == 7:
        st.write("头羊：你好呀，我是头牛的弟弟头羊，今天我来指导你")
        st.write("头羊：给我200阳光，我给你400阳光")

def apply_event(choice, use_hammer=False):
    if use_hammer:
        st.success("哎呦喂")
        return
    h = st.session_state.h
    if choice == 0:
        if h in [1,2,3]:
            st.session_state.t += 1
        else:
            st.session_state.t += 3
    elif choice == 1:
        if h in [1,2,3]:
            st.session_state.q = max(0, st.session_state.q - 1)
        else:
            st.session_state.q = max(0, st.session_state.q - 3)
    elif choice == 2:
        if h in [1,2,3]:
            st.session_state.q = max(0, st.session_state.q - 0.5)
        else:
            st.session_state.q = max(0, st.session_state.q - 2)
    elif choice == 3:
        if h in [1,2,3]:
            st.session_state.t += 1
        else:
            st.session_state.t += 3
    elif choice == 4:
        if h in [1,2,3]:
            st.session_state.q += 1
        else:
            st.session_state.q += 0.5
    elif choice == 5:
        if h in [1,2,3]:
            st.session_state.t += 2
        else:
            st.session_state.t += 1
    elif choice == 6:
        if st.session_state.o >= 100:
            st.session_state.o -= 100
            st.session_state.q = max(0, st.session_state.q - 1)
        else:
            st.warning("阳光不足")
    elif choice == 7:
        if st.session_state.h == 1:
            st.session_state.o += 200
        else:
            st.write("你被骗了")
            st.session_state.o = max(0, st.session_state.o - 200)

def check_win_loss():
    h = st.session_state.h
    q = st.session_state.q
    t = st.session_state.t
    win_conditions = {1:4, 2:6, 3:10, 4:15, 5:20}
    lose_conditions = {1:30, 2:20, 3:10, 4:7, 5:5}
    if h in win_conditions and q >= win_conditions[h]:
        st.session_state.win = True
        st.session_state.game_over = True
        return
    if h in lose_conditions and t >= lose_conditions[h]:
        st.session_state.game_over = True

def battle():
    if st.session_state.q > 0 and st.session_state.t >= 2:
        st.session_state.q -= 0.5
        st.session_state.t -= 2

st.title("植物大战僵尸")

if st.session_state.stage == "menu":
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("开始游戏", key="menu_start"):
            st.session_state.stage = "difficulty"
            st.rerun()
    with col2:
        dev_input = st.text_input("", key="dev_key_input", type="password", label_visibility="collapsed")
        if dev_input == "114514":
            st.session_state.stage = "dev"
            st.rerun()
    with col3:
        if st.button("退出", key="menu_exit"):
            st.session_state.stage = "exit"
            st.rerun()

elif st.session_state.stage == "dev":
    st.subheader("开发者模式")
    st.success("密码正确，已进入开发者模式")
    st.write("---")
    st.write("钉钉机器人发送")
    message = st.text_area("请输入需要发送的消息", key="dev_message")
    at_all = st.checkbox("@所有人", key="dev_atall")
    count = st.number_input("循环发送？输入次数(1-20)", min_value=1, max_value=20, value=1, key="dev_count")
    if st.button("发送", key="dev_send"):
        full_message = "[皇上诏曰]:" + message
        for i in range(int(count)):
            result = send_dingtalk(st.session_state.dev_webhook, full_message, at_all)
            st.write(f"发送结果：{result}")
            time.sleep(1)
        st.success("发送完成")
    if st.button("返回主菜单", key="dev_back"):
        st.session_state.stage = "menu"
        st.rerun()

elif st.session_state.stage == "exit":
    st.warning("真怂呀你")
    if st.button("重新进入", key="exit_restart"):
        st.session_state.stage = "menu"
        st.rerun()

elif st.session_state.stage == "difficulty":
    st.subheader("请选择难度")
    difficulty = st.selectbox("难度", ["1.宝宝", "2.简单", "3.普通", "4.困难", "5.噩梦"], key="difficulty_select")
    if st.button("确认", key="difficulty_confirm"):
        diff_num = difficulty[0]
        start_game(diff_num)
        st.rerun()
    if st.button("返回", key="difficulty_back"):
        st.session_state.stage = "menu"
        st.rerun()

elif st.session_state.stage == "game":
    check_win_loss()
    if st.session_state.game_over:
        if st.session_state.win:
            st.balloons()
            st.success("你竟然赢了，我一定会回来的")
        else:
            st.error("你失败了")
        st.write("---")
        st.write("是否鞭尸？")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("是", key="gameover_t"):
                st.write("哎呦喂\n" * 20)
                st.write("我错了,饶了我吧:")
                col3, col4 = st.columns(2)
                with col3:
                    if st.button("t", key="gameover_t_t"):
                        st.write("我错哪了我错了,我一点都没错")
                with col4:
                    if st.button("f", key="gameover_t_f"):
                        st.write("哎呦喂" * 100)
        with col2:
            if st.button("否", key="gameover_f"):
                st.write(st.session_state.bye_text)
        col5, col6 = st.columns(2)
        with col5:
            if st.button("再来一次", key="gameover_a"):
                st.session_state.stage = "difficulty"
                st.rerun()
        with col6:
            if st.button("退出", key="gameover_other"):
                st.write("我跑路了")
                st.session_state.stage = "exit"
                st.rerun()
        st.stop()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("阳光", int(st.session_state.o))
    with col2:
        val = st.session_state.q
        st.metric("植物", int(val) if val.is_integer() else val)
    with col3:
        st.metric("僵尸", int(st.session_state.t))
    with col4:
        st.metric("锤子", st.session_state.c)

    st.write("---")

    if st.session_state.round_step is None:
        if st.button("下一回合", key="game_next"):
            st.session_state.o += 50
            if st.session_state.h in [1,2,3]:
                st.session_state.t += 1
            else:
                st.session_state.t += 3
            st.session_state.round_event = random.randint(0,7)
            st.session_state.round_step = "plant"
            st.rerun()

    if st.session_state.round_step == "plant":
        if st.session_state.o >= 100:
            st.write("是否种植植物？")
            col_plant1, col_plant2 = st.columns(2)
            with col_plant1:
                if st.button("种植", key="plant_yes"):
                    st.session_state.o -= 100
                    st.session_state.q += 1
                    st.session_state.round_step = "event"
                    st.rerun()
            with col_plant2:
                if st.button("不种植", key="plant_no"):
                    st.session_state.round_step = "event"
                    st.rerun()
        else:
            st.session_state.round_step = "event"
            st.rerun()

    if st.session_state.round_step == "event":
        event = st.session_state.round_event
        describe_event(event)

        if event == 6:
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                if st.button("同意", key="event6_yes"):
                    st.session_state.event_choice_6_7 = "yes"
            with col_a2:
                if st.button("拒绝", key="event6_no"):
                    st.session_state.event_choice_6_7 = "no"
        elif event == 7:
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("同意", key="event7_yes"):
                    st.session_state.event_choice_6_7 = "yes"
            with col_b2:
                if st.button("拒绝", key="event7_no"):
                    st.session_state.event_choice_6_7 = "no"

        st.write("---")
        st.write("是否使用锤子？")
        col_h1, col_h2 = st.columns(2)
        use_hammer = False
        with col_h1:
            if st.button("使用", key="hammer_yes"):
                use_hammer = True
        with col_h2:
            if st.button("不使用", key="hammer_no"):
                use_hammer = False
        if 'hammer_chosen' not in st.session_state:
            st.session_state.hammer_chosen = None

        if use_hammer:
            st.session_state.hammer_chosen = True
            st.session_state.round_step = "battle"
            apply_event(event, use_hammer=True)
            st.rerun()
        elif use_hammer is False:
            st.session_state.hammer_chosen = False
            if event in [6,7]:
                if st.session_state.event_choice_6_7 == "yes":
                    apply_event(event, use_hammer=False)
            else:
                apply_event(event, use_hammer=False)
            st.session_state.round_step = "battle"
            st.rerun()

    if st.session_state.round_step == "battle":
        battle()
        st.session_state.round_event = None
        st.session_state.round_step = None
        st.session_state.event_choice_6_7 = None
        st.rerun()

    if st.button("返回主菜单", key="game_back"):
        st.session_state.stage = "menu"
        st.rerun()