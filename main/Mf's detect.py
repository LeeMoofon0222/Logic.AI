import datetime
from tkinter import filedialog
import cv2
from ultralytics import YOLO
import customtkinter as ctk
from PIL import Image
import time
import tkinter as tk

# ================================= setting up the appearance ======================================
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.geometry("1400x600")
root.title("logicAI")

# ==================================================================================================
# ======================================== video frame =============================================
# ==================================================================================================

# ===================================== create video frame =========================================
video_frame = ctk.CTkFrame(master=root, width=700, height=500)
video_frame.grid(pady=0, padx=20)
image_label = ctk.CTkLabel(video_frame, text='', width=video_frame.cget("width"),
                           height=video_frame.cget("height") + 10)
image_label.grid(column=0, padx=50)  # display image with a CTkLabel
frame_list = []

# ===================================== create video control frame =================================
video_control_frame = ctk.CTkFrame(master=root, width=600, height=400)
video_control_frame.grid(pady=0, padx=20)

play = 1
loadmp4 = False
current_value = 0.0


def play_pause():
    """ pauses and plays """
    global play
    if play == 1:
        play = 0
    else:
        play = 1


def update_slider():
    current_value = progress_value.get()
    if current_value < 3531:
        progress_value.set(current_value + 1)


# ========================================== Elements ================================================
row = 2
play_pause_btn = ctk.CTkButton(master=video_control_frame, text="Play/Pause", command=play_pause, width=20)
play_pause_btn.grid(row=2, column=0, pady=5, padx=20, sticky='w')

start_time = ctk.CTkLabel(video_control_frame, text=str(datetime.timedelta(seconds=0)))
start_time.grid(row=2, column=3, padx=20, sticky='nsew')

progress_value = tk.IntVar(video_control_frame)
progress_slider = ctk.CTkSlider(video_control_frame, variable=progress_value, from_=0, to=3531,
                                orientation="horizontal")

progress_slider.grid(row=2, column=4)

end_time = ctk.CTkLabel(video_control_frame, text=str(datetime.timedelta(seconds=141)))
end_time.grid(row=2, column=5, padx=20)
# ==================================================================================================
# ======================================== create tabview ==========================================
# ==================================================================================================
tabview = ctk.CTkTabview(root, width=250, height=500)
tabview.grid(row=0, column=2, padx=(20, 10), pady=(10, 0), sticky="nsew")
# tabview.add("上傳回測影片")
tabview.add("計算與呈現")
tabview.add("動作設定")
tabview.add("步驟")
tabview.add("結果")
# ==================================================================================================
# ======================================== for the model ===========================================
# ==================================================================================================
status_list = ['take', 'split', 'put_straw', 'put_milk']
status_setting_dictionary = {f'{status_list[i]}': {'bias_second': 0, 'reset_step': False} for i in
                             range(len(status_list))}  # create a space to put the configurations
status_order = [0 for i in range(len(status_list))]  # status的順序

model = YOLO(r"C:\NTUT\subjects\111-2\AI\FINAL DEMO\0_MODEL\runs\detect\train3\weights\best.pt")
video_path = r"C:\NTUT\subjects\111-2\AI\FINAL DEMO\0_MODEL\milk_vid.mp4"
# model = YOLO("best.pt")
# video_path = "milk_vid.mp4"
cap = cv2.VideoCapture(video_path)

# =========================================== cal_time ============================================
label_time = {'take': 0, 'split': 0, 'put_straw': 0, 'put_milk': 0}  # [take, split, put_straw, put_milk]
last_time_ = 0
counts = 0
count_num1 = 0
count_num2 = 0
count_num3 = 0
count_num4 = 0
count_nothing = 0
duration_time = 0
duration_start = 0
duration_num1 = 0


# ==================================================================================================
# ======================================== 0.影片撥放 ================================================
# ==================================================================================================

# ======================================== callbacks ===============================================

