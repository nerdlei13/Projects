import keyboard
log_file = "test_keystrokes.log"

def on_key_press(event):
    with open(log_file, "a") as f:
        f.write(event.name)

keyboard.on_press(on_key_press)

keyboard.wait