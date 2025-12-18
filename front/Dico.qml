import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import '../api/api.js' as API

ColumnLayout {
    anchors.fill: parent
    Layout.fillWidth: true
    Layout.fillHeight: true

    Text {
        text: "Tadiavo ny hevitry ny teny  Malagasy."
        font.family: "Century Gothic"
        font.pixelSize: 14
        color: "#7c7c7c"
        Layout.leftMargin: 20
        Layout.topMargin: 20
        Layout.bottomMargin: 20
    }

    Rectangle {
        Layout.fillWidth: true
        height: 80
        color: "#fff"
        radius: 5
        border.width: 1
        border.color: separatorColor
        Layout.leftMargin: 20
        Layout.rightMargin: 20
        Layout.bottomMargin: 20

        ColumnLayout {
            anchors.fill: parent
            Layout.fillWidth: true
            Layout.fillHeight: true

            Item { Layout.fillHeight: true }
            
            RowLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true

                ComboBox {
                    Layout.leftMargin: 15
                    width: 200
                    model: ["Option 1", "Option 2", "Option 3"]
                    currentIndex: 0
                    onActivated: console.log("Choix:", currentText)
                    visible: false
                }

                TextField {
                    id: search_zn
                    Layout.fillWidth: true
                    Layout.leftMargin: 15
                    placeholderText: "Tadiavo eto ny teny tianao ho fantatra ..."

                    background: Rectangle {
                        implicitHeight: 45
                        border.width: 1
                        border.color: "lightgrey"
                        radius: 3
                    }
                }

                Button {
                    text: "Tadiavo"
                    Layout.rightMargin: 15

                    contentItem: RowLayout {
                        Layout.fillWidth: true
                        spacing: 5

                        Item { Layout.fillWidth: true }

                        Text {
                            Layout.leftMargin: 5
                            font.family: faSolid.name
                            font.pixelSize: 16
                            text: "\uf002"
                            color: activeButtonTextColor
                        }

                        Text {
                            text: "Tadiavo"
                            color: activeButtonTextColor
                            font.pointSize: 9
                        }

                        Item { Layout.fillWidth: true }
                    }

                    background: Rectangle {
                        color: activeButtonColor
                        implicitHeight: 45
                        radius: 3
                    }

                    onClicked: {
                        var search = search_zn.text
                        API.callApi("/dico/" + search, "GET", null, function(response) {
                            if (response !== "erreur" && response.resultats) {
                                // On vide l'ancien contenu
                                search_result.clear()

                                // On ajoute les nouveaux résultats
                                for (var i = 0; i < response.resultats.length; i++) {
                                    var item = response.resultats[i]
                                    search_result.append({
                                        teny: item.teny,
                                        karazana: item.karazana || "",
                                        fanazavana: item.fanazavana || "",
                                        ohatra: item.ohatra || ""
                                    })
                                }

                                //console.log("Résultats trouvés :", search_result.count)
                            } else {
                                //console.log("Aucun résultat trouvé")
                                search_result.clear()
                            }
                        })
                    }

                }
            }

            Item { Layout.fillHeight: true }
        }
    }

    ColumnLayout {
        Layout.fillWidth: true
        Layout.topMargin: 20
        Layout.bottomMargin: 20
        
        RowLayout {
            Text {
                Layout.leftMargin: 20
                font.family: faSolid.name
                font.pixelSize: 18
                text: "\uf002"
                color: "#000"
            }

            Text {
                text: "Ireo vokatrin'ny fikarohana :"
                font.pixelSize: 18
                color: "#7c7c7c"
                Layout.leftMargin: 5
            }

            Item { Layout.fillWidth: true }
        }

        Rectangle {
            id: resultContainer
            color: "#ffffff"
            Layout.fillWidth: true
            Layout.preferredHeight: search_result.count === 0 ? 150 : Math.min(400, searchResultListView.contentHeight)
            border.width: 1
            border.color: separatorColor
            radius: 8

            // Modèle de données
            ListModel { 
                id: search_result 
            }

            // Message amélioré quand la liste est vide - EN DEHORS du ScrollView
            Rectangle {
                id: emptyState
                anchors.fill: parent
                anchors.margins: 20
                color: "#f8f9fa"
                radius: 8
                border.width: 1
                border.color: "#e0e0e0"
                visible: search_result.count === 0

                Column {
                    anchors.centerIn: parent
                    spacing: 10
                    width: Math.min(parent.width - 40, 300)

                    Text {
                        anchors.horizontalCenter: parent.horizontalCenter
                        font.family: faSolid.name
                        font.pixelSize: 32
                        text: "\uf06a"
                        color: "#95a5a6"
                    }

                    Text {
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: "Tsy misy valiny hita"
                        font.pixelSize: 16
                        font.bold: true
                        color: "#7f8c8d"
                    }

                    Text {
                        width: parent.width
                        text: "Avereno jerena ny teny notadiavinao na andramano teny hafa"
                        font.pixelSize: 12
                        color: "#95a5a6"
                        wrapMode: Text.Wrap
                        horizontalAlignment: Text.AlignHCenter
                    }
                }
            }

            ScrollView {
                id: scrollView
                anchors.fill: parent
                anchors.margins: 5
                clip: true
                visible: search_result.count > 0 // Seulement visible quand il y a des résultats

                ScrollBar.vertical.policy: ScrollBar.AsNeeded
                ScrollBar.horizontal.policy: ScrollBar.AsNeeded

                ListView {
                    id: searchResultListView
                    model: search_result
                    spacing: 8
                    boundsBehavior: Flickable.StopAtBounds

                    delegate: Rectangle {
                        width: searchResultListView.width - 10
                        height: contentColumn.height + 20
                        color: index % 2 === 0 ? "#f8f9fa" : "#ffffff"
                        border.color: "#e0e0e0"
                        border.width: 1
                        radius: 6
                        
                        property bool isHovered: false
                        states: State {
                            name: "hovered"
                            when: isHovered
                            PropertyChanges { target: hoverRect; opacity: 0.1 }
                        }

                        Rectangle {
                            id: hoverRect
                            anchors.fill: parent
                            color: "lightgray"
                            opacity: 0
                            radius: 6
                        }

                        Column {
                            id: contentColumn
                            anchors {
                                left: parent.left
                                right: parent.right
                                top: parent.top
                                margins: 10
                            }
                            spacing: 5

                            Text {
                                text: "Teny : " + teny
                                font.bold: true
                                font.pixelSize: 14
                                color: "#1a5fb4"
                                width: parent.width
                                wrapMode: Text.Wrap
                            }

                            Text {
                                text: "Karazana : " + karazana
                                font.pixelSize: 12
                                color: "#26a269"
                                width: parent.width
                                wrapMode: Text.Wrap
                            }

                            Text {
                                text: "Fanazavana : " + fanazavana
                                font.pixelSize: 12
                                color: "#2c2c2c"
                                width: parent.width
                                wrapMode: Text.Wrap
                                lineHeight: 1.2
                            }

                            Text {
                                text: "Ohatra : " + ohatra
                                font.pixelSize: 12
                                color: "#5e5c64"
                                width: parent.width
                                wrapMode: Text.Wrap
                                lineHeight: 1.2
                            }
                        }

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: parent.isHovered = true
                            onExited: parent.isHovered = false
                        }
                    }
                }
            }
        }

        Item { Layout.fillHeight: true }
    }

    Item { Layout.fillHeight: true }
}
