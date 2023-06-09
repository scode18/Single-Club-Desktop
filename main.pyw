from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

import os
import sys

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Одиночный Клуб")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'browser.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Version 2023.2.10 Няшный френд"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setStyleSheet("background-color: rgb(100, 133, 202);")

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('images', 'arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(QIcon(os.path.join('images', 'cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        file_menu = self.menuBar().addMenu("&File")

        new_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(os.path.join('images', 'disk--arrow.png')), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save Page As...", self)
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "About", self)
        about_action.setStatusTip("Find out more about Одиночный Клуб")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'lifebuoy.png')),
                                            "Одиночный Клуб", self)
        navigate_mozarella_action.setStatusTip("Go to Одиночный Клуб Homepage")
        navigate_mozarella_action.triggered.connect(self.navigate_mozarella)
        help_menu.addAction(navigate_mozarella_action)

        web_menu = self.menuBar().addMenu("&Web")

        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'youtube.png')),
                                            "My YouTube channel", self)
        navigate_mozarella_action.setStatusTip("Go to my YouTube channel")
        navigate_mozarella_action.triggered.connect(self.navigate_youtube)
        web_menu.addAction(navigate_mozarella_action)

        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'telegram.png')),
                                            "Моя группа в телеграм", self)
        navigate_mozarella_action.setStatusTip("Go to Telegram")
        navigate_mozarella_action.triggered.connect(self.navigate_telegram)
        web_menu.addAction(navigate_mozarella_action)

        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'vk.png')),
                                            "Моя группа в VK", self)
        navigate_mozarella_action.setStatusTip("Go to VK")
        navigate_mozarella_action.triggered.connect(self.navigate_vk)
        web_menu.addAction(navigate_mozarella_action)
        
        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'vk.png')),
                                            "Мой аккаунт в VK", self)
        navigate_mozarella_action.setStatusTip("Go to VK")
        navigate_mozarella_action.triggered.connect(self.navigate_vk_akk)
        web_menu.addAction(navigate_mozarella_action)

        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'github.png')),
                                            "Мой аккаунт в GitHub", self)
        navigate_mozarella_action.setStatusTip("Go to GitHub")
        navigate_mozarella_action.triggered.connect(self.navigate_github)
        web_menu.addAction(navigate_mozarella_action)
        
        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'boosty.png')),
                                            "My Boosty", self)
        navigate_mozarella_action.setStatusTip("Go to Boosty")
        navigate_mozarella_action.triggered.connect(self.navigate_boosty)
        web_menu.addAction(navigate_mozarella_action)
        
        donate_menu = self.menuBar().addMenu("&Donate")
        
        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'boosty.png')),
                                            "My Boosty", self)
        navigate_mozarella_action.setStatusTip("Go to Boosty")
        navigate_mozarella_action.triggered.connect(self.navigate_boosty)
        donate_menu.addAction(navigate_mozarella_action)

        self.add_new_tab(QUrl('https://scode18.github.io/Punk-Rock/'), 'Одиночный Клуб')

        self.show()

        self.setWindowTitle("Одиночный Клуб")
        self.setWindowIcon(QIcon(os.path.join('images', 'browser.png')))

    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl('')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - Одиночный Клуб" % title)

    def navigate_mozarella(self):
        self.tabs.currentWidget().setUrl(QUrl("https://scode18.github.io/Punk-Rock/"))

    def navigate_youtube(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.youtube.com/channel/UCtuZN__5yDphNTwetxlJ7Ig"))

    def navigate_vk(self):
        self.tabs.currentWidget().setUrl(QUrl("https://vk.com/pankrocksingleclub"))
        
    def navigate_vk_akk(self):
        self.tabs.currentWidget().setUrl(QUrl("https://vk.com/hackersolomon"))

    def navigate_telegram(self):
        self.tabs.currentWidget().setUrl(QUrl("https://t.me/scandsk"))

    def navigate_github(self):
        self.tabs.currentWidget().setUrl(QUrl("https://github.com/scode18"))
        
    def navigate_boosty(self):
        self.tabs.currentWidget().setUrl(QUrl("https://boosty.to/singleclub"))

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "All files (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)")

        if filename:
            html = self.tabs.currentWidget().page().toHtml()
            with open(filename, 'w') as f:
                f.write(html.encode('utf8'))

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://scode18.github.io/Punk-Rock/"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            return

        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))

        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("Одиночный Клуб")
app.setOrganizationDomain("https://scode18.github.io/Punk-Rock")

window = MainWindow()

app.exec_()
