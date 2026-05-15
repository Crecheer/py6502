from PyQt6.QtWidgets import QApplication, QFileDialog, QLabel, QMessageBox, QWidget, QGridLayout, QPushButton, QTextBrowser, QLayout, QLineEdit
from PyQt6.QtGui import QIcon
import sys
import memory
import processor

app = QApplication(sys.argv)
program = None
file = None

window = QWidget(windowTitle="py6502")
# add icon later
# window.setWindowIcon(QIcon())

mem = memory.Memory()
pc = ""


def exec():
    global mem
    global pc
    cpu = processor.Processor(mem)
    cpu.reset()
    if pc is "":
        pc = 0xFCE2
    elif pc.startswith("0x"):
        cpu.pc = int(pc, base=16)
    else:
        cpu.pc = int("0x"+pc, base=16)

    if file is None:
        status.setText("Please load a program first.")
        return

    with open(file) as f:
        for l in f:
            # first in line is usually <address>:, for example 0600:
            line = l.split()
            address = 0x0000
            count = 0x0000
            for b in line:
                if b.endswith(":"):
                    address = int(b[:-1], 16)
                else:
                    ins = int(b, 16)
                    loc = address + count
                    mem[loc] = ins
                    count += 1

    cpu.execute_until_stop(status)


def showFileDialog():
    global file
    file, ok = QFileDialog.getOpenFileName(window, "Open Image")
    filename.setText(file)
    print(ok)


def startPosChange():
    global pc
    pc = start_pos.text()
    print(pc)


layout = QGridLayout()
window.setLayout(layout)

status = QLabel()
filename = QLabel()

exec_button = QPushButton("Run")
exec_button.clicked.connect(exec)

load_button = QPushButton("Load")
load_button.clicked.connect(showFileDialog)

start_pos = QLineEdit(
    placeholderText="FCE2",
    clearButtonEnabled=True
)
start_pos.textChanged.connect(startPosChange)


layout.addWidget(status, 0, 0, 4, 1)
layout.addWidget(exec_button, 0, 1)
layout.addWidget(filename, 1, 1)
layout.addWidget(load_button, 0, 2)
layout.addWidget(start_pos, 1, 2, 4, 1)


window.show()

app.exec()
