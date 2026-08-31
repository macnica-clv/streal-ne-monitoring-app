import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Effects
import QtQuick.Controls.Material

Rectangle {
    id: connectionStatus
    width: parent ? parent.width : 0
    height: parent ? parent.height : 0
    property var _appBridge3: (typeof(appBridge3) !== "undefined" && appBridge3 !== null)
                          ? appBridge3
                          : null

    property int themeIndex: _appBridge3 ? _appBridge3.theme : 0
    Material.accent: Material.Indigo

    property var colors: ["#FFFFFF", "#FFFFFF", "#2A2D35"]
    property var colors2: ["#F2F4F8", "#F2F4F8", "#393D47"]
    property var shadow: ["#EAECF5", "#DDE1E6", "#15171A"]
    property var sources: ["Icon_info_black.png", "Icon_info_black.png", "Icon_info_white.png"]
    property var text_colors: ["#343A3F", "#343A3F", "#FFFFFF"]

    color: shadow[themeIndex]

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
            id: imageIcon
            x: 12
            y: 13
            width: 27
            height: 27
            source: sources[themeIndex]
            fillMode: Image.PreserveAspectFit
        }

        Text {
            id: text1
            x: 45
            y: 17
            text: qsTr("Connection Status")
            color: text_colors[themeIndex]
            font.pixelSize: 16
            font.family:"Roboto"
        }
        Rectangle {
            id: separator
            x: 13
            y: 47
            width: 370
            height: 1
            color: "gray"
        }

        Rectangle{
            id: back
            x: 13
            y: 57
            width: 370
            height: 80
            color: colors2[themeIndex]
        }

        Text {
            id: text2
            x: 18
            y: 63
            text: qsTr("Sensor Connection Status")
            color: text_colors[themeIndex]
            font.pixelSize: 14
            font.family:"Roboto"
        }

        Text {
            id: text3
            x: 30
            y: 100
            text: typeof(bridge) !== "undefined" ? bridge.connected_board : "-"
            color:text_colors[themeIndex]
            font.pixelSize: 14
            font.family:"Roboto"
            verticalAlignment: Text.AlignVCenter
        }

        Row {
              id: sensorRow
              x: 100
              y: 85
              spacing: 40

              // CH1
              Column {
                 spacing: 2
                 Text { text: "CH1"; font.pixelSize: 12; horizontalAlignment: Text.AlignHCenter; color: text_colors[themeIndex]}
                 Image {
                    width: 20
                    height: 20
                    source: connectionStatus.getImageFromStatus(0)
                    fillMode: Image.PreserveAspectFit
                 }
              }

              // CH2
              Column {
                spacing: 2
                Text { text: "CH2"; font.pixelSize: 12; horizontalAlignment: Text.AlignHCenter; color: text_colors[themeIndex] }
                Image {
                    width: 20
                    height: 20
                    source: connectionStatus.getImageFromStatus(1)
                    fillMode: Image.PreserveAspectFit
                }
              }

              // CH3
              Column {
                spacing: 2
                Text { text: "CH3"; font.pixelSize: 12; horizontalAlignment: Text.AlignHCenter; color: text_colors[themeIndex] }
                Image {
                    width: 20
                    height: 20
                    source: connectionStatus.getImageFromStatus(2)
                    fillMode: Image.PreserveAspectFit
                }
              }

              // CH4
              Column {
                spacing: 2
                Text { text: "CH4"; font.pixelSize: 12; horizontalAlignment: Text.AlignHCenter; color: text_colors[themeIndex] }
                Image {
                    width: 20
                    height: 20
                    source: connectionStatus.getImageFromStatus(3)
                    fillMode: Image.PreserveAspectFit
                }
              }
        }

        Rectangle{
            id: back2
            x: 13
            y: 147
            width: 370
            height: 140
            color: colors2[themeIndex]
        }

        Text {
            id: text4
            x: 18
            y: 158
            text: qsTr("Connection Details")
            color: text_colors[themeIndex]
            font.pixelSize: 14
            font.family:"Roboto"
        }

        Column {
            spacing: 2
            x: 18
            y: 185
            Text {
                text: qsTr("Connection Port")
                font.pixelSize: 13
                font.family:"Roboto"
                color: "#A2A9B0"
            }
            Rectangle {
                width: 360
                height: 1
                color: "#A2A9B0"
            }
        }

        Text {
            id: text7
            x: 150
            y: 185
            text: typeof(bridge) !== "undefined" ? bridge.connected_port : "-"
            color: text_colors[themeIndex]
            font.pixelSize: 13
            font.family:"Roboto"
        }

        Column {
            spacing: 2
            x: 18
            y: 222
            Text {
                text: qsTr("Sensor ID")
                font.pixelSize: 13
                font.family:"Roboto"
                color: "#A2A9B0"
            }
            Rectangle {
                width: 360
                height: 1
                color: "#A2A9B0"
            }
        }

        Text {
            id: text9
            x: 150
            y: 222
            text: typeof(bridge) !== "undefined" ? bridge.sensor_ids : "-"
            color: text_colors[themeIndex]
            font.pixelSize: 13
            font.family:"Roboto"
        }

        Column {
            spacing: 2
            x: 18
            y: 260
            Text {
                text: qsTr("FW Version")
                font.pixelSize: 13
                font.family:"Roboto"
                color: "#A2A9B0"
            }
            Rectangle {
                width: 360
                height: 1
                color: "#A2A9B0"
            }
        }

        Text {
            id: text10
            x: 150
            y: 260
            text: typeof(bridge) !== "undefined" ? bridge.board_version : "-"
            color: text_colors[themeIndex]
            font.pixelSize: 13
            font.family:"Roboto"
        }
    }
}