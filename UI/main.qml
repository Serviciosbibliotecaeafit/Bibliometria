import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ApplicationWindow{
    visible: true
    width: 900
    height: 800
    title: "Bibliometría"

    property int unit: 20

    property real progressValue: 50.0

    property string inputFile
    property string outputFolder
    property string dataBase
    property string email
    property string password

    property bool bInputFile: false
    property bool bOutputFolder: false
    property bool bDataBase: false
    property bool bEmail: false
    property bool bPassword: false
    property bool bFinishedSearch: false

    Rectangle {
        id: main_rect
        anchors.fill: parent
        color: "#c0c0c0"

        Image {
            sourceSize.width: parent.width/10
            sourceSize.height: parent.height/10
            source: "./images/EafitLogo.png"
            fillMode: Image.PreserveAspectCrop
            anchors {
                bottom: parent.bottom
                bottomMargin: 12
                right: parent.right
                rightMargin: 12
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    window.webpage()
                }
            }
        }

        Text {
            id:title
            text: "Obtención y Normalización"
            font.pixelSize: 36
            font.bold: true
            color: "black"
            anchors {
                bottom: sec_rect.top
                margins: unit/2
                horizontalCenter: sec_rect.horizontalCenter
            }
        }

        Text {
            text: "Versión: 0.1.0"
            font.italic: true
            font.pixelSize: 12
            anchors {
                bottom: parent.bottom
                left: parent.left
                margins: unit/2
            }
        }

        Rectangle {
            id: sec_rect
            implicitWidth: parent.width - 5*unit
            implicitHeight: parent.height - 10*unit
            anchors.centerIn: parent
            border.color: "#00001c"
            border.width: 1

            Column {
                id: columnLeft
                spacing: unit/2
                width: 20*unit

                anchors {
                    left: parent.left
                    top: parent.top
                    margins: unit
                }

                Text { 
                    text: "Base de Datos"
                    font.pixelSize: 18
                    font.italic: true
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                ComboBox {
                    id: dataBaseSelector
                    implicitHeight: 1.5*unit
                    implicitWidth: 10*unit
                    font.pixelSize: 18
                    onActivated: {
                        dataBase = currentValue
                        bDataBase = true
                    }
                    model: ["Seleccionar", "SCOPUS"]
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Item {
                    width: 1
                    height: unit
                }

                Text { 
                    text: "Archivo de Entradas"
                    font.pixelSize: 18
                    font.italic: true
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Button {
                    id: fn
                    implicitHeight: 1.5*unit
                    implicitWidth: 10*unit
                    text: "Seleccionar"
                    font.pixelSize: 18
                    onClicked: f_dialog.open()
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Item {
                    width: 1
                    height: unit
                }

                Text { 
                    text: "Credenciales"
                    font.pixelSize: 18
                    font.italic: true
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Rectangle {
                    width: unit
                    height: 2*unit
                    anchors.horizontalCenter: parent.horizontalCenter

                    Text {
                        id: emailText
                        text: "Correo"
                        font.pixelSize: 18
                        anchors {
                            right: emailBox.left
                            rightMargin: unit
                            verticalCenter: emailBox.verticalCenter
                        }
                    }

                    TextField {
                        id: emailBox
                        placeholderText: "usuario@eafit.edu.co"
                        font.pixelSize: 18
                        implicitWidth: 10*unit
                        onTextChanged: {
                            email = text
                            bEmail = true
                        }
                        anchors {
                            horizontalCenter: parent.horizontalCenter
                            top: parent.top
                        }
                    }

                    Text {
                        text: "Contraseña"
                        font.pixelSize: 18
                        anchors {
                            right: emailText.right
                            verticalCenter: passBox.verticalCenter
                        }
                    }

                    TextField {
                        id: passBox
                        placeholderText: "****************"
                        font.pixelSize: 18
                        implicitWidth: 10*unit
                        onTextChanged: {
                            password = text
                            bPassword = true
                        }
                        echoMode: TextInput.Password
                        anchors {
                            left: emailBox.left
                            top: emailBox.bottom
                            topMargin: unit/2
                        }
                    }
                }

                Item {
                    width: 1
                    height: 2*unit
                }

                Text { 
                    text: "Carpeta de Salida"
                    font.pixelSize: 18
                    font.italic: true
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Button {
                    id: fold_button
                    implicitHeight: 1.5*unit
                    implicitWidth: 10*unit
                    text: "Seleccionar"
                    font.pixelSize: 18
                    onClicked: folder_dialog.open()
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Item {
                    width: 1
                    height: unit
                }

                Button {
                    id: runButton
                    text: "Obtener Datos"
                    font.pixelSize: 18

                    enabled: {
                        if (bDataBase && bInputFile && bOutputFolder && bEmail && bPassword) return true
                        else return false
                    }
                    
                    onClicked: {
                        window.main_process(inputFile, dataBase, outputFolder, email, password)
                        runButton.enabled = false
                        progressBar.visible = true
                    }

                    anchors.horizontalCenter: parent.horizontalCenter
                }

                ProgressBar{
                    id: progressBar
                    from: 0
                    to: 100
                    value: progressValue
                    visible: false
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Button {
                    id: exportButton
                    text: "Exportar"
                    visible: false
                    font.pixelSize: 18
                    onClicked: {
                        window.export()
                    }
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }

            Rectangle {
                border.color: "#00001c"
                border.width: unit
                anchors {
                    left: columnLeft.right
                    right: parent.right
                    top: parent.top
                    bottom: parent.bottom
                    margins: unit
                }

                ScrollView {
                    anchors.fill: parent
                    clip: true

                    TextEdit {
                        id: logLabel
                        text: "Registro"
                        readOnly: true
                        selectByMouse: true
                        wrapMode: Text.WordWrap
                        font.pixelSize: 15
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
            }

            Button {
                id: exportBackup
                text: "Exportar Backup"
                font.pixelSize: 12

                enabled: {
                    if (bDataBase && bOutputFolder) return true
                    else return false
                }

                onClicked: {
                    window.exportBackup(dataBase, outputFolder)
                }

                anchors {
                    left: parent.left
                    bottom: parent.bottom
                    margins: unit
                }
            }
        }
    }

    Connections {
        target: window

        function onUpdated(msg) {
            logLabel.text = msg
        }

        function onProgress(msg) {
            progressValue = msg
        }

        function onFinishedSearching(msg) {
            exportButton.visible = msg
            progressBar.visible = !msg
        }

    }

    FileDialog {
        id: f_dialog
        nameFilters: ["Text files(*.txt)"]
        onAccepted: {
            inputFile = f_dialog.currentFile
            bInputFile = true
            fn.text = inputFile.split("/").reverse()[0]
        }
    }

    FolderDialog {
        id: folder_dialog
        onAccepted: {
            outputFolder = folder_dialog.currentFolder
            bOutputFolder = true
            fold_button.text = outputFolder.split("/").reverse()[0]
        }
    }
}