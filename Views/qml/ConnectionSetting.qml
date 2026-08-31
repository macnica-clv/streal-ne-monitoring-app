import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Effects
import QtQuick.Controls.Material




Rectangle {
    id: connectionSetting
    width: parent ? parent.width : 0
    height: parent ? parent.height : 0
    property var _appBridge2: (typeof(appBridge2) !== "undefined" && appBridge2 !== null)
                          ? appBridge2
                          : null

    property int themeIndex: _appBridge2 ? _appBridge2.theme : 0


    Material.accent: Material.Indigo

    property var colors: ["#FFFFFF", "#FFFFFF", "#2A2D35"]
    property var text_colors: ["#343A3F", "#343A3F", "#FFFFFF"]
    property var sources: ["Icon_ConnectionSetting.png", "Icon_ConnectionSetting.png", "Icon_ConnectionSetting_white.png"]
    property var colors2: ["#F2F4F8", "#F2F4F8", "#393D47"]
    property var combo_colors: ["#FFFFFF", "#FFFFFF", "#525563"]
    property var combo_border: ["#cccccc", "#cccccc", "#343640"]
    property var shadow: ["#EAECF5", "#DDE1E6", "#15171A"]
    color: shadow[themeIndex]

    Rectangle{
        width: parent.width - 5
        height: parent.height - 5
        color: colors[themeIndex]

        layer.enabled: true
        layer.effect: MultiEffect {
            shadowEnabled: true
            shadowBlur: 0.5
            shadowColor: "#45486E"
            shadowOpacity: 0.5
            shadowHorizontalOffset: 4
            shadowVerticalOffset: 4
        }

        Image {
            id: image
            x: 9
            y: 13
            width: 36
            height: 34
            source: sources[themeIndex]
            fillMode: Image.PreserveAspectFit
        }

        Text {
            id: text4
            x: 45
            y: 19
            text: qsTr("Connection Settings")
            color: text_colors[themeIndex]
            font.pixelSize: 16
            font.family:"Roboto"
        }

        Rectangle {
            id: separator
            x: 13
            y: 47
            width: 470
            height: 1
            color: "gray"
        }

        Text {
            id: text5
            x: 18
            y: 55
            text: qsTr("Connection Method")
            color:text_colors[themeIndex]
            font.pixelSize: 16
            font.family:"Roboto"
        }

        RadioButton {
            id: radioButtonUsb
            checked: typeof(bridge) !== "undefined" ? bridge.method == 0 : true
            x: 24
            y: 70
            text: qsTr("USB")
            font.pixelSize: 16
            font.family:"Roboto"

            spacing: 8

            indicator: Rectangle {
                implicitWidth: 18
                implicitHeight: 18
                radius: 8
                border.width: 2

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter

                border.color: text_colors[themeIndex]
                color: "transparent"

                Rectangle {
                    anchors.centerIn: parent
                    width: 10
                    height: 10
                    radius: 4
                    visible: radioButtonUsb.checked
                    color: "#0F62FE"   // 中点色
                }
            }


            contentItem: Label {
                text: radioButtonUsb.text
                font: radioButtonUsb.font
                verticalAlignment: Text.AlignVCenter
                leftPadding: radioButtonUsb.indicator ? radioButtonUsb.indicator.width + radioButtonUsb.spacing : 0

                color: text_colors[themeIndex]
            }


            onClicked: bridge.set_method(0)
        }

        RadioButton {
            id: radioButtonLan
            checked: typeof(bridge) !== "undefined" ? bridge.method == 1 : false
            x: 102
            y: 70
            text: qsTr("LAN")
            font.pixelSize: 16
            font.family:"Roboto"

            spacing: 8

            indicator: Rectangle {
                implicitWidth: 18
                implicitHeight: 18
                radius: 8
                border.width: 2

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter

                border.color: text_colors[themeIndex]
                color: "transparent"

                Rectangle {
                    anchors.centerIn: parent
                    width: 10
                    height: 10
                    radius: 4
                    visible: radioButtonLan.checked
                    color: "#0F62FE"   // 中点色
                }
            }

            contentItem: Label {
                text: radioButtonLan.text
                font: radioButtonLan.font
                verticalAlignment: Text.AlignVCenter
                leftPadding: radioButtonLan.indicator ? radioButtonLan.indicator.width + radioButtonLan.spacing : 0

                color: text_colors[themeIndex]
            }
            onClicked: bridge.set_method(1)
        }


        Button {
            id: connectButton
            x: 118
            y: 330
            width: 120
            text: qsTr("Connect")
            font.pixelSize: 16
            font.family: "Roboto"

            // ボタンのラベル部分
            contentItem: Label {
                text: parent.text
                color: "#FFFFFF" // テーマに従う文字色
                font: parent.font
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            // 背景＋押下オーバーレイ
            background: Rectangle {
                color: parent.pressed ? "#0043CE"
                     : parent.hovered ? "#4589FF"
                     : "#0F62FE"
                radius: 0
            }

            onClicked: bridge.connect_proc()
        }

        Button {
            id: disconnectButton
            x: 258
            y: 330
            width: 120
            text: qsTr("Disconnect")
            font.pixelSize: 16
            font.family: "Roboto"

            // ボタンのラベル部分
            contentItem: Label {
                text: parent.text
                color: "#FFFFFF" // テーマに従う文字色
                font: parent.font
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            // 背景＋押下オーバーレイ
            background: Rectangle {
                color: parent.pressed ? "#525563"
                     : parent.hovered ? "#697077"
                     : "#525563"
                radius: 0
            }

            onClicked: bridge.disconnect_proc()
        }


        Text {
            id: selectComPortLabel
            x: 18
            y: 125
            text: qsTr("Device Setting")
            color: text_colors[themeIndex]
            font.pixelSize: 16
            font.family: "Roboto"
        }

        Rectangle{
            id: device1Setting
            x: 13
            y: 150
            width: 470
            height: 170
            color: colors2[themeIndex]
        }

        Text {
            id: device1Label
            x: 18
            y: 152
            text: qsTr("Device 1")
            color:text_colors[themeIndex]
            font.pixelSize: 15
            font.family: "Roboto"
        }

       Text {
            id: com
            x: 18
            y: 175
            text: qsTr("COM Port: ")
            font.pixelSize: 14
            font.family: "Roboto"
            color: "#A2A9B0"
       }

        ComboBox {
            id: device1Combo
            x: 18
            y: 195
            height: 30
            width: 150
            model: typeof(bridge) !== "undefined" ? bridge.com_lists[0] : ["-"]
            currentIndex: typeof(bridge) !== "undefined" ? bridge.com_indexes[0] : 0
            font.pixelSize: 14
            font.family: "Roboto"

            contentItem: Text {
                text: device1Combo.displayText
                font: device1Combo.font
                color: text_colors[themeIndex]
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
                leftPadding: 8
                rightPadding: device1Combo.indicator.width + 8
            }

            background: Rectangle {
                color: combo_colors[themeIndex]
                border.color: combo_border[themeIndex]
                radius: 4
            }


            indicator: Canvas {
                id: arrow
                width: 12; height: 8
                x: device1Combo.width - width - 8
                y: (device1Combo.height - height) / 2
                contextType: "2d"

                onPaint: {
                    var ctx = getContext("2d")
                    ctx.clearRect(0, 0, width, height)
                    ctx.fillStyle = text_colors[themeIndex]
                    ctx.beginPath()
                    ctx.moveTo(0, 0)
                    ctx.lineTo(width, 0)
                    ctx.lineTo(width/2, height)
                    ctx.closePath()
                    ctx.fill()
                }


                Connections {
                    target: _appBridge2
                    function onThemeChanged() { arrow.requestPaint() }
                }

                Component.onCompleted: arrow.requestPaint()
            }


           delegate: ItemDelegate {
                width: device1Combo.width
                text: modelData
                font: device1Combo.font
                highlighted: device1Combo.highlightedIndex === index

                contentItem: Text {
                    text: modelData
                    font: device1Combo.font
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                    color: text_colors[themeIndex]
                }

           }

           popup: Popup {
               y: device1Combo.height
               width: device1Combo.width
               padding: 0

               contentItem: ListView {
                   clip: true
                   implicitHeight: contentHeight
                   model: device1Combo.popup.visible ? device1Combo.delegateModel : null
                   currentIndex: device1Combo.highlightedIndex
               }

               background: Rectangle {
                   radius: 1
                   color: combo_colors[themeIndex]
               }
           }

           onCurrentIndexChanged:{
                if(typeof bridge !== "undefined"){
                    bridge.set_com_port(0, currentIndex)
                }
           }
        }

        Text {
            id: address
            x: 230
            y: 175
            text: qsTr("IP address")
            font.pixelSize: 16
            font.family:"Roboto"
            color: "#A2A9B0"
        }

        Rectangle {
            id: ipAddressInput
            x: 230
            y: 195
            width:240
            height:30
            color: combo_colors[themeIndex]
            radius: 4
            border.width: 1

            property bool hasFocus: field1_1.activeFocus || field1_2.activeFocus || field1_3.activeFocus || field1_4.activeFocus

            border.color: hasFocus ? "#4CC2FF" : combo_border[themeIndex]

            // IPアドレスの各フィールドを格納するプロパティ
            property var fields: [field1_1, field1_2, field1_3, field1_4]

            Row {
                anchors.fill: parent
                anchors.margins: 2
                anchors.centerIn: parent
                spacing: 0

                // --- 1つ目 ---
                Item { width: 60; height: parent.height +3
                    TextField {
                        id: field1_1
                        text: typeof(bridge) !== "undefined" ? bridge.ip_ports[0][0] : 0
                        anchors.fill: parent
                        font.pixelSize: 12
                        font.family:"Roboto"
                        background: null
                        padding: 0
                        horizontalAlignment: Text.AlignRight
                        maximumLength: 3
                        inputMethodHints: Qt.ImhDigitsOnly
                        validator: IntValidator { bottom:0; top:255 }

                        color: text_colors[themeIndex]

                        onTextChanged: {
                            if(text.length === 3) field1_2.forceActiveFocus()
                            if (typeof(bridge) !== "undefined") bridge.set_ip_port(0, 0, text)
                        }
                    }
                    Text { text: "."; font.pixelSize: 16; anchors.verticalCenter: parent.verticalCenter; anchors.right: parent.right; anchors.rightMargin: -2;
                           color: text_colors[themeIndex]}
                }

                // --- 2つ目 ---
                Item { width: 60; height: parent.height +3
                    TextField {
                        id: field1_2
                        text: typeof(bridge) !== "undefined" ? bridge.ip_ports[0][1] : 0
                        anchors.fill: parent
                        font.pixelSize: 12
                        font.family:"Roboto"
                        background: null
                        padding: 0
                        horizontalAlignment: Text.AlignRight
                        maximumLength: 3
                        inputMethodHints: Qt.ImhDigitsOnly
                        validator: IntValidator { bottom:0; top:255 }

                        color: text_colors[themeIndex]

                        onTextChanged: {
                            if (text.length === 3) field1_3.forceActiveFocus()
                            if (typeof(bridge) !== "undefined") bridge.set_ip_port(0, 1, text)
                        }
                    }
                    Text { text: "."; font.pixelSize: 16; anchors.verticalCenter: parent.verticalCenter; anchors.right: parent.right; anchors.rightMargin: -2;
                           color: text_colors[themeIndex]}
                }

                // --- 3つ目 ---
                Item { width: 60; height: parent.height +3
                    TextField {
                        id: field1_3
                        text: typeof(bridge) !== "undefined" ? bridge.ip_ports[0][2] : 0
                        anchors.fill: parent
                        font.pixelSize: 12
                        font.family:"Roboto"
                        background: null
                        padding: 0
                        horizontalAlignment: Text.AlignRight
                        maximumLength: 3
                        inputMethodHints: Qt.ImhDigitsOnly
                        validator: IntValidator { bottom:0; top:255 }

                        color: text_colors[themeIndex]

                        onTextChanged: {
                            if (text.length === 3) field1_4.forceActiveFocus()
                            if (typeof(bridge) !== "undefined") bridge.set_ip_port(0, 2, text)
                        }
                    }
                    Text { text: "."; font.pixelSize: 16; anchors.verticalCenter: parent.verticalCenter; anchors.right: parent.right; anchors.rightMargin: -2;
                           color: text_colors[themeIndex]}
                }

                // --- 4つ目 ---
                TextField {
                    id: field1_4
                    text: typeof(bridge) !== "undefined" ? bridge.ip_ports[0][3] : 0
                    width: 60
                    height: parent.height +3
                    font.pixelSize: 12
                    font.family:"Roboto"
                    background: null
                    padding: 0
                    horizontalAlignment: Text.AlignRight
                    maximumLength: 3
                    inputMethodHints: Qt.ImhDigitsOnly
                    validator: IntValidator { bottom:0; top:255 }

                    color: text_colors[themeIndex]

                    onTextChanged: {
                        if (typeof(bridge) !== "undefined") bridge.set_ip_port(0, 3, text)
                    }
                }
            }

            function getAddress() {
                return [field1_1.text || "0", field1_2.text || "0", field1_3.text || "0", field1_4.text || "0"].join(".")
            }
        }

        Text {
            id: device2Label
            x: 18
            y: 237
            text: qsTr("Device 2")
            color: text_colors[themeIndex]
            font.pixelSize: 15
            font.family: "Roboto"
        }

       Text {
            id: com2
            x: 18
            y: 260
            text: qsTr("COM Port: ")
            font.pixelSize: 14
            font.family: "Roboto"
            color: "#A2A9B0"
       }

        ComboBox {
            id: device2Combo
            x: 18
            y: 280
            height: 30
            width: 150
            model: typeof(bridge) !== "undefined" ? bridge.com_lists[1] : ["-"]
            currentIndex: typeof(bridge) !== "undefined" ? bridge.com_indexes[1] : 0
            font.pixelSize: 14
            font.family: "Roboto"

            contentItem: Text {
                text: device2Combo.displayText
                font: device2Combo.font
                color: text_colors[themeIndex]
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
                leftPadding: 8
                rightPadding: device2Combo.indicator.width + 8
            }

            background: Rectangle {
                color: combo_colors[themeIndex]
                border.color: combo_border[themeIndex]
                radius: 4
            }


            indicator: Canvas {
                id: arrow2
                width: 12; height: 8
                x: device2Combo.width - width - 8
                y: (device2Combo.height - height) / 2
                contextType: "2d"

                onPaint: {
                    var ctx = getContext("2d")
                    ctx.clearRect(0, 0, width, height)
                    ctx.fillStyle = text_colors[themeIndex]
                    ctx.beginPath()
                    ctx.moveTo(0, 0)
                    ctx.lineTo(width, 0)
                    ctx.lineTo(width/2, height)
                    ctx.closePath()
                    ctx.fill()
                }


                Connections {
                    target: _appBridge2
                    function onThemeChanged() { arrow2.requestPaint() }
                }

                Component.onCompleted: arrow2.requestPaint()
            }


           delegate: ItemDelegate {
                width: device1Combo.width
                text: modelData
                font: device2Combo.font
                highlighted: device2Combo.highlightedIndex === index

                contentItem: Text {
                    text: modelData
                    font: device1Combo.font
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                    color: text_colors[themeIndex]
                }

           }

           popup: Popup {
               y: device2Combo.height
               width: device2Combo.width
               padding: 0

               contentItem: ListView {
                   clip: true
                   implicitHeight: contentHeight
                   model: device2Combo.popup.visible ? device2Combo.delegateModel : null
                   currentIndex: device2Combo.highlightedIndex
               }

               background: Rectangle {
                   radius: 1
                   color: combo_colors[themeIndex]
               }
           }
            onCurrentIndexChanged:{
                if(typeof bridge !== "undefined"){
                    bridge.set_com_port(1, currentIndex)
                }
            }
        }

        Text {
            id: address2
            x: 230
            y: 260
            text: qsTr("IP address")
            font.pixelSize: 16
            font.family:"Roboto"
            color: "#A2A9B0"
        }

        Rectangle {
            id: ipAddressInput2
            x: 230
            y: 280
            width:240
            height:30
            color: combo_colors[themeIndex]
            border.width: 1
            radius: 4

            property bool hasFocus: field2_1.activeFocus || field2_2.activeFocus || field2_3.activeFocus || field2_4.activeFocus

            border.color: hasFocus ? "#4CC2FF" : combo_border[themeIndex]

            // IPアドレスの各フィールドを格納するプロパティ
            property var fields: [field2_1, field2_2, field2_3, field2_4]

            Row {
                anchors.fill: parent
                anchors.margins: 2
                anchors.centerIn: parent
                spacing: 0

                // --- 1つ目 ---
                Item { width: 60; height: parent.height +3
                    TextField {
                        id: field2_1
                        text: typeof(bridge) !== "undefined" ? bridge.ip_ports[1][0] : 0
                        anchors.fill: parent
                        font.pixelSize: 12
                        font.family:"Roboto"
                        background: null
                        padding: 0
                        horizontalAlignment: Text.AlignRight
                        maximumLength: 3
                        inputMethodHints: Qt.ImhDigitsOnly
                        validator: IntValidator { bottom:0; top:255 }

                        color: text_colors[themeIndex]

                        onTextChanged: {
                            if(text.length === 3) field2_2.forceActiveFocus()
                            if (typeof(bridge) !== "undefined") bridge.set_ip_port(1, 0, text)
                        }
                    }
                    Text { text: "."; font.pixelSize: 16; anchors.verticalCenter: parent.verticalCenter; anchors.right: parent.right; anchors.rightMargin: -2;
                           color:text_colors[themeIndex]}
                }

                // --- 2つ目 ---
                Item { width: 60; height: parent.height +3
                    TextField {
                        id: field2_2
                        text: typeof(bridge) !== "undefined" ? bridge.ip_ports[1][1] : 0
                        anchors.fill: parent
                        font.pixelSize: 12
                        font.family:"Roboto"
                        background: null
                        padding: 0
                        horizontalAlignment: Text.AlignRight
                        maximumLength: 3
                        inputMethodHints: Qt.ImhDigitsOnly
                        validator: IntValidator { bottom:0; top:255 }

                        color: text_colors[themeIndex]

                        onTextChanged: {
                            if (text.length === 3) field2_3.forceActiveFocus()
                            if (typeof(bridge) !== "undefined") bridge.set_ip_port(1, 1, text)
                        }
                    }
                    Text { text: "."; font.pixelSize: 16; anchors.verticalCenter: parent.verticalCenter; anchors.right: parent.right; anchors.rightMargin: -2;
                           color: text_colors[themeIndex] }
                }

                // --- 3つ目 ---
                Item { width: 60; height: parent.height +3
                    TextField {
                        id: field2_3
                        text: typeof(bridge) !== "undefined" ? bridge.ip_ports[1][2] : 0
                        anchors.fill: parent
                        font.pixelSize: 12
                        font.family:"Roboto"
                        background: null
                        padding: 0
                        horizontalAlignment: Text.AlignRight
                        maximumLength: 3
                        inputMethodHints: Qt.ImhDigitsOnly
                        validator: IntValidator { bottom:0; top:255 }

                        color: text_colors[themeIndex]

                        onTextChanged: {
                            if (text.length === 3) field2_4.forceActiveFocus()
                            if (typeof(bridge) !== "undefined") bridge.set_ip_port(1, 2, text)
                        }
                    }
                    Text { text: "."; font.pixelSize: 16; anchors.verticalCenter: parent.verticalCenter; anchors.right: parent.right; anchors.rightMargin: -2;
                           color:text_colors[themeIndex] }
                }

                // --- 4つ目 ---
                TextField {
                    id: field2_4
                    text: typeof(bridge) !== "undefined" ? bridge.ip_ports[1][3] : 0
                    width: 60
                    height: parent.height +3
                    font.pixelSize: 12
                    font.family:"Roboto"
                    background: null
                    padding: 0
                    horizontalAlignment: Text.AlignRight
                    maximumLength: 3
                    inputMethodHints: Qt.ImhDigitsOnly
                    validator: IntValidator { bottom:0; top:255 }

                    color: text_colors[themeIndex]

                    onTextChanged: {
                        if (typeof(bridge) !== "undefined") bridge.set_ip_port(1, 3, text)
                    }
                }
            }

            function getAddress() {
                return [field2_1.text || "0", field2_2.text || "0", field2_3.text || "0", field2_4.text || "0"].join(".")
            }
        }
    }
}
