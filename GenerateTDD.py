import xml.etree.ElementTree as ET
import os
import CreateDocxFile
import os.path
import ParseElementXML as parseElement
import TDDConstant as constants
import CreateDocxFile
import TDDVariable as variables
from datetime import date

def initDocument():
    CreateDocxFile.initDocument(variables.TEMPLATE_TXT)
    CreateDocxFile.addHeading(variables.IDD_NAME, constants.HEADER1)
    CreateDocxFile.addLineBreak()
    CreateDocxFile.addParagraph_italic(constants.PREPARED_FOR, variables.CUST_NAME)
    CreateDocxFile.addParagraph_italic(constants.PREPARED_BY, variables.DEVELOPER_NAME)
    CreateDocxFile.addPageBreak()

def addDocumentSection(projectDict):
    if(variables.CHANGE_RECORD_CHECKED == True or variables.REVIEWER_CHECKED == True or variables.APPROVER_CHECKED == True):
        addRevision()
        CreateDocxFile.addPageBreak()
        
    addOverview()
    CreateDocxFile.addPageBreak()
    
    if(variables.ENTRYANDEXIT_CHECKED == True):
        addEntryNExit()
        CreateDocxFile.addPageBreak()
        
    if(variables.ESTIMATES_CHECKED == True):
        addEstimates()
        CreateDocxFile.addPageBreak()
        
    addCustomization(projectDict)
    CreateDocxFile.addPageBreak()
    
    if(variables.UNITTEST_CHECKED == True):
        addUnitTest()
        CreateDocxFile.addPageBreak()
        
    if(variables.PERFORMANCE_CHECKED == True):
        addPerformance()
        CreateDocxFile.addPageBreak()
        
    if(variables.UPGRADABILITY_CHECKED == True):
        addUpgradability()
        CreateDocxFile.addPageBreak()
        
    if(variables.ASSUMPTIONS_CHECKED == True):
        addAssumption()

def addRevision():
    def changeRecord():
        recordDict = {0: [constants.DATE, constants.AUTHOR, constants.VERSION, constants.CHANGEREF]}
        recordDict[1] = [variables.TODAY, variables.DEVELOPER_NAME, constants.CURVERSION, constants.BLANK]
        return recordDict

    def reviewers(approver = False):
        if(approver == True):
            version = constants.VERSIONAPPROVED
        else:
            version = constants.VERSIONREVIEWED
        reviewerDict = {0: [constants.NAME, version, constants.POSITION, constants.DATE]}
        reviewerDict[1] = [constants.BLANK, constants.BLANK, constants.BLANK, constants.BLANK]
        return reviewerDict

    def addHeadingTableLineBreak(heading, tableDict):
        CreateDocxFile.addHeading(heading, constants.HEADER2)
        CreateDocxFile.addTable(tableDict)
        CreateDocxFile.addLineBreak()

    CreateDocxFile.addHeading(constants.REVISION, constants.HEADER1)
    if(variables.CHANGE_RECORD_CHECKED == True):
        addHeadingTableLineBreak(constants.CHANGE_RECORD, changeRecord())
    if(variables.REVIEWER_CHECKED == True):
        addHeadingTableLineBreak(constants.REVIEWERS, reviewers())
    if(variables.APPROVER_CHECKED == True):
        addHeadingTableLineBreak(constants.APPROVERS, reviewers(True))