# ========================================= element ================================================
# ==================================================================================================
# ======================================== 1.計算與呈現 ==============================================
# ==================================================================================================
# ======================================= callbacks ================================================
def load_video_button_callback():
    global video_path
    global cap
    global loadmp4
    loadmp4 = True
    file_path = filedialog.askopenfilename()
    if file_path:
        cap = cv2.VideoCapture(video_path)
        load_video_button.configure(text="影片已上傳")


def load_model_button_callback():
    global model
    model_path = filedialog.askopenfilename()
    if model_path:
        load_model_button.configure(text="模型已上傳")


bbox = False  # 是否要顯示bounding box


def bbox_checkbox_callback():
    global bbox
    if bbox_checkbox.get() == 'on':
        bbox = True
    else:
        bbox = False


# ========================================= element ================================================
load_video_button = ctk.CTkButton(tabview.tab("計算與呈現"), text="上傳影片", width=70, font=("Roboto", 14),
                                  command=load_video_button_callback)
load_video_button.grid(row=0, column=0, padx=0, pady=10)

load_model_button = ctk.CTkButton(tabview.tab("計算與呈現"), text="上傳模型", width=70, font=("Roboto", 14),
                                  command=load_model_button_callback)
load_model_button.grid(row=1, column=0, padx=0, pady=10)

data_show_label = ctk.CTkLabel(tabview.tab("計算與呈現"), text="資料呈現方式", width=230, font=("Roboto", 14))
data_show_label.grid(row=2, column=0, padx=10, pady=0)

data_show_menu = ctk.CTkOptionMenu(tabview.tab("計算與呈現"), values=["加在外框"], width=230)
data_show_menu.grid(row=3, column=0, padx=20, pady=(0, 10))

apply_mode_label = ctk.CTkLabel(tabview.tab("計算與呈現"), text="應用模式", width=230, font=("Roboto", 14))
apply_mode_label.grid(row=4, column=0, padx=0, pady=0)

mode_select = ctk.CTkSegmentedButton(tabview.tab("計算與呈現"), values=["獨立計算", "獨立SOP", "共用SOP", "警報"], width=230)
mode_select.grid(row=5, column=0, padx=0, pady=0)

bbox_checkbox = ctk.CTkCheckBox(tabview.tab("計算與呈現"), text="顯示bounding box", onvalue="on", offvalue="off",
                                command=bbox_checkbox_callback)
bbox_checkbox.grid(row=6, column=0, padx=0, pady=20)

# ==================================================================================================
# ========================================= 2.動作設定 ===============================================
# ==================================================================================================

# ========================================= callbacks ==============================================
plus_button_count = 0
label_text_button_list = []


def select_label_menu_callback(choice):
    bias_second_entry.configure(placeholder_text=0)


def bias_second_enter_callback():
    if bias_second_entry.get() != '':
        status_setting_dictionary[f'{select_label_menu.get()}']['bias_second'] = float(bias_second_entry.get())
    print(status_setting_dictionary)


def checkbox_callback():
    if checkbox.get() == 'on':
        status_setting_dictionary[f'{select_label_menu.get()}']['reset_step'] = True
    else:
        status_setting_dictionary[f'{select_label_menu.get()}']['reset_step'] = False
    print(status_setting_dictionary)


# ========================================= elements ================================================

select_label = ctk.CTkLabel(tabview.tab("動作設定"), text="選擇狀態", width=60, font=("Roboto", 14))
select_label.grid(row=0, column=0, padx=0, pady=0)

select_label_menu = ctk.CTkOptionMenu(tabview.tab("動作設定"), values=status_list,
                                      width=230, command=select_label_menu_callback)
select_label_menu.grid(row=1, column=0, padx=20, pady=(0, 10))

bias_second_label = ctk.CTkLabel(tabview.tab("動作設定"), text="誤差秒數", width=60, font=("Roboto", 14))
bias_second_label.grid(row=2, column=0, padx=0, pady=0)

