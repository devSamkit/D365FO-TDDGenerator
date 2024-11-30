# main class for TDD generator
import sys
import TDDConstant as constants
from PyQt6.QtWidgets import *
import PyQt6.QtGui as QtGui
import TDDVariable as variables
import GenerateTDD
import ReadConfigFile
import CreateConfigFile

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(constants.TDD_GENRATOR)
        self.createConfig()

    def createConfig(self):
        qvLayout = QVBoxLayout()
        self.setLayout(qvLayout)
        self.mainLayout = QFormLayout()
        qvLayout.addLayout(self.mainLayout)
        
        # Read config file and assign values to variables
        ReadConfigFile.readConfigFile()
        
        # Create TDD Generator UI
        tabs = QTabWidget()
        tabs.addTab(self.generalTabUI(), constants.GENERAL)
        tabs.addTab(self.labelTabUI(), constants.LABEL)

        subTabs = QTabWidget()
        subTabs.addTab(self.documentTabUI(), constants.DOCUMENT)
        subTabs.addTab(self.customizationTabUI(), constants.CUSTOMIZATION)
        subFormLayout = QFormLayout()
        subFormLayout.addWidget(subTabs)
        subWidget = QWidget()
        subWidget.setLayout(subFormLayout)
        tabs.addTab(subWidget, constants.WORD_DOCUMENT)

        self.mainLayout.addWidget(tabs)
        generateTDDButton = QPushButton(constants.GENETATE_TDD)
        self.mainLayout.addWidget(generateTDDButton)
        generateTDDButton.clicked.connect(lambda:self.generateTDD())

    def labelTabUI(self):
        labelTab = QWidget()
        layout = QVBoxLayout()
        labelButton = QPushButton(constants.ADD_LABEL)
        layout.addWidget(labelButton)
        self.labelList = QListWidget()
        layout.addWidget(self.labelList)
        layout.addStretch()
        labelTab.setLayout(layout)
        labelButton.clicked.connect(lambda:self.addLabelsToList())
        self.labelList.addItem(variables.LABELS_LIST)
        return labelTab

    # File dialog box for template, labels, project
    def fileDialog(self, fileFilter: str, captionText: str):
        file = QFileDialog.getOpenFileName(self, captionText, filter=fileFilter)
        fileName: str
        
        # file may contain filter text
        if isinstance(file, tuple):
            print(file)
            fileName = file[0]
        else:
            fileName = str(file)
        return fileName

    # Folder dialog box for output path, metadata path
    def pathDialog(self, lineEdit: QLineEdit, captionText: str):
        folderPath = QFileDialog.getExistingDirectory(self, captionText)
        folderPathStr: str
        
        # path may contain filter text
        if isinstance(folderPath, tuple):
            folderPathStr = folderPath[0]
        else:
            folderPathStr = str(folderPath) 
        lineEdit.setText(folderPathStr)

    # for selecting multiple label files
    def addLabelsToList(self):
        self.labelList.addItem(self.fileDialog(constants.XML_FILE_FILTER, constants.SELECT_LABEL))

    def selectFile(self, lineEdit: QLineEdit, fileFilter: str, captionText: str):
        lineEdit.setText(self.fileDialog(fileFilter, captionText))

    def generalTabUI(self):
        Window.generalTabUI.rowCounter = 0

        def addWidgetToGridLayout(qWidget: list[QWidget]):
            column = 0
            Window.generalTabUI.rowCounter += 1
            for element in qWidget:
                column += 1
                layout.addWidget(element, Window.generalTabUI.rowCounter, column)

        def getBoldLabel(label: str):
            boldLabel = QLabel(label)
            boldLabel.setFont(boldFont)
            return boldLabel

        def paths():
            addWidgetToGridLayout([getBoldLabel(constants.PATHS)])
            # Template
            qLabel = QLabel(constants.TEMPLATE)
            self.templateEdit = QLineEdit(variables.TEMPLATE_TXT)
            templateButton = QPushButton(constants.FILE_FOLDER)
            addWidgetToGridLayout([qLabel, self.templateEdit, templateButton])
            templateButton.clicked.connect(lambda:self.selectFile(self.templateEdit, constants.DOCX_FILE_FILTER, constants.SELECT_TEMPLATE))
            # Project
            qLabel = QLabel(constants.PROJECT)
            self.projectEdit = QLineEdit(variables.PROJECT_TXT)
            projectButton = QPushButton(constants.FILE_FOLDER)
            addWidgetToGridLayout([qLabel, self.projectEdit, projectButton])
            projectButton.clicked.connect(lambda:self.selectFile(self.projectEdit, constants.VSPROJECT_FILTER, constants.SELECT_PROJECT))
            # Metadata
            qLabel = QLabel(constants.METADATA)
            self.metaDataEdit = QLineEdit(variables.METADATA_TXT)
            metaDataButton = QPushButton(constants.FILE_FOLDER)
            addWidgetToGridLayout([qLabel, self.metaDataEdit, metaDataButton])
            metaDataButton.clicked.connect(lambda:self.pathDialog(self.metaDataEdit, constants.SELECT_METADATA))
            
            # Output
            qLabel = QLabel(constants.OUTPUT)
            self.outputEdit = QLineEdit(variables.OUTPUT_TXT)
            outputButton = QPushButton(constants.FILE_FOLDER)
            addWidgetToGridLayout([qLabel, self.outputEdit, outputButton])
            outputButton.clicked.connect(lambda:self.pathDialog(self.outputEdit, constants.SELECT_OUTPUT))
            
        def package():
            addWidgetToGridLayout([getBoldLabel(constants.PACKAGES)])
            qLabel = QLabel(constants.PACKAGE)
            self.packageNameEdit = QLineEdit(variables.PACKAGE_NAME)
            addWidgetToGridLayout([qLabel, self.packageNameEdit])
            qLabel = QLabel(constants.MODEL)
            self.modelNameEdit = QLineEdit(variables.MODEL_NAME)
            addWidgetToGridLayout([qLabel, self.modelNameEdit])

        generalTab = QWidget()
        layout = QGridLayout()
        
        boldFont=QtGui.QFont()
        boldFont.setBold(True)
        paths()
        package()
        outerlayer = QVBoxLayout()
        outerlayer.addLayout(layout)
        outerlayer.addStretch()
        generalTab.setLayout(outerlayer)
        return generalTab

    def documentTabUI(self):
        Window.documentTabUI.rowCounter = 0

        # Add list of widgets in same row
        def addWidgetToGridLayout(qWidget: list[QWidget]):
            column = 0
            Window.documentTabUI.rowCounter += 1
            for element in qWidget:
                column += 1
                layout.addWidget(element, Window.documentTabUI.rowCounter, column)

        def getBoldLabel(label: str):
            boldLabel = QLabel(label)
            boldLabel.setFont(boldFont)
            return boldLabel

        def documentHeader():
            qLabel              = QLabel(constants.PREPARED_FOR)
            self.customerEdit   = QLineEdit(variables.CUST_NAME)
            addWidgetToGridLayout([qLabel, self.customerEdit])
            qLabel              = QLabel(constants.PREPARED_BY)
            self.developerEdit  = QLineEdit(variables.DEVELOPER_NAME)
            addWidgetToGridLayout([qLabel, self.developerEdit])
            qLabel              = QLabel(constants.IDD)
            self.iddEdit        = QLineEdit(variables.IDD_NAME)
            addWidgetToGridLayout([qLabel, self.iddEdit])

        def documentSection():
            addWidgetToGridLayout([getBoldLabel(constants.DOCUMENT_SECTION)])
            
            self.changeRecordCB     = QCheckBox(constants.CHANGE_RECORD)
            self.reviewerCB         = QCheckBox(constants.REVIEWER)
            addWidgetToGridLayout([self.changeRecordCB, self.reviewerCB])
            self.approverCB         = QCheckBox(constants.APPROVERS)
            self.entryAndExitCB     = QCheckBox(constants.ENTRY_EXIT)
            addWidgetToGridLayout([self.approverCB, self.entryAndExitCB])
            self.estimatesCB        = QCheckBox(constants.ESTIMATES)
            self.unitTestCB         = QCheckBox(constants.UNITTEST)
            addWidgetToGridLayout([self.estimatesCB, self.unitTestCB])
            self.performanceCB      = QCheckBox(constants.PERFORMANCE)
            self.upgradabilityCB    = QCheckBox(constants.UPGRADABILITY)
            addWidgetToGridLayout([self.performanceCB, self.upgradabilityCB])
            self.assumptionsCB      = QCheckBox(constants.ASSUMPTIONS)
            addWidgetToGridLayout([self.assumptionsCB])

            addWidgetToGridLayout([getBoldLabel(constants.OVERVIEW)])
            qLabel              = QLabel(constants.OBJECTIVE)
            self.objectiveEdit  = QLineEdit(variables.OBJECTIVE_TXT)
            addWidgetToGridLayout([qLabel, self.objectiveEdit])
            qLabel              = QLabel(constants.AUDIENCE)
            self.audienceEdit   = QLineEdit(variables.AUDIENCE_TXT)
            addWidgetToGridLayout([qLabel, self.audienceEdit])
            qLabel              = QLabel(constants.ACRONYM)
            self.acronymEdit    = QLineEdit(variables.ACRONYM_TXT)
            addWidgetToGridLayout([qLabel, self.acronymEdit])
            qLabel                  = QLabel(constants.ACRONYM_DESC)
            self.acronymDescEdit    = QLineEdit(variables.ACRONYM_DESC_TXT)
            addWidgetToGridLayout([qLabel, self.acronymDescEdit])
            qLabel              = QLabel(constants.REF_DOCUMENT)
            self.refDocEdit     = QLineEdit(variables.REF_DOCUMENT_TXT)
            addWidgetToGridLayout([qLabel, self.refDocEdit])

            qLabel              = QLabel(constants.REF_DESC)
            self.refDescEdit    = QLineEdit(variables.REF_DESC_TXT)
            addWidgetToGridLayout([qLabel, self.refDescEdit])

            qLabel              = QLabel(constants.PURPOSE_OVERVIEW)
            self.purposeEdit    = QLineEdit(variables.PURPOSE_OVERVIEW_TXT)
            addWidgetToGridLayout([qLabel, self.purposeEdit])
            
            self.changeRecordCB.setChecked(variables.CHANGE_RECORD_CHECKED)
            self.reviewerCB.setChecked(variables.REVIEWER_CHECKED)
            self.approverCB.setChecked(variables.APPROVER_CHECKED)
            self.entryAndExitCB.setChecked(variables.ENTRYANDEXIT_CHECKED)
            self.estimatesCB.setChecked(variables.ESTIMATES_CHECKED)
            self.unitTestCB.setChecked(variables.UNITTEST_CHECKED)
            self.performanceCB.setChecked(variables.PERFORMANCE_CHECKED)
            self.upgradabilityCB.setChecked(variables.UPGRADABILITY_CHECKED)
            self.assumptionsCB.setChecked(variables.ASSUMPTIONS_CHECKED)

        documentTab = QWidget()
        layout      = QGridLayout()
        boldFont    = QtGui.QFont()
        boldFont.setBold(True)
        documentHeader()
        documentSection()
        outerlayer  = QVBoxLayout()
        outerlayer.addLayout(layout)
        outerlayer.addStretch()
        
        documentTab.setLayout(outerlayer)
        return documentTab

    # Customization sub tab
    def customizationTabUI(self):
        Window.customizationTabUI.rowCounter = 0

        def addWidgetToGridLayout(qWidget: list[QWidget]):
            column = 0
            Window.customizationTabUI.rowCounter += 1
            for element in qWidget:
                column += 1
                layout.addWidget(element, Window.customizationTabUI.rowCounter, column)

        def getBoldLabel(label: str):
            boldLabel = QLabel(label)
            boldLabel.setFont(boldFont)
            return boldLabel

        def customizationHeader():
            self.codeColumn = QCheckBox(constants.CODE_COLUMN)
            addWidgetToGridLayout([self.codeColumn])
            self.codeColumn.setChecked(variables.CODE_COLUMN_CHECKED)

        def customizationStyle():
            addWidgetToGridLayout([getBoldLabel(constants.STYLE)])
            qLabel      = QLabel(constants.TABLE)
            tableEdit   = QLineEdit(variables.TABLE_TXT)
            addWidgetToGridLayout([qLabel, tableEdit])
            addWidgetToGridLayout([getBoldLabel(constants.HEADER)])
            qLabel              = QLabel(constants.HEADER_1)
            self.header1Edit    = QLineEdit(variables.HEADER_NUM_1_TXT)
            addWidgetToGridLayout([qLabel, self.header1Edit])
            qLabel              = QLabel(constants.HEADER_2)
            self.header2Edit    = QLineEdit(variables.HEADER_NUM_2_TXT)
            addWidgetToGridLayout([qLabel, self.header2Edit])
            qLabel              = QLabel(constants.HEADER_3)
            self.header3Edit    = QLineEdit(variables.HEADER_NUM_3_TXT)
            addWidgetToGridLayout([qLabel, self.header3Edit])
            qLabel              = QLabel(constants.HEADER_4)
            self.header4Edit    = QLineEdit(variables.HEADER_NUM_4_TXT)
            addWidgetToGridLayout([qLabel, self.header4Edit])
            qLabel              = QLabel(constants.HEADER_5)
            self.header5Edit    = QLineEdit(variables.HEADER_NUM_5_TXT)
            addWidgetToGridLayout([qLabel, self.header5Edit])
            qLabel              = QLabel(constants.HEADER_6)
            self.header6Edit    = QLineEdit(variables.HEADER_NUM_6_TXT)
            addWidgetToGridLayout([qLabel, self.header6Edit])

        documentTab = QWidget()
        layout      = QGridLayout()
        
        boldFont=QtGui.QFont()
        boldFont.setBold(True)
        customizationHeader()
        customizationStyle()
        outerlayer = QVBoxLayout()
        outerlayer.addLayout(layout)
        outerlayer.addStretch()
        documentTab.setLayout(outerlayer)
        return documentTab

    def generateTDD(self):
        variables.TEMPLATE_TXT      = self.templateEdit.text()
        variables.PROJECT_TXT       = self.projectEdit.text()
        variables.METADATA_TXT      = self.metaDataEdit.text()
        variables.OUTPUT_TXT        = self.outputEdit.text()
        variables.PACKAGE_NAME      = self.packageNameEdit.text()
        variables.MODEL_NAME        = self.modelNameEdit.text()
        variables.CUST_NAME         = self.customerEdit.text()
        variables.DEVELOPER_NAME    = self.developerEdit.text()
        variables.IDD_NAME          = self.iddEdit.text()
        variables.OBJECTIVE_TXT     = self.objectiveEdit.text()
        variables.AUDIENCE_TXT      = self.audienceEdit.text()
        variables.ACRONYM_TXT       = self.acronymEdit.text()
        variables.ACRONYM_DESC_TXT  = self.acronymDescEdit.text()
        variables.REF_DESC_TXT      = self.refDocEdit.text()
        variables.REF_DOCUMENT_TXT  = self.refDescEdit.text()
        variables.HEADER_NUM_1_TXT  = self.header1Edit.text()
        variables.HEADER_NUM_2_TXT  = self.header2Edit.text()
        variables.HEADER_NUM_3_TXT  = self.header3Edit.text()
        variables.HEADER_NUM_4_TXT  = self.header4Edit.text()
        variables.HEADER_NUM_5_TXT  = self.header5Edit.text()
        variables.HEADER_NUM_6_TXT  = self.header6Edit.text()
        variables.PURPOSE_OVERVIEW_TXT = self.purposeEdit.text()

        variables.CHANGE_RECORD_CHECKED = self.changeRecordCB.isChecked()
        variables.REVIEWER_CHECKED      = self.reviewerCB.isChecked()
        variables.APPROVER_CHECKED      = self.approverCB.isChecked()
        variables.ENTRYANDEXIT_CHECKED  = self.entryAndExitCB.isChecked()
        variables.ESTIMATES_CHECKED     = self.estimatesCB.isChecked()
        variables.UNITTEST_CHECKED      = self.unitTestCB.isChecked()
        variables.PERFORMANCE_CHECKED   = self.performanceCB.isChecked()
        variables.UPGRADABILITY_CHECKED = self.upgradabilityCB.isChecked()
        variables.ASSUMPTIONS_CHECKED   = self.assumptionsCB.isChecked()
        variables.CODE_COLUMN_CHECKED   = self.codeColumn.isChecked()

        variables.LABELS_LIST = [self.labelList.item(x).text() for x in range(self.labelList.count())]
        
        # Create or update config file from variables
        CreateConfigFile.startProcess()
        
        GenerateTDD.startProcess()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())