def addOverview():
    def acronyms():
        acronymsDict = {0: [constants.ACRONYMTERM , constants.DESCRIPTION]}
        acronymsDict[1] = [variables.ACRONYM_TXT, variables.ACRONYM_DESC_TXT]
        return acronymsDict

    def references():
        referenceDict = {0: [constants.DOCUMENTURL, constants.BRIEFDESCRIPTION]}
        referenceDict[1] = [variables.REF_DOCUMENT_TXT, variables.REF_DESC_TXT]
        return referenceDict

    CreateDocxFile.addHeading_num(constants.OVERVIEW, variables.HEADER_NUM_1_TXT)
    CreateDocxFile.addHeading_num(constants.OBJECTIVE, variables.HEADER_NUM_2_TXT)
    CreateDocxFile.addParagraph(variables.OBJECTIVE_TXT)
    CreateDocxFile.addHeading_num(constants.AUDIENCE, variables.HEADER_NUM_2_TXT)
    CreateDocxFile.addParagraph(variables.AUDIENCE_TXT)
    CreateDocxFile.addHeading_num(constants.ACRONYMS, variables.HEADER_NUM_2_TXT)
    CreateDocxFile.addTable(acronyms())
    CreateDocxFile.addHeading_num(constants.REFERENCES, variables.HEADER_NUM_2_TXT)
    CreateDocxFile.addTable(references())
    CreateDocxFile.addHeading_num(constants.PURPOSE_OVERVIEW, variables.HEADER_NUM_2_TXT)
    CreateDocxFile.addParagraph(variables.PURPOSE_OVERVIEW_TXT)
    CreateDocxFile.addHeading_num(constants.REQUIREMENT_OVERVIEW, variables.HEADER_NUM_3_TXT)
    CreateDocxFile.addHeading_num(constants.SOLUTION_OVERVIEW, variables.HEADER_NUM_3_TXT)

def addEntryNExit():
    def entryChecklist():
        entryDict = {0: [constants.CRITERIA, constants.OWNER, constants.COMPLETED]}
        
        entryDict[1] = [constants.FDD_CRITERIA, constants.APP_CONSULTANT, constants.YES]
        entryDict[2] = [constants.CUST_REVIEW_CRITERIA, constants.APP_CONSULTANT, constants.YES]
        entryDict[3] = [constants.HIGH_LEVEL_CRITERIA, constants.DEV_CONSULTANT, constants.YES]
        entryDict[4] = [constants.SECURITY_MATRIX_CRITERIA, constants.APP_CONSULTANT, constants.YES]
        entryDict[5] = [constants.TDD_PREP_CRITERIA, constants.DEV_CONSULTANT, constants.YES]
        entryDict[6] = [constants.DEPENDENCY_CRITERIA, constants.APP_CONSULTANT, constants.YES]
        entryDict[7] = [constants.TEST_CASE_CRITERIA, constants.APP_CONSULTANT, constants.YES]
        entryDict[8] = [constants.WALKTHROUGH_CRITERIA, constants.APP_CONSULTANT, constants.YES]
        return entryDict

    def exitChecklist():
        exitDict = {0: [constants.CRITERIA, constants.OWNER, constants.COMPLETED]}
        exitDict[1] = [constants.TDDREVIEWANDSIGNED, constants.DEV_CONSULT_LEAD, constants.YES]
        exitDict[2] = [constants.TRACEABIILITY, constants.DEV_CONSULT, constants.YES]
        exitDict[3] = [constants.REVIEWTRACE, constants.APP_CONSULT_DEV_CONSULT, constants.YES]
        return exitDict

    CreateDocxFile.addHeading_num(constants.ENTRY_EXIT_CRIT, variables.HEADER_NUM_1_TXT)
    CreateDocxFile.addHeading_num(constants.ENTRY_CRITERIA, variables.HEADER_NUM_2_TXT)
    CreateDocxFile.addTable(entryChecklist())
    CreateDocxFile.addHeading_num(constants.EXIT_CRITERIA, variables.HEADER_NUM_2_TXT)
    CreateDocxFile.addTable(exitChecklist())

def addEstimates():
    CreateDocxFile.addHeading_num(constants.ESTIMATES, variables.HEADER_NUM_1_TXT)
    CreateDocxFile.addTable(createDictFromListWithBlankRows(constants.estimateList, constants.BLANK_ROWS))

def addUnitTest():
    CreateDocxFile.addHeading_num(constants.UNIT_TEST, variables.HEADER_NUM_1_TXT)
    CreateDocxFile.addTable(createDictFromListWithBlankRows(constants.unitTestList, constants.BLANK_ROWS))