bias_second_entry = ctk.CTkEntry(tabview.tab("動作設定"), width=40, height=20, border_width=2,
                                 corner_radius=0)
bias_second_entry.grid(row=3, column=0, padx=0, pady=5)
bias_second_entry.configure(placeholder_text=0)

bias_second_enter = ctk.CTkButton(tabview.tab("動作設定"), text="Enter", width=20, height=25, border_width=2,
                                  corner_radius=10, command=bias_second_enter_callback)
bias_second_enter.grid(row=4, column=0, padx=20, pady=5)

checkbox = ctk.CTkCheckBox(tabview.tab("動作設定"), text="設為重製步驟", onvalue="on", offvalue="off",
                           command=checkbox_callback)
checkbox.grid(row=5, column=0, padx=0, pady=5)

# ==================================================================================================
# =========================================== 3.步驟 ================================================
# ==================================================================================================

# ========================================== callbacks =============================================
step_count = 0


def add_step_button_callback():
    global step_count
    if step_count < len(status_list):
        selected_status = select_status.get()
        status_order[step_count] = (selected_status)
        step_count += 1
        print(status_order)
        steps_label = ctk.CTkLabel(master=step_display_frame,
                                   text=f"{step_count}. {selected_status}",
                                   fg_color="gray", text_color="white", corner_radius=5, width=200)
        steps_label.grid(pady=5, padx=0)


def finish_button_callback():
    if finish_button.cget('text') == "設定完成":
        finish_button.configure(text='已完成設定')


# =========================================== Elements =============================================

# status selector
status_label = ctk.CTkLabel(tabview.tab("步驟"), text="選擇狀態", width=230, font=("Roboto", 14))
status_label.grid(row=2, column=0, padx=20, pady=0)
select_status = ctk.CTkOptionMenu(tabview.tab("步驟"), values=status_list, width=230)
select_status.grid(row=3, column=0, padx=20, pady=(0, 10))
select_status.set(f"{status_list[0]}")

# add a step
add_step_button = ctk.CTkButton(tabview.tab("步驟"), text="+新增步驟", command=add_step_button_callback,
                                width=230)
add_step_button.grid(row=4, column=0, padx=20, pady=5)

# create scrollable frame
step_display_frame = ctk.CTkScrollableFrame(tabview.tab("步驟"), width=230)
step_display_frame.grid(row=5, column=0, padx=20, pady=5)
step_display_frame.grid_columnconfigure(0, weight=1)
steps = 3

finish_button = ctk.CTkButton(tabview.tab("步驟"), text="設定完成", width=70, command=finish_button_callback)
finish_button.grid(row=6, column=0)


# ==================================================================================================
# ========================================== 4.結果 =================================================
# ==================================================================================================
# ======================================== call_back ===============================================

def play_pause_button_callback():
    if play_pause_button.cget("text") == '播放':
        play_pause_button.configure(text='暫停')
    else:
        play_pause_button.configure(text='播放')


# ========================================== Elements ================================================


play_pause_button = ctk.CTkButton(tabview.tab("結果"), text='播放', width=60, font=("Roboto", 14),
                                  command=play_pause_button_callback)
play_pause_button.grid(row=0, column=0, padx=0, pady=0)

select_label = ctk.CTkLabel(tabview.tab("結果"), text="持續時間", width=60, font=("Roboto", 14))
select_label.grid(row=1, column=0, padx=0, pady=10)

add_step_button_all = ctk.CTkButton(tabview.tab("結果"), text="0", width=150, hover=False)
add_step_button_all.grid(row=1, column=1, padx=30, pady=0)

select_label0 = ctk.CTkLabel(tabview.tab("結果"), text=f"{status_order[0]}", width=60, font=("Roboto", 14))
select_label0.configure(text=f'{status_order[0]}')
select_label0.grid(row=2, column=0, padx=0, pady=10)

