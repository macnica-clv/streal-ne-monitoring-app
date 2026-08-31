import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Effects
import QtQuick.Controls.Material

Rectangle {
    width: parent.width
    height: parent.height

    property var colors: ["#3E4784", "#F7F7F8", "#000000"]
    color: typeof(bridge) !== "undefined" ? colors[bridge.theme] : "#FFFFFF"

    Material.accent: Material.Indigo

    function getImageFromStatus(index) {
        if (typeof(bridge) == "undefined"){
            return "lamp_gray.png"
        }
        switch(bridge.sensor_status[index]) {
            case 1:
                return "lamp_green.png"
            case 2:
                return "lamp_red.png"
            case 0:
            default:
                return "lamp_gray.png"
        }
    }

    Row {
        id: sensorArea
        property var colors: ["#FFFFFF", "#000000", "#FFFFFF"]
        anchors.centerIn: parent
        spacing: 20

        Row {
            spacing: 2
            Text {
                text: "CH1"
                font.pixelSize: 12
                horizontalAlignment: Text.AlignHCenter
                color: typeof(bridge) !== "undefined" ? sensorArea.colors[bridge.theme] : "#000000"
            }
            Image {
                width: 20
                height: 20
                source: getImageFromStatus(0)
                fillMode: Image.PreserveAspectFit
            }
        }

        Row {
            spacing: 2
            Text {
                text: "CH2"
                font.pixelSize: 12
                horizontalAlignment: Text.AlignHCenter
                color: typeof(bridge) !== "undefined" ? sensorArea.colors[bridge.theme] : "#000000"
            }
            Image {
                width: 20
                height: 20
                source: getImageFromStatus(1)
                fillMode: Image.PreserveAspectFit
            }
        }

        Row {
            spacing: 2
            Text {
                text: "CH3"
                font.pixelSize: 12
                horizontalAlignment: Text.AlignHCenter
                color: typeof(bridge) !== "undefined" ? sensorArea.colors[bridge.theme] : "#000000"
            }
            Image {
                width: 20
                height: 20
                source: getImageFromStatus(2)
                fillMode: Image.PreserveAspectFit
            }
        }

        Row {
            spacing: 2
            Text {
                text: "CH4"
                font.pixelSize: 12
                horizontalAlignment: Text.AlignHCenter
                color: typeof(bridge) !== "undefined" ? sensorArea.colors[bridge.theme] : "#000000"
            }
            Image {
                width: 20
                height: 20
                source: getImageFromStatus(3)
                fillMode: Image.PreserveAspectFit
            }
        }
    }
}
