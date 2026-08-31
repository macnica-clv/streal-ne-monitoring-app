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
    color: colors[themeIndex]

    property var text_colors: ["#343A3F", "#343A3F", "#FFFFFF"]
    property var button_colors: ["#3F51B5", "#3F51B5", "#4CC2FF"]
    property var field_colors: ["#FFFFFF", "#FFFFFF", "#525563"]
    property var field_focus_colors: ["#FFFFFF", "#FFFFFF", "#1E2024"]
    property var border_colors: ["#D0D5DD", "#D0D5DD", "#393D47"]
    property var colors2: ["#F2F4F8", "#F2F4F8", "#2A2D35"]

    Text {
        x:6
        y:5
        text: "FFT"
        font.bold: true
        font.pointSize: 10
        font.family:"Roboto"
        color: text_colors[themeIndex]
    }

    Switch {
        x:160
        y:7
        id: fftSwitch
        checked: typeof(bridge) !== "undefined" ? bridge.fft : false
        scale: 0.85
        Material.accent: button_colors[themeIndex]
        onClicked:bridge.change_fft(checked)
    }

    Text {
        x:6
        y:27
        text: qsTr("Frequency Domain Analysis")
        font.pointSize: 8
        font.family:"Roboto"
        color: "#A2A9B0"
    }

    Text {
        x:11
        y:61
        text: qsTr("Resolution：")
        font.pointSize: 10
        font.family:"Roboto"
        color: text_colors[themeIndex]
    }

    TextField {
        id: resolutionSize
        property bool is_error: false

        x: 120
        y: 57
        width: 94
        height: 30
        Material.accent: button_colors[themeIndex]
        font.pixelSize: 12
        font.family:"Roboto"
        placeholderText: qsTr("Enter value")
        inputMethodHints: Qt.ImhDigitsOnly // 数字のみ入力
        text: typeof(bridge) !== "undefined" ? bridge.fft_resolution : 256
        validator: IntValidator { bottom: 0; top: 99999 }
        color: text_colors[themeIndex]
        placeholderTextColor: {
            if (resolutionSize.activeFocus) {
                return button_colors[themeIndex]
            } else {
                return "#A2A9B0"
            }
        }
        background: Rectangle {
            radius: 3
            color: {
                if (resolutionSize.activeFocus) {
                    // フォーカス時：少し暗く
                    return field_focus_colors[themeIndex]
                } else {
                    // 通常時
                    return field_colors[themeIndex]
                }
            }
            border.color: resolutionSize.is_error ? "red" : border_colors[themeIndex]
        }

        onTextChanged: {
            if (typeof(bridge) !== "undefined") {
                var value = text ? Number(text) : 0;
                is_error = value < 256 || 16384 < value;
                bridge.change_fft_resolution(value);
            }
        }
    }

    Text {
        x:11
        y:111
        text: qsTr("Window：")
        font.pointSize: 10
        font.family:"Roboto"
        color: text_colors[themeIndex]
    }

    ComboBox {
        id: window
        x: 90
        y: 104
        width: 124
        height: 30
        Material.accent: button_colors[themeIndex]
        model: ListModel {
            ListElement { text: "-" }
            ListElement { text: qsTr("Rectangular") }
            ListElement { text: qsTr("Hanning") }
            ListElement { text: qsTr("Hamming") }
            ListElement { text: qsTr("Blackman") }
            ListElement { text: qsTr("Blackman-Harris") }
            ListElement { text: qsTr("Flat-top") }
        }
        currentIndex: typeof(bridge) !== "undefined" ? bridge.fft_window : 0

        contentItem: Text {
            text: window.displayText
            font: window.font
            color: text_colors[themeIndex]
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
            leftPadding: 8
            rightPadding: window.indicator.width + 8
        }
        background: Rectangle {
            color: field_colors[themeIndex]
            border.color: border_colors[themeIndex]
            radius: 4
        }
        indicator: Canvas {
            id: arrow
            width: 12; height: 8
            x: window.width - width - 8
            y: (window.height - height) / 2
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


        delegate: ItemDelegate {
            width: window.width
            text: model.text
            font: window.font
            highlighted: window.highlightedIndex === index

            contentItem: Text {
                text: model.text
                font: window.font
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
                color: text_colors[themeIndex]
            }

        }

        popup: Popup {
            y: window.height + 7
            width: window.width
            padding: 0
            implicitHeight: Math.min(listView.contentHeight, 180)

            contentItem: ListView {
                id: listView
                clip: true
                model: window.popup.visible ? window.delegateModel : null
                currentIndex: window.highlightedIndex
                delegate: window.delegate
            }

            background: Rectangle {
                radius: 1
                color: field_colors[themeIndex]
            }

        }

        onCurrentIndexChanged: {
            if (typeof(bridge) !== "undefined") {
                bridge.change_fft_window(currentIndex);
            }
        }
    }

    Rectangle {
        x: 8
        y: 145
        width: parent.width - 16
        height: 147
        color: colors2[themeIndex]
    }

    Text {
        x:11
        y:152
        text: qsTr("Schedule Setting")
        font.pointSize: 10
        font.family:"Roboto"
        color: text_colors[themeIndex]
    }

    Rectangle {
        x: 130
        y: 151
        width: 16
        height: 16
        color: "#FFFFFF"
    }

    CheckBox {
        x: 117
        y: 136
        id: scheduleCheck
        Material.accent: button_colors[themeIndex]
        checked: false
        onToggled: {
            if (typeof(bridge) !== "undefined") {
                bridge.change_fft_use_schedule(checked);
            }
        }
    }

    Text {
        x:13
        y:175
        text: qsTr("Start Timing")
        font.pointSize: 9
        font.family:"Roboto"
        color: text_colors[themeIndex]
    }

    TextField {
        id: dateField
        property string border_color: "#D0D5DD"
        x: 13
        y: 197
        width: 115
        height: 30
        Material.accent: button_colors[themeIndex]
        color: text_colors[themeIndex]
        placeholderTextColor: {
            if (dateField.activeFocus) {
                return button_colors[themeIndex]
            } else {
                return "#A2A9B0"
            }
        }
        placeholderText: "YYYY/MM/DD"
        text: ""
        inputMask: "0000/00/00;_"
        background: Rectangle {
            radius: 3
            color: {
                if (dateField.activeFocus) {
                    // フォーカス時：少し暗く
                    return field_focus_colors[themeIndex]
                } else {
                    // 通常時
                    return field_colors[themeIndex]
                }
            }
            border.color: typeof(bridge) !== "undefined" ? (bridge.fft_start_time_error ? "red" : border_colors[themeIndex]) : border_colors[themeIndex]
        }

        onTextChanged: {
            var parts = text.split("/");
            if (parts.length === 3) {
                var yyyy = parseInt(parts[0]);
                var mm = parseInt(parts[1]);
                var dd = parseInt(parts[2]);
                if (mm < 1 || mm > 12 || dd < 1 || dd > 31) {
                    console.log("Invalid time:", text);
                    dateField.border_color = "red";
                }else{
                    dateField.border_color = "#D0D5DD";
                }
                if (typeof(bridge) !== "undefined") {
                    bridge.change_fft_start_day(text);
                }
            }
        }
    }

    TextField {
        id: time
        property string border_color: "#D0D5DD"
        x: 134
        y: 197
        width: 79
        height: 30
        Material.accent: button_colors[themeIndex]
        placeholderTextColor: {
            if (time.activeFocus) {
                return button_colors[themeIndex]
            } else {
                return "#A2A9B0"
            }
        }
        color: text_colors[themeIndex]
        placeholderText: "HH/MM"
        text: ""
        inputMask: "00:00;_ "
        background: Rectangle {
            radius: 3
            color: {
                if (time.activeFocus) {
                    // フォーカス時：少し暗く
                    return field_focus_colors[themeIndex]
                } else {
                    // 通常時
                    return field_colors[themeIndex]
                }
            }
            border.color: typeof(bridge) !== "undefined" ? (bridge.fft_start_time_error ? "red" : border_colors[themeIndex]) : border_colors[themeIndex]
        }

        onTextChanged: {
            var parts = text.split(":");
            if (parts.length === 2) {
                var hh = parseInt(parts[0]);
                var mm = parseInt(parts[1]);
                if (hh < 0 || hh > 23 || mm < 0 || mm > 59) {
                    console.log("Invalid time:", text);
                    time.border_color = "red";
                }else{
                    time.border_color = "#D0D5DD";
                }
                if (typeof(bridge) !== "undefined") {
                    bridge.change_fft_start_time(text);
                }
            }
        }
    }

    function validateInterval() {
        var value = Number(numField.text);
        if (value < 1 || 999 < value){
            numField.background.border.color = "red";
            return;
        }

        var unit = timeCombo.currentIndex;
        switch(unit){
            case 0:
                var sec = value;
                break;
            case 1:
                var sec = value * 60;
                break;
            case 2:
                var sec = value * 60 * 60;
                break;
            case 3:
                var sec = value * 60 * 60 * 24;
                break;
            default:
                timeCombo.background.border.color = "red";
                return;
        }

        numField.isError = false
        timeCombo.isError = false

        if (typeof(bridge) !== "undefined") {
            bridge.change_fft_interval(sec);
        }
    }

    Text {
        x:13
        y:235
        text: qsTr("Interval")
        font.pointSize: 9
        font.family:"Roboto"
        color: text_colors[themeIndex]
    }

    TextField {
        id: numField
        property bool isError: false
        x: 13
        y: 254
        width: 90
        height: 30
        Material.accent: button_colors[themeIndex]
        text: "1"
        inputMethodHints: Qt.ImhDigitsOnly
        color: text_colors[themeIndex]
        validator: IntValidator {
            bottom: 0
            top: 999    // 最大3桁
        }
        background: Rectangle {
            radius: 3
            color: {
                if (numField.activeFocus) {
                    // フォーカス時：少し暗く
                    return field_focus_colors[themeIndex]
                } else {
                    // 通常時
                    return field_colors[themeIndex]
                }
            }
            border.color: numField.isError
                      ? "red"
                      : border_colors[themeIndex]
        }
        onTextChanged: validateInterval()
    }

    ComboBox {
        id: timeCombo
        property bool isError: false
        x: 109
        y: 254
        width: 104
        height: 30
        Material.accent: Material.Indigo
        model: ListModel {
            ListElement { text: qsTr("second") }
            ListElement { text: qsTr("minute") }
            ListElement { text: qsTr("hour") }
            ListElement { text: qsTr("day") }
        }
        contentItem: Text {
            text: timeCombo.displayText
            font: timeCombo.font
            color: text_colors[themeIndex]
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
            leftPadding: 8
            rightPadding: timeCombo.indicator.width + 8
        }
        background: Rectangle {
            color: field_colors[themeIndex]
            border.color: timeCombo.isError
                      ? "red"
                      : border_colors[themeIndex]
            radius: 4
        }
        indicator: Canvas {
            id: arrow2
            width: 12; height: 8
            x: timeCombo.width - width - 8
            y: (timeCombo.height - height) / 2
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
        delegate: ItemDelegate {
            width: timeCombo.width
            text: model.text
            font: timeCombo.font
            highlighted: timeCombo.highlightedIndex === index

            contentItem: Text {
                text: model.text
                font: timeCombo.font
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
                color: text_colors[themeIndex]
            }

        }
        popup: Popup {
            y: timeCombo.height + 7
            width: timeCombo.width
            padding: 0
            implicitHeight: Math.min(listView2.contentHeight, 180)

            contentItem: ListView {
                id: listView2
                clip: true
                model: timeCombo.popup.visible ? timeCombo.delegateModel : null
                currentIndex: timeCombo.highlightedIndex
                delegate: timeCombo.delegate
            }

            background: Rectangle {
                radius: 1
                color: field_colors[themeIndex]
            }

        }

        onCurrentIndexChanged: validateInterval()
    }
}