add_step_button_label1 = ctk.CTkButton(tabview.tab("結果"), text="0", width=150, hover=False)
add_step_button_label1.grid(row=2, column=1, padx=30, pady=0)

select_label1 = ctk.CTkLabel(tabview.tab("結果"), text=f"{status_order[1]}", width=60, font=("Roboto", 14))
select_label1.configure(text=f'{status_order[1]}')
select_label1.grid(row=3, column=0, padx=0, pady=10)

add_step_button_label2 = ctk.CTkButton(tabview.tab("結果"), text="0", width=150, hover=False)
add_step_button_label2.grid(row=3, column=1, padx=30, pady=0)

select_label2 = ctk.CTkLabel(tabview.tab("結果"), text=f"{status_order[2]}", width=60, font=("Roboto", 14))
select_label2.configure(text=f'{status_order[2]}')
select_label2.grid(row=4, column=0, padx=0, pady=10)

add_step_button_label3 = ctk.CTkButton(tabview.tab("結果"), text="0", width=150, hover=False)
add_step_button_label3.grid(row=4, column=1, padx=30, pady=0)

select_label3 = ctk.CTkLabel(tabview.tab("結果"), text=f"{status_order[3]}", width=60, font=("Roboto", 14))
select_label3.configure(text=f'{status_order[3]}')
select_label3.grid(row=5, column=0, padx=0, pady=10)

add_step_button_label4 = ctk.CTkButton(tabview.tab("結果"), text="0", width=150, hover=False)
add_step_button_label4.grid(row=5, column=1, padx=30, pady=0)

latest_time_label = ctk.CTkLabel(tabview.tab("結果"), text="單輪執行時間", width=60, font=("Roboto", 14))
latest_time_label.grid(row=6, column=0, padx=0, pady=10)

latest_time_button = ctk.CTkButton(tabview.tab("結果"), text="0", width=150, hover=False)
latest_time_button.grid(row=6, column=1, padx=30, pady=0)

work_counts_label = ctk.CTkLabel(tabview.tab("結果"), text="已完成次數", width=60, font=("Roboto", 14))
work_counts_label.grid(row=7, column=0, padx=0, pady=10)

work_counts_button = ctk.CTkButton(tabview.tab("結果"), text=str(counts), width=60, hover=False)
work_counts_button.grid(row=7, column=1, padx=30, pady=0)

# ================================================UI設定結束=================================================
while cap.isOpened() and finish_button.cget('text') != '已完成設定':
    while play == 1 and finish_button.cget('text') != '已完成設定':
        current_value = progress_value.get()
        success, frame = cap.read()
        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame)
            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            if loadmp4:
                frame_list.append(annotated_frame)
                update_slider()
                # print(current_value,len(frame_list))
                if (current_value + 1 == len(frame_list)):
                    img = cv2.resize(annotated_frame, (video_frame.cget("width"), video_frame.cget("height")), interpolation=cv2.INTER_AREA)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(img)
                    # Display the annotated frame
                    my_image = ctk.CTkImage(light_image=img, size=(video_frame.cget("width"), video_frame.cget("height")))
                    image_label.configure(image=my_image)
                elif (current_value + 1 < len(frame_list)):
                    while current_value + 1 != len(frame_list) and play == 1:
                        # print(current_value,len(frame_list))
                        img = cv2.resize(frame_list[current_value], (video_frame.cget("width"), video_frame.cget("height")), interpolation=cv2.INTER_AREA)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(img)
                        # Display the annotated frame
                        my_image = ctk.CTkImage(light_image=img, size=(video_frame.cget("width"), video_frame.cget("height")))
                        image_label.configure(image=my_image)
                        cv2.waitKey(45)
                        root.update()
                        video_control_frame.update()
                        video_frame.update()
                        current_value = progress_value.get()
                        update_slider()

            root.update()
            video_frame.update()
            video_control_frame.update()
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            # Break the loop if the end of the video is reached
            break
    video_control_frame.update()
