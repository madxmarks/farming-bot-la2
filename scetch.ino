#include <Keyboard.h>

String input = "";

void setup() {
  Serial.begin(9600);
  Keyboard.begin();
}

void loop() {
  while (Serial.available()) {
    char ch = Serial.read();
    if (ch == '\n') {
      handleCommand(input);
      input = "";
    } else {
      input += ch;
    }
  }
}

void handleCommand(String cmd) {
  cmd.trim();
  cmd.toUpperCase();
  if (cmd == "F1") pressKey(KEY_F1);
  else if (cmd == "F2") pressKey(KEY_F2);
  else if (cmd == "F3") pressKey(KEY_F3);
  else if (cmd == "F4") pressKey(KEY_F4);
  else if (cmd == "F5") pressKey(KEY_F5);
  else if (cmd == "F6") pressKey(KEY_F6);
  else if (cmd == "F7") pressKey(KEY_F7);
  else if (cmd == "F8") pressKey(KEY_F8);
  else if (cmd == "F9") pressKey(KEY_F9);
  else if (cmd == "F10") pressKey(KEY_F10);
  else if (cmd == "F11") pressKey(KEY_F11);
  else if (cmd == "F12") pressKey(KEY_F12);
  else if (cmd == "ENTER") pressKey(KEY_RETURN);
  else if (cmd == "ESC") pressKey(KEY_ESC);
  else if (cmd == "TAB") pressKey(KEY_TAB);
  else if (cmd.length() == 1) {
    char c = cmd.charAt(0);
    if (isAscii(c)) {
      pressKey(c);
    }
  }
}

void pressKey(uint8_t keycode) {
  Keyboard.press(keycode);
  delay(100);
  Keyboard.release(keycode);
}