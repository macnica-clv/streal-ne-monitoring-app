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

    Text {
        x:6
        y:5
        text: qsTr("Moving Average")
        font.bold: true
        font.pointSize: 10
        font.family:"Roboto"
        color: text_colors[themeIndex]
    }

    Switch {
        x:160
        y:7
        id: movingAverageSwitch
        checked: typeof(bridge) !== "undefined" ? bridge.moving_average : false
        scale: 0.85
        Material.accent: button_colors[themeIndex]
        onClicked: {
            if (typeof(bridge) !== "undefined"){
                bridge.change_moving_average(checked)
            }
        }
    }

    Text {
        x:6
        y:24
        text: qsTr("Noise Reduction and Smoothing")
        font.pointSize: 8
        font.family:"Roboto"
        color: "#A2A9B0"
    }

    Text {
        x:11
        y:61
        text: qsTr("Window Size :")
        font.pointSize: 10
        font.family:"Roboto"
        color:text_colors[themeIndex]
    }
    TextField {
        id: windowSize
        property bool is_error: false

        x: 120
        y: 54
        width: 94
        height: 30
        Material.accent: button_colors[themeIndex]
        font.pixelSize: 12
        font.family:"Roboto"
        placeholderText: qsTr("Enter value")
        placeholderTextColor: {
            if (windowSize.activeFocus) {
                return button_colors[themeIndex]
            } else {
                return "#A2A9B0"
            }
        }

        inputMethodHints: Qt.ImhDigitsOnly // 数字のみ入力
        validator: IntValidator { bottom: 0; top: 9999 } // 0～1000制限
        text: typeof(bridge) !== "undefined" ? bridge.moving_average_window_size : 1
        color: text_colors[themeIndex]
        background: Rectangle {
            radius: 3
            color: {
                if (windowSize.activeFocus) {
                    // フォーカス時：少し暗く
                    return field_focus_colors[themeIndex]
                } else {
                    // 通常時
                    return field_colors[themeIndex]
                }
            }
            border.color: windowSize.is_error ? "red" : border_colors[themeIndex]
        }

        onTextChanged: {
            if (typeof(bridge) !== "undefined"){
                var value = text ? Number(text) : 0;
                is_error = value < 2 || 1000 < value;
                bridge.change_moving_average_window_size(value);
            }
        }
    }
}
