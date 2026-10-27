// © Mayanktaker Computers & Web Development | https://mayanktaker.com
// SDDM greeter for MT Verdant Nocturne

import QtQuick 2.15
import QtQuick.Controls 2.15
import SddmComponents 2.0

Rectangle {
    id: root
    width: 1920
    height: 1080
    color: "#0F141B"

    Image {
        id: bg
        anchors.fill: parent
        source: config.background || "background.png"
        fillMode: Image.PreserveAspectCrop
    }

    Rectangle {
        anchors.fill: parent
        color: "#0B0F14"
        opacity: 0.35
    }

    Column {
        anchors.centerIn: parent
        spacing: 24

        // Clock
        Text {
            id: timeText
            anchors.horizontalCenter: parent.horizontalCenter
            color: "#E9F1EC"
            font.pixelSize: 64
            font.bold: true
            text: Qt.formatTime(new Date(), "hh:mm")
        }

        // Login Card
        Rectangle {
            width: 360
            height: 220
            radius: 20
            color: "#0F141B"
            border.color: "#2C3E44"
            border.width: 1

            Column {
                anchors.centerIn: parent
                spacing: 16
                width: parent.width - 48

                TextField {
                    id: nameField
                    width: parent.width
                    height: 44
                    placeholderText: "Username"
                    color: "#E9F1EC"
                    background: Rectangle {
                        color: "#16222A"
                        radius: 10
                        border.color: nameField.activeFocus ? "#8FB8A6" : "#2C3E44"
                    }
                }

                TextField {
                    id: passwordField
                    width: parent.width
                    height: 44
                    echoMode: TextInput.Password
                    placeholderText: "Password"
                    color: "#E9F1EC"
                    background: Rectangle {
                        color: "#16222A"
                        radius: 10
                        border.color: passwordField.activeFocus ? "#8FB8A6" : "#2C3E44"
                    }
                    onAccepted: sddm.login(nameField.text, passwordField.text, sessionBox.currentIndex)
                }

                Button {
                    width: parent.width
                    height: 44
                    text: "Log In"
                    background: Rectangle {
                        color: "#8FB8A6"
                        radius: 10
                    }
                    onClicked: sddm.login(nameField.text, passwordField.text, sessionBox.currentIndex)
                }
            }
        }
    }
}
