import sys

import classes.home
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    st = classes.home.Home()
    st.show()
    sys.exit(app.exec())
