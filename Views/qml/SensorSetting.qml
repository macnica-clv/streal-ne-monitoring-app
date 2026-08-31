import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Effects
import QtQuick.Controls.Material


Rectangle {

    width: parent ? parent.width : 0
    height: parent ? parent.height : 0

    property var _appBridge: (typeof(appBridge) !== "undefined" && appBridge !== null)
                          ? appBridge
                          : null

    property int themeIndex: _appBridge ? _appBridge.theme : 0

    property var colors: ["#FFFFFF", "#FFFFFF", "#393D47"]
    property var text_colors: ["#343A3F", "#343A3F", "#FFFFFF"]
    property var border_colors: ["#D0D5DD", "#D0D5DD", "#393D47"]
    property var colors2: ["#F2F4F8", "#F2F4F8", "#2A2D35"]
    property var field_colors: ["#FFFFFF", "#FFFFFF", "#525563"]
    property var field_focus_colors: ["#FFFFFF", "#FFFFFF", "#1E2024"]
    property var button_colors: ["#3F51B5", "#3F51B5", "#4CC2FF"]

    color: colors[themeIndex]
    border.width: 1
    border.color: border_colors[themeIndex]
    property double offsetValue: typeof(bridge) !== "undefined" ? bridge.line_offset : 0

    Text {
        x:11
        y:5
        text: `CH${typeof(bridge) !== "undefined" ? bridge.ch + 1 : 0} ` + qsTr("Waveform Settings")
        font.bold: true
        font.pointSize: 10
        font.family:"Roboto"
        color: text_colors[themeIndex]
    }

    // 線の色モデル
    ListModel {
        id: colorModel
        ListElement { name: qsTr("Red");     hex: "#e53935" }
        ListElement { name: qsTr("Orange");  hex: "#fb8c00" }
        ListElement { name: qsTr("Yellow");  hex: "#fdd835" }
        ListElement { name: qsTr("Green");   hex: "#43a047" }
        ListElement { name: qsTr("Cyan");    hex: "#00acc1" }
        ListElement { name: qsTr("Blue");    hex: "#1e88e5" }
        ListElement { name: qsTr("Purple");  hex: "#8e24aa" }
        ListElement { name: qsTr("Gray");    hex: "#9e9e9e" }
        ListElement { name: qsTr("Black");   hex: "#212121" }
        ListElement { name: qsTr("White");   hex: "#ffffff" }
    }

    // 線の太さモデル
    ListModel {
        id: widthModel
        ListElement { name: "1.0"; value: 1 }
        ListElement { name: "1.5"; value: 1.5 }
        ListElement { name: "2.0"; value: 2 }
        ListElement { name: "3.0"; value: 3 }
        ListElement { name: "10.0"; value: 10 }
    }

    //線の色
    Text {
        x:11
        y:33
        text: qsTr("Strain Color：")
        font.pointSize: 10
        font.family:"Roboto"
        color: text_colors[themeIndex]
    }
    ComboBox {
        id: colorCombo
        model: colorModel
        x: 148
        y: 31
        height:18
        width: 50
        Material.accent: button_colors[themeIndex]
        editable: false
        flat: false
        // 初期選択
        currentIndex: typeof(bridge) !== "undefined" ? bridge.strain_line_color : 2
        // Layout.preferredWidth: 220
        Layout.alignment: Qt.AlignLeft
        onCurrentIndexChanged: {
            if (typeof(bridge) !== "undefined"){
                bridge.change_strain_line_color_index(colorCombo.currentIndex)
            }
        }
        background: Rectangle {
            color: field_colors[themeIndex]
            border.color: border_colors[themeIndex]
            radius: 4
        }
        indicator: Canvas {
            id: arrow
            width: 8; height: 6
            x: colorCombo.width - width - 8
            y: (colorCombo.height - height) / 2
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
                target: _appBridge
                function onThemeChanged() { arrow.requestPaint() }
            }
            Component.onCompleted: arrow.requestPaint()
        }
        // コンボボックスの表示部分（選択中の項目にスウォッチを表示）
        contentItem: Row {
            anchors.fill: parent
            anchors.margins: 3
            spacing: 8
            Rectangle {
                id: preview
                width: 13; height: 13
                radius: 4
                color: (colorCombo.currentIndex >= 0) ? colorModel.get(colorCombo.currentIndex).hex : "transparent"
                border.color: Qt.darker(color, 1.4) // ちょっとだけ縁取る
            }
            Text {
                color:text_colors[themeIndex]
            }
            /*Text {
                text: (colorCombo.currentIndex >= 0) ? colorModel.get(colorCombo.currentIndex).name : qsTr("選択してください")
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
            }*/
        }

        // ドロップダウンの中身（デリゲート）
        delegate: ItemDelegate {
            width: parent.width
            height: 30

            Row {
                anchors.left: parent.left
                anchors.leftMargin: 6
                anchors.verticalCenter: parent.verticalCenter
                spacing: 10
                Rectangle {
                    width: 20; height: 20; radius: 4
                    color: model.hex
                    border.width: 1
                    border.color: (model.hex.toLowerCase() === "#ffffff") ? "#bdbdbd" : "transparent"
                }

                Text {
                    text: model.name
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                    color: text_colors[themeIndex]
                }
            }
        }

        popup: Popup {
            y: colorCombo.height
            width: 100
            x: colorCombo.width - width
            padding: 0
            implicitHeight: Math.min(listView2.contentHeight, 90)

            contentItem: ListView {
                id: listView2
                clip: true
                model: colorCombo.popup.visible ? colorCombo.delegateModel : null
                currentIndex: colorCombo.highlightedIndex
                delegate: colorCombo.delegate
            }

            background: Rectangle {
                radius: 1
                color: field_colors[themeIndex]
                border.color: border_colors[themeIndex]
            }

        }
    }

        //線の色
    Text {
        x:11
        y:61
        text: qsTr("Temperature Color：")
        font.pointSize: 10
        font.family:"Roboto"
        color: text_colors[themeIndex]
    }
    ComboBox {
        id: colorCombo2
        model: colorModel
        x: 148
        y: 61
        height:18
        width: 50
        Material.accent: button_colors[themeIndex]
        editable: false
        flat: false
        // 初期選択
        currentIndex: typeof(bridge) !== "undefined" ? bridge.temp_line_color : 2
        // Layout.preferredWidth: 220
        Layout.alignment: Qt.AlignLeft
        onCurrentIndexChanged: {
            if (typeof(bridge) !== "undefined"){
                bridge.change_temp_line_color_index(colorCombo2.currentIndex)
            }
        }
        background: Rectangle {
            color: field_colors[themeIndex]
            border.color: border_colors[themeIndex]
            radius: 4
        }
        indicator: Canvas {
            id: arrow2
            width: 8; height: 6
            x: colorCombo2.width - width - 8
            y: (colorCombo2.height - height) / 2
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
                target: _appBridge
                function onThemeChanged() { arrow2.requestPaint() }
            }
            Component.onCompleted: arrow2.requestPaint()
        }

        // コンボボックスの表示部分（選択中の項目にスウォッチを表示）
        contentItem: Row {
            anchors.fill: parent
            anchors.margins: 3
            spacing: 8
            Rectangle {
                id: preview2
                width: 13; height: 13
                radius: 4
                color: (colorCombo2.currentIndex >= 0) ? colorModel.get(colorCombo2.currentIndex).hex : "transparent"
                border.color: Qt.darker(color, 1.4) // ちょっとだけ縁取る
            }
            Text {
                color:text_colors[themeIndex]
            }
            /*Text {
                text: (colorCombo2.currentIndex >= 0) ? colorModel.get(colorCombo2.currentIndex).name : qsTr("選択してください")
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
            }*/
        }

        // ドロップダウンの中身（デリゲート）
        delegate: ItemDelegate {
            width: parent.width
            height: 30
            Row {
                anchors.left: parent.left
                anchors.leftMargin: 6
                anchors.verticalCenter: parent.verticalCenter
                spacing: 10

                Rectangle {
                    width: 20; height: 20; radius: 4
                    color: model.hex
                    border.width: 1
                    border.color: (model.hex.toLowerCase() === "#ffffff") ? "#bdbdbd" : "transparent"
                }

                Text {
                    text: model.name
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                    color: text_colors[themeIndex]
                }
            }
        }
        popup: Popup {

            width: 100
            x: colorCombo2.width - width
            padding: 0
            implicitHeight: Math.min(listView3.contentHeight, 90)

            contentItem: ListView {
                id: listView3
                clip: true
                model: colorCombo2.popup.visible ? colorCombo2.delegateModel : null
                currentIndex: colorCombo2.highlightedIndex
                delegate: colorCombo2.delegate
            }

            background: Rectangle {
                radius: 1
                color: field_colors[themeIndex]
                border.color: border_colors[themeIndex]
            }

        }
    }

    //線の太さ
    Text {
        x:11
        y:89
        text: qsTr("Line Width：")
        font.pointSize: 10
        font.family:"Roboto"
        color: text_colors[themeIndex]
    }

    ComboBox {
        id: widthCombo
        model: widthModel
        x: 108
        y: 86
        currentIndex: typeof(bridge) !== "undefined" ? bridge.line_width : 3
        width: 90
        height: 22
        Material.accent: Material.Indigo
        onCurrentIndexChanged: {
            if (typeof(bridge) !== "undefined"){
                bridge.change_line_width_index(widthCombo.currentIndex)
            }
        }
        background: Rectangle {
            color: field_colors[themeIndex]
            border.color: border_colors[themeIndex]
            radius: 4
        }
        indicator: Canvas {
            id: arrow3
            width: 8; height: 6
            x: widthCombo.width - width - 8
            y: (widthCombo.height - height) / 2
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
                target: _appBridge
                function onThemeChanged() { arrow3.requestPaint() }
            }
            Component.onCompleted: arrow3.requestPaint()
        }

        // 選択中の表示部
        contentItem: Row {
            anchors.fill: parent
            anchors.margins: 3
            spacing: 8

            Text {
                text: {
                    var color = widthModel.get(widthCombo.currentIndex)
                    return color !== undefined ? color.name : "-"
                }
                verticalAlignment: Text.AlignHCenter
                color: text_colors[themeIndex]
            }
            Rectangle {
                width: 30; height: 20
                color: "transparent"
                border.color: "transparent"
                Canvas {
                    id: contentCanvas
                    anchors.fill: parent
                    onPaint: {
                        var ctx = getContext("2d");
                        ctx.reset();
                        ctx.strokeStyle = text_colors[themeIndex];
                        ctx.lineWidth = widthModel.get(widthCombo.currentIndex).value;
                        ctx.beginPath();
                        ctx.moveTo(5, height/2);
                        ctx.lineTo(width-5, height/2);
                        ctx.stroke();
                    }
                    Connections {
                        target: _appBridge
                        function onThemeChanged() { contentCanvas.requestPaint() }
                    }
                }
                Connections {
                    target: widthCombo
                    function onCurrentIndexChanged(){
                        contentCanvas.requestPaint()
                    }
                }
            }
        }

        // ドロップダウンのリスト（delegate）
        delegate: ItemDelegate {
            width: parent.width
            height: 30
            Row {
                anchors.left: parent.left
                anchors.leftMargin: 6
                anchors.verticalCenter: parent.verticalCenter
                spacing: 10

                Rectangle {
                    width: 60; height: 20
                    color: "transparent"
                    border.color: "transparent"
                    Canvas {
                        anchors.fill: parent
                        onPaint: {
                            var ctx = getContext("2d");
                            ctx.reset();
                            ctx.strokeStyle =text_colors[themeIndex];
                            ctx.lineWidth = model.value;
                            ctx.beginPath();
                            ctx.moveTo(5, height/2);
                            ctx.lineTo(width-5, height/2);
                            ctx.stroke();
                        }
                        Connections {
                            target: _appBridge
                            function onThemeChanged() { delegateCanvas.requestPaint() }
                        }
                    }
                }
                Text {
                    text: model.name
                    verticalAlignment: Text.AlignHCenter
                    color: text_colors[themeIndex]
                }
            }
        }
        popup: Popup {
            y: widthCombo.height
            width: 120
            x: widthCombo.width - width
            padding: 0
            implicitHeight: Math.min(listView4.contentHeight, 130)

            contentItem: ListView {
                id: listView4
                clip: true
                model: widthCombo.popup.visible ? widthCombo.delegateModel : null
                currentIndex: widthCombo.highlightedIndex
                delegate: widthCombo.delegate
            }

            background: Rectangle {
                radius: 1
                color: field_colors[themeIndex]
                border.color: border_colors[themeIndex]
            }

        }

    }

    //オフセット
    Text {
        x:11
        y:117
        text: qsTr("Offset：")
        font.pointSize: 10
        font.family:"Roboto"
        color: text_colors[themeIndex]
    }

    Rectangle {
        x: 88
        y: 114
        width: 110
        height: 22
        border.color: border_colors[themeIndex]
        radius: 4
        color: {
            if (offsetInput.activeFocus) {
                return field_focus_colors[themeIndex]
            } else {
                return field_colors[themeIndex]
            }
        }
    }
    Button {
        x: 89
        y: 109
        width: 20
        height: 30
        flat: true
        text: "-"
        contentItem: Text {
            text: parent.text
            font: parent.font
            color: text_colors[themeIndex]
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.fill: parent
        }

        onClicked: {
            offsetValue = Math.max(-1000, offsetValue - 1.0);
            offsetInput.text = (offsetValue >= 0 ? "+" : "") + Math.round(offsetValue);
            bridge.change_line_offset_value(offsetValue)
        }

    }
    Button {
        x: 177
        y: 109
        width: 20
        height: 30
        flat: true
        text: "+"
        contentItem: Text {
            text: parent.text
            font: parent.font
            color: text_colors[themeIndex]
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.fill: parent
        }

        onClicked: {
            offsetValue = Math.min(1000, offsetValue + 1.0);
            offsetInput.text = (offsetValue >= 0 ? "+" : "") + Math.round(offsetValue);
            bridge.change_line_offset_value(offsetValue)
        }

    }

    TextField {
        id: offsetInput
        x: 114
        y: 109
        background: null
        inputMethodHints: Qt.ImhFormattedNumbersOnly
        text: (offsetValue >= 0 ? "+" : "") + Math.round(offsetValue)
        width: 75
        Material.accent: button_colors[themeIndex]
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
        color: text_colors[themeIndex]

        onEditingFinished: {
            var val = parseFloat(text);
            if (!isNaN(val)) {
                offsetValue = Math.max(-1000, Math.min(1000, val)); // 範囲制限
            }
            text = (offsetValue >= 0 ? "+" : "") + Math.round(offsetValue);
            bridge.change_line_offset_value(offsetValue)
        }


    }

    signal changedSignal(bool checked)

}