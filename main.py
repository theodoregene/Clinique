import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QIcon

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.load(QUrl("front/main.qml"))
    # Récupérer la fenêtre principale
    window = engine.rootObjects()[0]

    # Définir l'icône
    window.setIcon(QIcon('front/img/TSIPeLINA.ico'))
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
