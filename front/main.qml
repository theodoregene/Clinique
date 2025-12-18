import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Window {
    width: 1336
    height: 768
    visible: true
    title: "Application TSIPeLINA"

    // Component.onCompleted: {
    //     mainWindow.setIcon("qrc:/font/img/TSIPeLINA.png")
    // }

    // Propriété pour suivre la page active
    property int currentPage: 0

    // Configuration des couleurs
    property color asideBackground: "#ffffff"
    property color separatorColor: "#EDEDED"
    property color activeButtonColor: "#3B506B"
    property color inactiveButtonColor: "#D0FAE4"
    property color buttonTextColor: "#05976A"
    property color activeButtonTextColor: "#ffffff"
    property color pageColor: "#F9FAFC"

    FontLoader {
        id: faSolid
        source: "fonts/Font Awesome 6 Free-Solid-900.otf"
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        
        // Séparateur vertical
        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: 1
            color: separatorColor
        }

        // Content - Partie droite
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            // Header
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                color: "#fff"
                
                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 30
                    anchors.rightMargin: 30

                    Text {
                        Layout.leftMargin: 20
                        font.family: faSolid.name
                        font.pixelSize: 28
                        text: {
                            switch(currentPage) {
                                case 0: return "\uf058"
                                case 1: return "\uf19d"
                                case 2: return "\uf518"
                                default: return ""
                            }
                        }
                        color: activeButtonColor
                    }
                    
                    Text {
                        text: {
                            switch(currentPage) {
                                case 0: return "Fanoratana (Editeur de Texte)"
                                case 1: return "Fianarana teny Malagasy"
                                case 2: return "Rakibolana Malagasy"
                                default: return ""
                            }
                        }
                        color: activeButtonColor
                        font.bold: false
                        font.pixelSize: 28
                    }

                    Item { Layout.fillWidth: true }

                    Button {
                        id: rakibolana
                        text: "Rakibolana"

                        onClicked: stackLayout.currentIndex = 1

                        contentItem: RowLayout {
                            Layout.fillWidth: true
                            spacing: 5

                            Text {
                                text: "Rakibolana"
                                color: "#fff"
                                font.pointSize: 9
                            }

                            Item { Layout.fillWidth: true }
                        }

                        background: Rectangle {
                            color: "#3B506B"
                            implicitHeight: 40
                            radius: 5
                            border {
                                width: 1
                                color: parent.pressed ? "#B2B4BA" : "#D1D4DB"
                            }
                        }
                    }
                }
            }

            // Séparateur horizontal
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: separatorColor
            }

            // Contenu des pages
            StackLayout {
                id: stackLayout
                Layout.fillWidth: true
                Layout.fillHeight: true
                currentIndex: currentPage

                // Page 1
                Rectangle {
                    color: pageColor

                    Prompt { } // Contenu page Fanabeazana
                }

                // Page 3
                Rectangle {
                    color: pageColor
                    
                    Dico { } // Contenu Rakibolana
                }
            }
        }
    }
}