cap.release()
# ===============================================UI介面展示================================================
cap = cv2.VideoCapture(video_path)
while True:
    root.update()
    if finish_button.cget('text') == '已完成設定':
        select_label0.configure(text=f'{status_order[0]}')
        select_label1.configure(text=f'{status_order[1]}')
        select_label2.configure(text=f'{status_order[2]}')
        select_label3.configure(text=f'{status_order[3]}')
        while play_pause_button.cget('text') == '暫停':
            update_slider()
            number = 9
            number2 = 9
            # Read a frame from the video
            success, frame = cap.read()

            if success:
                root.update()
                # Run YOLOv8 inference on the frame
                start_time = time.time()

                results = model(frame)
                # Visualize the results on the frame
                annotated_frame = results[0].plot(boxes=bbox)
                print(bbox)
                img = cv2.resize(annotated_frame, (video_frame.cget("width"), video_frame.cget("height")),
                                 interpolation=cv2.INTER_AREA)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                # Display the annotated frame
                my_image = ctk.CTkImage(light_image=img, size=(video_frame.cget("width"), video_frame.cget("height")))
                image_label.configure(image=my_image)

                # to analyze diff obj=====================================================
                empty_tensor = results[0].boxes.cls
                # Check if the tensor is empty
                if empty_tensor.numel() == 1:
                    # Get the number from the tensor
                    number = empty_tensor.item()
                    # print(number)
                elif empty_tensor.numel() == 2:
                    number = empty_tensor[0].item()
                    number2 = empty_tensor[1].item()
                    # print(number)
                    # print(number2)
                else:
                    print("not detect")

                end_time = time.time()
                last_time = last_time_ + end_time - start_time
                last_time_ = last_time  # memory the time

                add_step_button_all.configure(text=str(round(last_time, 1)))

                num1 = status_order.index("take") + 1
                num2 = status_order.index("split") + 1
                num3 = status_order.index("put_straw") + 1
                num4 = status_order.index("put_milk") + 1

                if number == 0:
                    label_time['take'] += end_time - start_time
                    print(type(add_step_button_label1))
                    variable_name = "add_step_button_label{}".format(num1)
                    label_widget = globals()[variable_name]
                    label_widget.configure(text=str(round(label_time['take'], 1)))
                    label_widget.configure(fg_color='green')
                    for i in (num2, num3, num4):
                        variable_name = "add_step_button_label{}".format(i)
                        label_widget = globals()[variable_name]
                        label_widget.configure(fg_color=['#3B8ED0', '#1F6AA5'])
                    count_num1 += 1
                    duration_num1 += 1
                    count_nothing = 0
                elif number == 1:
                    label_time['split'] += end_time - start_time
                    variable_name = "add_step_button_label" + str(num2)
                    label_widget = globals()[variable_name]
                    label_widget.configure(text=str(round(label_time['split'], 1)))
                    label_widget.configure(fg_color='green')
                    for i in (num1, num3, num4):
                        variable_name = "add_step_button_label{}".format(i)
                        label_widget = globals()[variable_name]
                        label_widget.configure(fg_color=['#3B8ED0', '#1F6AA5'])
                    count_num2 += 1
                    count_nothing = 0
                elif number == 2:
                    label_time['put_straw'] += end_time - start_time
                    variable_name = "add_step_button_label" + str(num3)
                    label_widget = globals()[variable_name]
                    label_widget.configure(text=str(round(label_time['put_straw'], 1)))
                    label_widget.configure(fg_color='green')
                    for i in (num1, num2, num4):
                        variable_name = "add_step_button_label{}".format(i)
                        label_widget = globals()[variable_name]
                        label_widget.configure(fg_color=['#3B8ED0', '#1F6AA5'])
                    count_num3 += 1
                    count_nothing = 0

                elif number == 3:
                    label_time['put_milk'] += end_time - start_time
                    variable_name = "add_step_button_label" + str(num4)
                    label_widget = globals()[variable_name]
                    label_widget.configure(text=str(round(label_time['put_milk'], 1)))
                    label_widget.configure(fg_color='green')
                    for i in (num1, num2, num3):
                        variable_name = "add_step_button_label{}".format(i)
                        label_widget = globals()[variable_name]
                        label_widget.configure(fg_color=['#3B8ED0', '#1F6AA5'])
                    count_num4 += 1
                    count_nothing = 0
                else:
                    count_nothing += 1
                    print("not detect")

                if count_num1 == 1:
                    duration_start = last_time

                if status_setting_dictionary['take']['reset_step']:
                    if count_num1 > 3 and count_nothing > 3:
                        counts += 1
                        k = 1
                        for i in ['take', 'split', 'put_straw', 'put_milk']:
                            label_time[i] = 0
                            variable_name = "add_step_button_label" + str(k)
                            label_widget = globals()[variable_name]
                            label_widget.configure(text=str(round(label_time[i], 1)))
                            k += 1
                        duration_time = last_time - duration_start
                        latest_time_button.configure(text=str(round(duration_time, 1)))
                        work_counts_button.configure(text=str(counts))
                        count_num1 = 0
                        count_nothing = 0
                if status_setting_dictionary['split']['reset_step']:
                    print(status_setting_dictionary[f'{status_order[1]}'])
                    if count_num1 > 3 and count_num2 > 3 and count_nothing > 3:
                        counts += 1
                        k = 1
                        for i in ['take', 'split', 'put_straw', 'put_milk']:
                            label_time[i] = 0
                            variable_name = "add_step_button_label" + str(k)
                            label_widget = globals()[variable_name]
                            label_widget.configure(text=str(round(label_time[i], 1)))
                            k += 1
                        duration_time = last_time - duration_start
                        latest_time_button.configure(text=str(round(duration_time, 1)))
                        work_counts_button.configure(text=str(counts))
                        count_num1 = 0
                        count_num2 = 0
                        count_nothing = 0
                if status_setting_dictionary['put_straw']['reset_step']:
                    if count_num1 > 5 and count_num2 > 5 and count_num3 > 5 and count_nothing > 5:
                        counts += 1
                        k = 1
                        for i in ['take', 'split', 'put_straw', 'put_milk']:
                            label_time[i] = 0
                            variable_name = "add_step_button_label" + str(k)
                            label_widget = globals()[variable_name]
                            label_widget.configure(text=str(round(label_time[i], 1)))
                            k += 1
                        duration_time = last_time - duration_start
                        latest_time_button.configure(text=str(round(duration_time, 1)))
                        work_counts_button.configure(text=str(counts))
                        count_num1 = 0
                        count_num2 = 0
                        count_num3 = 0
                        count_nothing = 0
                if status_setting_dictionary['put_milk']['reset_step']:
                    if count_num1 > 5 and count_num2 > 5 and count_num3 > 5 and count_num4 > 5 and count_nothing > 5:
                        counts += 1
                        k = 1
                        for i in ['take', 'split', 'put_straw', 'put_milk']:
                            label_time[i] = 0
                            variable_name = "add_step_button_label" + str(k)
                            label_widget = globals()[variable_name]
                            label_widget.configure(text=str(round(label_time[i], 1)))
                            k += 1


                        duration_time = last_time - duration_start
                        latest_time_button.configure(text=str(round(duration_time, 1)))
                        work_counts_button.configure(text=str(counts))
                        count_num1 = 0
                        count_num2 = 0
                        count_num3 = 0
                        count_num4 = 0
                        count_nothing = 0

                root.update()
                video_frame.update()  # Update the Tkinter window

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) == ord('q'):
                    break
            else:
                # Break the loop if the end of the video is reached
                break
    tabview.tab("結果").update()

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

# =========================================== main loop =============================================
root.mainloop()