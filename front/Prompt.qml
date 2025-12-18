import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import '../api/api.js' as API

ColumnLayout {
    anchors.fill: parent
    Layout.fillWidth: true
    Layout.fillHeight: true
    spacing: 10
    Layout.margins: 20

    Text {
        text: "Hadiovy amin'ny IA mba hanitsiana ny teny soratra Malagasy."
        font.family: "Century Gothic"
        font.pixelSize: 14
        color: "#7c7c7c"
        Layout.leftMargin: 20
        Layout.topMargin: 20
    }

    RowLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true

        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true

            Rectangle {
                Layout.fillWidth: true
                height: 450
                border.width: 1
                border.color: separatorColor
                color: "#fff"
                radius: 5
                Layout.leftMargin: 20

                Column {
                    width: parent.width
                    height: parent.height

                    // Section haute
                    Rectangle {
                        width: parent.width
                        height: 60
                        color: "transparent"
                        border.color: "#dbdbdb"
                        border.width: 0

                        Column {
                            anchors.fill: parent
                            padding: 10

                            Text {
                                text: "Ampidiro ny lahatsoratra"
                                font.family: "Century Gothic"
                                font.weight: Font.Light
                            }

                            Text {
                                text: "Soraty eto ny lahatsoratra"
                                font.family: "Century Gothic"
                                font.pixelSize: 14
                                color: "#7c7c7c"
                            }
                        }
                    }

                    // Section milieu
                    Rectangle {
                        width: parent.width
                        height: 400
                        color: "transparent"
                        border.color: "#dbdbdb"
                        border.width: 0

                        TextArea {
                            id: text_zn
                            anchors.fill: parent
                            anchors.margins: 10
                            wrapMode: TextEdit.Wrap
                            font.pixelSize: 18

                            background: Rectangle {
                                border.width: 1
                                border.color: "lightgrey"
                                radius: 3
                            }
                        }
                    }

                    // Section basse
                    Rectangle {
                        width: parent.width
                        height: 50
                        color: "transparent"

                        RowLayout {
                            anchors.verticalCenter: parent.verticalCenter
                            spacing: 5

                            Button {
                                Layout.leftMargin: 8

                                onClicked: {
                                    //res_zn.text = text_zn.text
                                    var text_input = text_zn.text
                                    API.callApi("/corriger", "POST", {texte: text_input}, function(response) {
                                        if (response !== "erreur") {
                                            text_zn.text = response.corrige
                                            fault_count.text = response.nombre_fautes
                                            fault_count.text = fault_count.text + " no diso hita"
                                        } else {
                                            text_zn.text = "Erreur de chargement"
                                        }
                                    })
                                }

                                contentItem: RowLayout {
                                    Layout.fillWidth: true
                                    spacing: 5

                                    Text {
                                        font.family: faSolid.name
                                        font.pixelSize: 14
                                        text: "\uf058"
                                        color: "#000"
                                    }

                                    Text {
                                        text: "Hadiovy"
                                        color: "#000"
                                        font.pointSize: 9
                                    }

                                    Item { Layout.fillWidth: true }
                                }

                                background: Rectangle {
                                    color: "#D1D4DB"
                                    implicitHeight: 40
                                    radius: 5
                                    border {
                                        width: 1
                                        color: parent.pressed ? "#B2B4BA" : "#D1D4DB"
                                    }
                                }
                            }

                            Button {
                                Layout.leftMargin: 5
                                contentItem: RowLayout {
                                    Layout.fillWidth: true
                                    spacing: 5

                                    Text {
                                        font.family: faSolid.name
                                        font.pixelSize: 14
                                        text: "\uf2ea"
                                        color: "#000"
                                    }

                                    Text {
                                        text: "Avereno"
                                        color: "#000"
                                        font.pointSize: 9
                                    }
                                    Item { Layout.fillWidth: true }
                                }

                                background: Rectangle {
                                    color: parent.pressed ? "#E6E6E6" : "#fff"
                                    implicitHeight: 40
                                    radius: 5
                                    border {
                                        width: 1
                                        color: "grey"
                                    }
                                }

                                onClicked: {
                                    text_zn.text = ""
                                    fault_count.text = "0 no diso hita"
                                }
                            }
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: 150
                        color: "transparent"
                        border.color: "#fff"
                        border.width: 0

                    }
                }
            }

            Item { Layout.fillHeight: true }
        }

        ColumnLayout {
            Layout.fillHeight: true
            Layout.rightMargin: 20

            Rectangle {
                border.width: 1
                border.color: separatorColor
                color: "#fff"
                width: 300
                height: 200
                radius: 5

                Column {
                    width: parent.width
                    height: parent.height

                    Rectangle {
                        width: parent.width
                        height: 60
                        color: "transparent"
                        // border.color: "#dbdbdb"

                        Column {
                            anchors.fill: parent
                            padding: 10

                            Text {
                                text: "Vokatra"
                                font.family: "Century Gothic"
                                font.weight: Font.Light
                            }

                            Text {
                                id: fault_count
                                text: "0 ny diso hita"
                                font.family: "Century Gothic"
                                font.pixelSize: 14
                                color: "#7c7c7c"
                            }
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: 155
                        color: "transparent"

                        Column {
                            anchors.centerIn: parent
                            spacing: 10

                            Text {
                                text: "💡"
                                font.pixelSize: 30
                                color: "#7c7c7c"
                                anchors.horizontalCenter: parent.horizontalCenter
                            }

                            Text {
                                text: "Tsindrio \"Hadiovy\" mba hanomboka"
                                font.family: "Century Gothic"
                                font.pixelSize: 14
                                color: "#7c7c7c"
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }
                    }
                }
            }

            Item { Layout.fillHeight: true }
        }
    }

    Item { Layout.fillHeight: true }
}