def addPerformance():
    CreateDocxFile.addHeading_num(constants.PERFORMANCE, variables.HEADER_NUM_1_TXT)

def addUpgradability():
    CreateDocxFile.addHeading_num(constants.UPGRADABILITY, variables.HEADER_NUM_1_TXT)

def addAssumption():
    CreateDocxFile.addHeading_num(constants.ASSUMPTIONS, variables.HEADER_NUM_1_TXT)
    CreateDocxFile.addTable(createDictFromListWithBlankRows(constants.assumptionList, constants.BLANK_ROWS))
        
def createDictFromListWithBlankRows(tableList, rows):
    listLength = len(tableList)
    counter = 0
    newList = []
    for x in range(listLength):
        newList.append(constants.BLANK)
    tableDict = {counter: tableList}
    while counter < rows:
        counter += 1
        newList
        tableDict[counter] = newList
    return tableDict

def addCustomization(projectDict):
    CreateDocxFile.addHeading_num(constants.CUSTOMIZATION, variables.HEADER_NUM_1_TXT)
    elementDict = projectDict

    def dataType():
        dataTypeList = constants.dataTypes
        isTrue = False
        for element in dataTypeList:
            if element in elementDict.keys():
                if(isTrue == False):
                    isTrue = True
                    CreateDocxFile.addHeading_num(constants.DATA_TYPES, variables.HEADER_NUM_2_TXT)
                addFromXML_dataType(element, elementDict.pop(element))
    
    def dataModel():
        dataModelList = constants.dataModels
        isTrue = False
        for element in dataModelList:
            if element in elementDict.keys():
                if(isTrue == False):
                    isTrue = True
                    CreateDocxFile.addHeading_num(constants.DATA_MODEL, variables.HEADER_NUM_2_TXT)
                addFromXML_dataModels(element, elementDict.pop(element))

    def code():
        codeList = constants.code
        isTrue = False
        for element in codeList:
            if element in elementDict.keys():
                if(isTrue == False):
                    isTrue = True
                    CreateDocxFile.addHeading_num(constants.CODE, variables.HEADER_NUM_2_TXT)
                addFromXML_code(element, elementDict.pop(element)) 
                
    def ui():
        uiList = constants.userInterFace
        isTrue = False
        isMenuItem = False
        isMenuItemExt = False
        for element in uiList:
            if element in elementDict.keys():
                if(isTrue == False):
                    isTrue = True
                    CreateDocxFile.addHeading_num(constants.USER_INTERFACE, variables.HEADER_NUM_2_TXT)
                if(isMenuItem == False and (element in constants.menuItem)):
                    isMenuItem = True
                    addFromXML_UI(element, elementDict.pop(element), True)
                elif(isMenuItemExt == False and (element in constants.menuItemExt)):
                    isMenuItemExt = True
                    addFromXML_UI(element, elementDict.pop(element), menuItemExt=True)
                else:
                    addFromXML_UI(element, elementDict.pop(element)) 
    
    def analytics():
        analyticsList = constants.analytics
        isTrue = False
        isPerspective = False
        for element in analyticsList:
            if element in elementDict.keys():
                if(isTrue == False):
                    isTrue = True
                    CreateDocxFile.addHeading_num(constants.ANALYTICS, variables.HEADER_NUM_2_TXT)
                if(isPerspective == False and (element in constants.perspective)):
                    isPerspective = True
                    addFromXML_analytics(element, elementDict.pop(element), True)
                else:
                    addFromXML_analytics(element, elementDict.pop(element)) 
        
    def report():
        reportList = constants.report
        isTrue = False
        isReportStyle = False
        for element in reportList:
            if element in elementDict.keys():
                if(isTrue == False):
                    isTrue = True
                    CreateDocxFile.addHeading_num(constants.REPORTS, variables.HEADER_NUM_2_TXT)
                if(isReportStyle == False and (element in constants.reportStyle)):
                    isReportStyle = True
                    addFromXML_report(element, elementDict.pop(element), True)
                else:
                    addFromXML_report(element, elementDict.pop(element)) 

    def workFlow():
        workFlowList = constants.workFlow
        isTrue = False
        isProvider = False
        for element in workFlowList:
            if element in elementDict.keys():
                if(isTrue == False):
                    isTrue = True
                    CreateDocxFile.addHeading_num(constants.BUSINESS_PROCESS_WF, variables.HEADER_NUM_2_TXT)
                if(isProvider == False and (element in constants.wfProvider)):
                    isProvider = True
                    addFromXML_workFlow(element, elementDict.pop(element), True)
                else:
                    addFromXML_workFlow(element, elementDict.pop(element)) 

    dataType()
    dataModel()
    code()
    ui()
    analytics()
    report()
    workFlow()

