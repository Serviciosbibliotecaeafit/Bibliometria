import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

/*
    UI basica en formato qml (en un futuro tal vez serio mejor usar html y css para ser compatible en web)

    Update Notes:
    - v0.1.0: Se aplico un diseño basico con los siguientes componentes:
        * Titulo
        * Logo EAFIT (con direccionamiento a la website de la universidad)
        * Implementacion basica de inputs (archivo de entrada, directorio de salida, credenciales y base de datos)
        * Registro de actividad de Selenium
        * Barra de progreso
        * Boton de exportacion de backup (supone que existe un backup !posibles bugs!)
    
    La paleta de colores seleccionada no tiene sentido ya que se priorizo uso sobre estetica (MODIFICAR)
*/

ApplicationWindow{
    visible: true
    width: 900
    height: 800
    title: "Bibliometría"

    property int unit: 20 // Unidad de separacion de los bloques (REVISAR)

    property real progressValue: 50.0 // La inicializacion no importa ya que la barra no es visible hasta iniciar

    // INPUTS
    property string inputFile // URLS
    property string outputFolder // Directorio
    property string dataBase // Base de datos
        // Credenciales
    property string email
    property string password

    // Boolean Inputs (para activar el boton de obtencion)
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
            // Logo de EAFIT
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
                    window.webpage() // Direcciona a la webpage de la universidad
                }
            }
        }

        Text {
            id:title
            text: "Obtención y Normalización" // Titulo sujeto a cambios
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
            // Version
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
                    model: ["Seleccionar", "SCOPUS", "LENS"] // Futuras bases de datos: ["LENS", "SCIELO", "WOS", "DIMENSIONS"]
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
                    // InputFile
                    id: fn
                    implicitHeight: 1.5*unit
                    implicitWidth: 10*unit
                    text: "Seleccionar"
                    font.pixelSize: 18
                    onClicked: f_dialog.open() // Abre ventana del OS para seleccionar el archivo
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
                        echoMode: showPassword.checked ? TextInput.Normal : TextInput.Password // Cambiar el echoMode al hacer clic en el CheckBox
                        anchors {
                            left: emailBox.left
                            top: emailBox.bottom
                            topMargin: unit/2
                        }
                    }

                    CheckBox {
                        id: showPassword
                        text: "Mostrar"
                        anchors {
                            left: passBox.right
                            leftMargin: unit
                            verticalCenter: passBox.verticalCenter
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
                    // Directorio de salida
                    id: fold_button
                    implicitHeight: 1.5*unit
                    implicitWidth: 10*unit
                    text: "Seleccionar"
                    font.pixelSize: 18
                    onClicked: folder_dialog.open() // Abre ventana del OS para seleccionar la carpeta de salida
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
                        // Obliga a llenar todos los inputs
                        if (bDataBase && bInputFile && bOutputFolder && bEmail && bPassword) return true
                        else return false
                    }
                    
                    onClicked: {
                        // Proceso principal de obtencion de datos
                        window.main_process(inputFile, dataBase, outputFolder, email, password)
                        runButton.enabled = false // Desactiva el boton para evitar bugs
                        progressBar.visible = true // activamos la barra de progreso
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
                    // exportar obtenidos
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
                // Registro de actividad
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
                        text: "Registro" // No muestra este texto PRIORIDAD: BAJA
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
                    // Solo algunos inputs son necesarios (puede ocurrir el error de que la base de datos no corresponda al backup REVISAR) PRIORIDAD: MEDIA
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
        // Señales de PyQt6

        function onUpdated(msg) {
            logLabel.text = msg // Registro de actividad
        }

        function onProgress(msg) {
            progressValue = msg // Registro de progreso
        }

        function onFinishedSearching(msg) {
            // Registro de finalizacion
            exportButton.visible = msg
            progressBar.visible = !msg
        }

    }

    FileDialog {
        // Seleccion de inputFile
        id: f_dialog
        nameFilters: ["Text files(*.txt)"]
        onAccepted: {
            inputFile = f_dialog.currentFile
            bInputFile = true
            fn.text = inputFile.split("/").reverse()[0] // Se muestra solo el nombre del archivo
        }
    }

    FolderDialog {
        // Seleccion de outputFolder
        id: folder_dialog
        onAccepted: {
            outputFolder = folder_dialog.currentFolder
            bOutputFolder = true
            fold_button.text = outputFolder.split("/").reverse()[0] // Se muestra solo el nombre del directorio
        }
    }
}