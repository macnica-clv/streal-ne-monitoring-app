import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Effects
import QtQuick.Controls.Material


Rectangle {
    width: parent ? parent.width : 0
    height: parent ? parent.height : 0
    property var colors: ["#F1F3FC", "#EEF2F7", "#2A2D36"]
    property var text_colors: ["#343A3F", "#343A3F", "#FFFFFF"]
    property var button_colors: ["#3F51B5", "#3F51B5", "#4CC2FF"]
    color: typeof(appBridge) !== "undefined" ? colors[appBridge.theme] : "#2A2D36"

    Text {
        x:20
        y:10
        text: qsTr("Auto save")
        font.pointSize: 9
        font.family:"Yu Gothic"
        font.bold: true
        color: typeof(appBridge) !== "undefined" ? text_colors[appBridge.theme] : "#343A3F"
    }
    Switch {
        x:90
        id: autoSaveSwitch
        scale: 0.85
        checked: typeof(bridge) !== "undefined" ? bridge.auto_save : false
        Material.accent: typeof(appBridge) !== "undefined" ? button_colors[appBridge.theme] : "#4CC2FF"
        onClicked: bridge?.set_auto_save(checked)
    }

    Text {
        x:5
        y:40
        text: qsTr("Per-Filter Logging Control")
        font.pointSize: 9
        font.family:"Yu Gothic"
        font.bold: true
        color:  typeof(appBridge) !== "undefined" ? text_colors[appBridge.theme] : "#343A3F"
    }
    Row {
        x:5
        y:55
        spacing: 40

        Item {
            width: maCheck.implicitWidth
            height: maCheck.implicitHeight

            Rectangle {
                width: 16
                height: 16
                color: autoSaveSwitch.checked ? "#FFFFFF" : "#cccccc"
                anchors.left: parent.left
                anchors.leftMargin: 9
                anchors.verticalCenter: parent.verticalCenter
            }

            CheckBox {
                id: maCheck
                text: qsTr("Moving Average")
                enabled: autoSaveSwitch.checked
                checked: typeof(bridge) !== "undefined" ? bridge.save_ma : false
                Material.accent: typeof(appBridge) !== "undefined" ? button_colors[appBridge.theme] : "#4CC2FF"
                onClicked: bridge?.set_save_ma(checked)

                contentItem: Text {
                    text: maCheck.text
                    color: typeof(appBridge) !== "undefined" ? text_colors[appBridge.theme] : "#343A3F"
                    font.pointSize: 9
                    font.family: "Yu Gothic"
                    font.bold: true
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: maCheck.indicator.width + maCheck.spacing
                    opacity: maCheck.enabled ? 1.0 : 0.4
                }
            }
        }

        Item {
            width: fftCheck.implicitWidth
            height: fftCheck.implicitHeight

            Rectangle {
                width: 16
                height: 16
                color: autoSaveSwitch.checked ? "#FFFFFF" : "#cccccc"
                anchors.left: parent.left
                anchors.leftMargin: 9
                anchors.verticalCenter: parent.verticalCenter
            }

            CheckBox {
                id: fftCheck
                text: qsTr("FFT")
                enabled: autoSaveSwitch.checked
                checked: typeof(bridge) !== "undefined" ? bridge.save_fft : false
                Material.accent: typeof(appBridge) !== "undefined" ? button_colors[appBridge.theme] : "#4CC2FF"
                onClicked: bridge?.set_save_fft(checked)

                contentItem: Text {
                    text: fftCheck.text
                    color: typeof(appBridge) !== "undefined" ? text_colors[appBridge.theme] : "#343A3F"
                    font.pointSize: 9
                    font.family: "Yu Gothic"
                    font.bold: true
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: fftCheck.indicator.width + fftCheck.spacing
                    opacity: fftCheck.enabled ? 1.0 : 0.4
                }
            }
        }

        Item {
            width: sdCheck.implicitWidth
            height: sdCheck.implicitHeight

            Rectangle {
                width: 16
                height: 16
                color: autoSaveSwitch.checked ? "#FFFFFF" : "#cccccc"
                anchors.left: parent.left
                anchors.leftMargin: 9
                anchors.verticalCenter: parent.verticalCenter
            }

            CheckBox {
                id: sdCheck
                text: qsTr("Standard Deviation")
                enabled: autoSaveSwitch.checked
                checked: typeof(bridge) !== "undefined" ? bridge.save_std : false
                Material.accent: typeof(appBridge) !== "undefined" ? button_colors[appBridge.theme] : "#4CC2FF"
                onClicked: bridge?.set_save_std(checked)

                contentItem: Text {
                    text: sdCheck.text
                    color: typeof(appBridge) !== "undefined" ? text_colors[appBridge.theme] : "#343A3F"
                    font.pointSize: 9
                    font.family: "Yu Gothic"
                    font.bold: true
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: sdCheck.indicator.width + sdCheck.spacing
                    opacity: sdCheck.enabled ? 1.0 : 0.4
                }
            }
        }
    }
}