def addTableElement(objectType, objectName, methodName):
    tableDict = parseObjectXML(objectType, objectName, methodName)
    CreateDocxFile.addTable(tableDict)

def addFromXML_dataType(elementName, elementList):
    if(elementName == constants.AXENUM):
        CreateDocxFile.addHeading_num(constants.ENUM, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.PROPERTY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_property')
            CreateDocxFile.addHeading_num(constants.ENUMERATION, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseEnum_value')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXENUMEXT):
        CreateDocxFile.addHeading_num(constants.ENUMEXT, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseEnumExt')
        CreateDocxFile.addLineBreak()
    
    if(elementName == constants.AXEDT):
        CreateDocxFile.addHeading_num(constants.EDT, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseElement_property')
        CreateDocxFile.addLineBreak()
    
    if(elementName == constants.AXEDTEXT):
        CreateDocxFile.addHeading_num(constants.EDTEXT, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseEDTExt')
        CreateDocxFile.addLineBreak()

def addFromXML_dataModels(elementName, elementList):
    if(elementName == constants.AXTABLE):
        CreateDocxFile.addHeading_num(constants.TABLE, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.PROPERTY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_property')
            CreateDocxFile.addHeading_num(constants.FIELD, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseTable_field')
            CreateDocxFile.addHeading_num(constants.FIELD_GROUP, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseTable_fieldGroup')
            CreateDocxFile.addHeading_num(constants.INDEX, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseTable_index')
            CreateDocxFile.addHeading_num(constants.RELATION, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseTable_relation')
            CreateDocxFile.addHeading_num(constants.METHOD, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_method')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXTABLEEXT):
        CreateDocxFile.addHeading_num(constants.TABLEEXT, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.PROPERTY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseTableExt_modifiedDict')
            CreateDocxFile.addHeading_num(constants.FIELD, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseTable_field')
            CreateDocxFile.addHeading_num(constants.FIELD_GROUP, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseTable_fieldGroup')
            CreateDocxFile.addHeading_num(constants.INDEX, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseTable_index')
            CreateDocxFile.addHeading_num(constants.RELATION, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseTable_relation')
        CreateDocxFile.addLineBreak()
    
    if(elementName == constants.AXVIEW):
        CreateDocxFile.addHeading_num(constants.VIEW, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.PROPERTY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_property')
            CreateDocxFile.addHeading_num(constants.DATASOURCE, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseViewNQuery_DS')
            CreateDocxFile.addHeading_num(constants.FIELD, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseView_field')
            CreateDocxFile.addHeading_num(constants.FIELD_GROUP, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseTable_fieldGroup')
            CreateDocxFile.addHeading_num(constants.METHOD, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_method')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXVIEWEXT):
        CreateDocxFile.addHeading_num(constants.VIEWEXT, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.DATASOURCE, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseQueryNViewExt_ds')
            CreateDocxFile.addHeading_num(constants.FIELD, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseView_field')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXQUERY):
        CreateDocxFile.addHeading_num(constants.QUERY, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.DATASOURCE, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseViewNQuery_DS')
            CreateDocxFile.addHeading_num(constants.GROUP_BY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseQuery_groupBy')
            CreateDocxFile.addHeading_num(constants.ORDER_BY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseQuery_orderBy')
        CreateDocxFile.addLineBreak()
        
    if(elementName == constants.AXQUERYEXT):
        CreateDocxFile.addHeading_num(constants.QUERYEXT, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.DATASOURCE, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseQueryNViewExt_ds')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXDATAENTITY):
        CreateDocxFile.addHeading_num(constants.DATAENTITY, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.PROPERTY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_property')
            CreateDocxFile.addHeading_num(constants.FIELD, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseEntity_field')
            CreateDocxFile.addHeading_num(constants.KEY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseEntity_key')
            CreateDocxFile.addHeading_num(constants.METHOD, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_method')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXDATAENTITYEXT):
        CreateDocxFile.addHeading_num(constants.DATAENTITYEXT, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.FIELD, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseEntityExt_field')
        CreateDocxFile.addLineBreak()
    
    if(elementName == constants.AXCOMPOSITEENTITY):
        CreateDocxFile.addLineBreak()
        CreateDocxFile.addHeading_num(constants.COMPOSITEENTITY, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'compositeEntity')

    if(elementName == constants.AXAGGREGATEDATAENTITY):
        CreateDocxFile.addHeading_num(constants.AGGREGATEDATAENTITY, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.PROPERTY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_property')
            CreateDocxFile.addHeading_num(constants.MEASUREMENT, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseAggEntity_measure')
            CreateDocxFile.addHeading_num(constants.FIELD, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseAggEntity_field')
            CreateDocxFile.addHeading_num(constants.FIELD_GROUP, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseTable_fieldGroup')
            CreateDocxFile.addHeading_num(constants.KEY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseEntity_key')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXMAP):
        CreateDocxFile.addHeading_num(constants.MAP, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.PROPERTY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_property')
            CreateDocxFile.addHeading_num(constants.FIELD, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseMap_field')
            CreateDocxFile.addHeading_num(constants.METHOD, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_method')
            # TODO: Mappings
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXTABLECOLLECTION):
        CreateDocxFile.addHeading_num(constants.TABLECOLLECTION, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseTableColl')
        CreateDocxFile.addLineBreak()

def addFromXML_code(elementName, elementList):
    if(elementName == constants.AXCLASS):
        CreateDocxFile.addHeading_num(constants.CLASS, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseElement_method')
        CreateDocxFile.addLineBreak()
    # TODO: Macro

def addFromXML_UI(elementName, elementList, menuItem = False, menuItemExt = False):
    if(elementName == constants.AXFORM):
        CreateDocxFile.addHeading_num(constants.FORM, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.DESIGN_PROPERTY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseForm_design')
            CreateDocxFile.addHeading_num(constants.DATASOURCE, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseForm_datasource')
            CreateDocxFile.addHeading_num(constants.METHOD, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_method')
            # TODO: Form methods with Parent
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXFORMEXT):
        CreateDocxFile.addHeading_num(constants.FORMEXT, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseFormExt')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXTILE):
        CreateDocxFile.addHeading_num(constants.TILE, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseElement_property')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXMENU):
        CreateDocxFile.addHeading_num(constants.MENU, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseMenu')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXMENUEXT):
        CreateDocxFile.addHeading_num(constants.MENUEXT, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseMenuExt')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXMENUITEMDISPLAY):
        if(menuItem == True):
            CreateDocxFile.addHeading_num(constants.MENU_ITEMS, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.DISPLAY,  variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseMenuItem')
        CreateDocxFile.addLineBreak()
        
    if(elementName == constants.AXMENUITEMACTION):
        if(menuItem == True):
            CreateDocxFile.addHeading_num(constants.MENU_ITEMS, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.ACTION, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseMenuItem')
        CreateDocxFile.addLineBreak()
    
    if(elementName == constants.AXMENUITEMOUTPUT):
        if(menuItem == True):
            CreateDocxFile.addHeading_num(constants.MENU_ITEMS, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.OUTPUT, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseMenuItem')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXMENUITEMDISPLAYEXT):
        if(menuItemExt == True):
            CreateDocxFile.addHeading_num(constants.MENU_ITEMEXT, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.DISPLAYEXT, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseMenuItemExt')
        CreateDocxFile.addLineBreak()
        
    if(elementName == constants.AXMENUITEMOUTPUTEXT):
        if(menuItemExt == True):
            CreateDocxFile.addHeading_num(constants.MENU_ITEMEXT, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.OUTPUTEXT, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseMenuItemExt')
        CreateDocxFile.addLineBreak()
    
    if(elementName == constants.AXMENUITEMACTIONEXT):
        if(menuItemExt == True):
            CreateDocxFile.addHeading_num(constants.MENU_ITEMEXT, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.ACTIONEXT, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseMenuItemExt')
        CreateDocxFile.addLineBreak()

def addFromXML_analytics(elementName, elementList, perspective = False):
    if(elementName == constants.AXAGGREGATEDIMENSION):
        if(perspective == True):
            CreateDocxFile.addHeading_num(constants.PERSPECTIVES, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.AGGREGATEDIMENSION, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.PROPERTY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_property')
            CreateDocxFile.addHeading_num(constants.ATTRIBUTE, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseAggDim_attribute')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXAGGREGATEMEASUREMENT):
        if(perspective == True):
            CreateDocxFile.addHeading_num(constants.PERSPECTIVES, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.AGGREGATEMEASUREMENT, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.PROPERTY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_property')
            # TODO: check standard FMTAggregateMeasurement
        CreateDocxFile.addLineBreak()
    
    if(elementName == constants.AXAGGCALCMEASURETEMPLATE):
        if(perspective == True):
            CreateDocxFile.addHeading_num(constants.PERSPECTIVES, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.CALC_MEASURE_TEMPLATE, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            # TODO: parse methods
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXAGGCALCMEASURETEMPLATEPERIOD):
        if(perspective == True):
            CreateDocxFile.addHeading_num(constants.PERSPECTIVES, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.CALC_MEASURE_PERIOD_TEMPLATE, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            # TODO: parse methods
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXKPI):
        CreateDocxFile.addHeading_num(constants.KPI, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            # TODO: parse methods
        CreateDocxFile.addLineBreak()

def addFromXML_report(elementName, elementList, reportStyle = False):
    if(elementName == constants.AXREPORT):
        CreateDocxFile.addHeading_num(constants.REPORT, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.DATASET, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseReport_dataSet')
            # TODO: Default Parameters ?
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXREPORTLAYOUTTEMPLATE):
        if(reportStyle == True):
            CreateDocxFile.addHeading_num(constants.REPORT_STYLE_TEMPLATE, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.LAYOUT_TEMPLATE, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            # TODO: If required parse
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXREPORTLISTSTYLETEMPLATE):
        if(reportStyle == True):
            CreateDocxFile.addHeading_num(constants.REPORT_STYLE_TEMPLATE, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.LIST_STYLE_TEMPLATE, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            # TODO: If required parse
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXMATRIXSTYLETEMPLATE):
        if(reportStyle == True):
            CreateDocxFile.addHeading_num(constants.REPORT_STYLE_TEMPLATE, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.MATRIX_STYLE_TEMPLATE, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            # TODO: If required parse
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXTPIECHARTSTYLETEMPLATE):
        if(reportStyle == True):
            CreateDocxFile.addHeading_num(constants.REPORT_STYLE_TEMPLATE, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.PIE_CHART_TEMPLATE, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            # TODO: If required parse
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXTABLESTYLETEMPLATE):
        if(reportStyle == True):
            CreateDocxFile.addHeading_num(constants.REPORT_STYLE_TEMPLATE, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.TABLE_STYLE_TEMPLATE, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            # TODO: If required parse
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXXYCHARTSTYLETEMPLATE):
        if(reportStyle == True):
            CreateDocxFile.addHeading_num(constants.REPORT_STYLE_TEMPLATE, variables.HEADER_NUM_3_TXT)
        CreateDocxFile.addHeading_num(constants.XY_CHART_STYLE_TEMPLATES, variables.HEADER_NUM_4_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            # TODO: If required parse
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXREPORTEXTERNALDS):
        CreateDocxFile.addHeading_num(constants.REPORT_DATASOURCE, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            # TODO: If required parse
        CreateDocxFile.addLineBreak()
    
    if(elementName == constants.AXREPORTEMBEDDEDIMAGE):
        CreateDocxFile.addHeading_num(constants.REPORT_IMAGES, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            # TODO: If required parse
        CreateDocxFile.addLineBreak()

def addFromXML_workFlow(elementName, elementList, reportStyle = False):
    if(elementName == constants.AXWORKFLOWCATEGORY):
        CreateDocxFile.addHeading_num(constants.WORKFLOWCATEGORY, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            addTableElement(elementName, element, 'parseElement_property')
        CreateDocxFile.addLineBreak()

    if(elementName == constants.AXWORKFLOWAPPROVAL):
        CreateDocxFile.addHeading_num(constants.WORKFLOWAPPROVAL, variables.HEADER_NUM_3_TXT)
        for element in elementList:
            CreateDocxFile.addHeading_num(element, variables.HEADER_NUM_4_TXT)
            CreateDocxFile.addHeading_num(constants.PROPERTY, variables.HEADER_NUM_6_TXT)
            addTableElement(elementName, element, 'parseElement_property')
        CreateDocxFile.addLineBreak()

def parseObjectXML(objectType, objectName, methodName):
    filePath = variables.OBJECT_PATH
    xmlFile = os.path.join(filePath, objectType, objectName + constants.XMLEXT)
    if(os.path.exists(xmlFile)):
        objectDict = getattr(parseElement, methodName)(xmlFile)
        return objectDict

def getProjectDict():
    try:
        projectDict = parseElement.elementFromProject(variables.PROJECT_TXT)
    except:
        raise SystemExit(constants.PROJECT_ERROR)
    return projectDict

def parseLabelXML(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    fileName = root.find(constants.TEXTLABELFILE).text
    return fileName

def parseLabelFile(filePath):
    a_file = open(filePath, constants.READONLY, encoding = constants.ENCODINGSIG)
    # get labels and values as list
    # e.g. @sys.lableText=Lable Text
    labelNValue = [(line.strip()) for line in a_file if constants.SEMICOLON not in line]
    newdict = {labelNValue[i].split(constants.LABEL_SEPRATOR)[0]: labelNValue[i].split(constants.LABEL_SEPRATOR)[1] for i in range(0, len(labelNValue))}
    return newdict

def updateLabelList():
    for element in variables.LABELS_LIST:
        if(os.path.exists(element)):
            labelTextFile = os.path.join(variables.METADATA_TXT, parseLabelXML(element))
            if(os.path.exists(labelTextFile)):
                variables.LABELS_DICT.update(parseLabelFile(labelTextFile))

# process starts from here
def startProcess():
    projectDict = getProjectDict()
    updateLabelList()
    parseElement.labelDict(variables.LABELS_DICT)
    variables.TODAY = date.today().strftime('%B %d, %Y')
    variables.OBJECT_PATH = os.path.join(variables.METADATA_TXT, variables.PACKAGE_NAME, variables.MODEL_NAME)
    variables.OUTPUT_FILE_NAME = constants.TDD + variables.IDD_NAME + constants.DOCXEXT
    initDocument()
    addDocumentSection(projectDict)
    CreateDocxFile.saveDocx(variables.OUTPUT_TXT, variables.OUTPUT_FILE_NAME)