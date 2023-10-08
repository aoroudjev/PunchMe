import punch_handler
import driver_handler
import customtkinter as ctk

from selenium.common import WebDriverException

from threading import Thread

credentials = {}
driver_handler.download_driver('117.0.5938.149')


def update_status(color, text):
    status_label.configure(text_color=color.upper(), text=text.upper())


def update_entry_state(state):
    username_entry.configure(state=state)
    password_entry.configure(state=state)
    hour_combobox.configure(state=state)
    minute_combobox.configure(state=state)
    start_button.configure(state=state)
    sequence_combobox.configure(state=state)


def start_punch_thread():
    global credentials
    credentials = {
        'Username': username_entry.get(),
        'Password': password_entry.get(),
    }

    match sequence_combobox.get():
        case 'Full Day':
            Thread(target=full_day_seq).start()
        case 'Lunch Only':
            Thread(target=lunch_seq).start()
        case 'Out Only':
            Thread(target=out_seq).start()


def check_login(driver):
    update_status('YELLOW', 'CHECKING LOGIN INFO')
    punch_handler.login(driver, credentials)
    if driver.title != 'Quick Punch':
        update_status('RED', 'BAD LOGIN')
        raise WebDriverException


def full_day_seq():
    hour = hour_combobox.get()
    minute = minute_combobox.get()
    update_entry_state('disabled')
    update_status('YELLOW', 'STARTING DRIVER')
    driver = punch_handler.start_driver()
    check_login(driver)
    update_status('YELLOW', 'STARTING DAY PUNCH...')
    punch_handler.login(driver, credentials)
    update_status('YELLOW', f'WAITING UNTIL {hour}:{minute}')
    punch_handler.sleep_until(hour, minute)
    update_entry_state('normal')


def out_seq():
    update_entry_state('disabled')
    update_status('YELLOW', 'STARTING DRIVER')
    driver = punch_handler.start_driver()
    update_entry_state('normal')


def lunch_seq():
    update_entry_state('disabled')
    update_status('YELLOW', 'STARTING DRIVER')
    driver = punch_handler.start_driver()
    update_entry_state('normal')


root = ctk.CTk()
root.title('PunchMe')

# GUI elements
username_label = ctk.CTkLabel(root, text="Username:")
username_label.grid(column=0, row=0, sticky=ctk.W)
username_entry = ctk.CTkEntry(root)
username_entry.grid(column=1, row=0)

password_label = ctk.CTkLabel(root, text="Password:")
password_label.grid(column=0, row=1, sticky=ctk.W)
password_entry = ctk.CTkEntry(root, show="*")  # Password is hidden
password_entry.grid(column=1, row=1)

time_label = ctk.CTkLabel(root, text="Time(24):")
time_label.grid(column=0, row=2, sticky=ctk.W)
hour_combobox = ctk.CTkComboBox(root, values=[str(i).zfill(2) for i in range(8, 19)], width=60)
hour_combobox.set('12')
hour_combobox.grid(column=1, row=2, sticky=ctk.W)
ctk.CTkLabel(root, text=":", anchor=ctk.CENTER).grid(column=1, row=2)
minute_combobox = ctk.CTkComboBox(root, values=["00", "30"], width=60)
minute_combobox.grid(column=1, row=2, sticky=ctk.E)

sequence_combobox = ctk.CTkComboBox(root, values=['Full Day', 'Lunch Only', 'Out Only'])
sequence_combobox.set('Lunch Only')
sequence_combobox.grid(column=1, row=3)

start_button = ctk.CTkButton(root, text='START', command=start_punch_thread, width=50)
start_button.grid(column=0, row=3)

status_label = ctk.CTkLabel(root, text_color='GREEN', text='READY')
status_label.grid(column=0, row=4, columnspan=2)

root.mainloop()
