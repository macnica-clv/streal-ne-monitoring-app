import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Effects
import QtQuick.Controls.Material


Rectangle {
    width: parent.width
    height: parent.height
    color: "transparent"
    border.width: 1
    border.color: "#DDE1E6"

    Text {
        x:6
        y:5
        text: qsTr("Standard Deviation")
        font.bold: true
        font.pointSize: 10
        font.family:"Roboto"
    }

    Switch {
        x:160
        y:7
        id: sDSwitch
        checked: typeof(bridge) !== "undefined" ? bridge.standard_deviation : false
        scale: 0.85
        Material.accent: Material.Indigo
        onClicked:bridge.change_standard_deviation(checked)
    }

    Text {
        x:6
        y:24
        text: qsTr("Data Variability Analysis")
        font.pointSize: 8
        font.family:"Roboto"
        color: "#697077"
    }

    Text {
        x:11
        y:61
        text: qsTr("Window Size：")
        font.pointSize: 10
        font.family:"Roboto"
    }

    TextField {
        id: windowSize2
        x: 120
        y: 54
        width: 100
        height: 30
        Material.accent: Material.Indigo
        font.pixelSize: 12
        font.family:"Roboto"
        placeholderText: qsTr("Enter value")
        inputMethodHints: Qt.ImhDigitsOnly // 数字のみ入力
        validator: IntValidator { bottom: 0; top: 1000 } // 0～1000制限
        text: typeof(bridge) !== "undefined" ? bridge.standard_deviation_window_size : 1

        onEditingFinished: {
            var val = parseInt(text);
            if (!isNaN(val)) {
                val = Math.max(1, Math.min(1000, val)); // 範囲制限
            }
            bridge.change_standard_deviation_window_size(val)
        }
    }
}