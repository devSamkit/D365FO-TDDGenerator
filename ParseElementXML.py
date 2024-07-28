import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import ParseElementConstant as constants
from TDDVariable import CODE_COLUMN_CHECKED

def labelDict(label = {}):
    labelDict.label = label

def elementFromProject(xmlFile):
    with open(xmlFile) as f:
        soup = BeautifulSoup(f, constants.XML)
    results = soup.find_all(constants.CONTENT)
    elementDict = {}
    for items in results:
        # get type and name seprated by '\'
        partitionResult = items.get(constants.INCLUDE).partition(constants.BACKWARD_SLASH)
        elementType = partitionResult[0]
        elementName = partitionResult[2]
        if(elementType not in elementDict.keys()):
            elementDict[elementType] = [elementName]
        else:
            elementDict[elementType].append(elementName)
    return elementDict

def compositeEntity(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    comEntityDict = {counter: constants.COMPOSITEENTITYLIST}
    for entity in root.iter(constants.DATAENTITY):
        counter += 1
        comEntityDict[counter] = [entity.text, constants.BLANK]
    return comEntityDict

def getLabel(labelText):
    if(constants.ATSIGN in labelText and constants.SEPRATOR in labelText):
        newLabelText = labelText.split(constants.SEPRATOR, 1)[1]
        if(newLabelText in labelDict.label):
            return labelDict.label[newLabelText]
        else:
            return labelText
    return labelText

def parseEntity_key(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    entityDict = {counter: [constants.DATA_FIELD, constants.REMARK]}
    keys = root.find(constants.KEYS)
    for key in keys.iter(constants.DATAFIELD):
        counter += 1
        entityDict[counter] = [key.text, '']
    return None if counter == 0 else entityDict

def parseElement_method(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    sourceCode = root.find(constants.SOURCECODE)
    if(sourceCode is None):
        sourceCode = root.find(constants.SOURCECODE_V6)
        
    if(CODE_COLUMN_CHECKED == True):
        methodDict = {counter: ['MethodName', 'Signature', 'Code', 'Remark']}
    else:
        methodDict = {counter: ['MethodName', 'Signature', 'Remark']}
        
    if(sourceCode is not None):
        for methods in sourceCode.iter('Method'):
            name = methods.find('Name')
            method = methods.find('Source')
            nameStr = ''
            methodStr = ''
            if(name is not None):
                nameStr = name.text
            if(method is not None):
                counter += 1
                methodStr = method.text.strip()
                partitionStr = methodStr.partition('{')
                partitionStr = filter(bool, partitionStr[0].splitlines())
                partitionStr = [x for x in partitionStr if '//' not in x]
                signature = ''.join(str(e) + '\n' for e in partitionStr)
                signature = signature.strip()
                signature += '\n' + '{}'
                if(CODE_COLUMN_CHECKED == True):
                    methodDict[counter] = [nameStr, signature, methodStr, '']
                else:
                    methodDict[counter] = [nameStr, signature, '']
                    
    return None if counter == 0 else methodDict

def parseMap_field(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    fieldDict = {counter: ['Name', 'Extended data type', 'Property']}
    for dataFields in root.iter('AxMapBaseField'):
        counter += 1
        name = dataFields.find('Name')
        edt = dataFields.find('ExtendedDataType')
        nameStr = ''
        edtStr = ''
        propertyStr = ''
        if(name is not None):
            nameStr = name.text
        if(edt is not None):
            edtStr = edt.text
        for property in dataFields.iter():
            if(len([dataFields for dataFields in property.iter()]) == 1 and property.text is not None and property.tag != 'Name' and property.tag != 'ExtendedDataType'):
                valueText = property.text
                if(property.tag == 'Label' or property.tag == 'HelpText'):
                    valueText = getLabel(valueText)
                propertyStr += property.tag + ': ' + valueText + '\n'
        fieldDict[counter] = [nameStr, edtStr, propertyStr.strip()]
    return fieldDict if counter != 0 else None

def parseTableColl(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    tableDict = {counter: ['Name', 'Remark']}
    for element in root.iter('AxTableCollectionTableReference'):
        counter += 1
        tableDict[counter] = [element.find('Name').text, '']
    return tableDict if counter != 0 else None

def parseEntity_field(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    fieldDict = {counter: ['Name', 'Datasource', 'Property']}
    for dataFields in root.iter('AxDataEntityViewField'):
        counter += 1
        name = dataFields.find('Name')
        dataSource = dataFields.find('DataSource')
        nameStr = ''
        dataSourceStr = ''
        propertyStr = ''
        if(name is not None):
            nameStr = name.text
        if(dataSource is not None):
            dataSourceStr = dataSource.text
        for property in dataFields.iter():
            if(len([dataFields for dataFields in property.iter()]) == 1 and property.text is not None and property.tag != 'Name' and property.tag != 'DataSource'):
                valueText = property.text
                if(property.tag == 'Label' or property.tag == 'HelpText'):
                    valueText = getLabel(valueText)
                propertyStr += property.tag + ': ' + valueText + '\n'
        fieldDict[counter] = [nameStr, dataSourceStr, propertyStr.strip()]
    return fieldDict if counter != 0 else None

def parseEntityExt_field(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    fieldDict = {counter: ['Name', 'Datasource']}
    for dataFields in root.iter('AxDataEntityViewField'):
        counter += 1
        name = dataFields.find('Name')
        dataSource = dataFields.find('DataSource')
        nameStr = ''
        dataSourceStr = ''
        if(name is not None):
            nameStr = name.text
        if(dataSource is not None):
            dataSourceStr = dataSource.text
        fieldDict[counter] = [nameStr, dataSourceStr]
    return None if counter == 0 else fieldDict

def parseEDTExt(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    edtExtDict = {counter: ['Modified property', 'Value']}
    for element in root.iter('AxPropertyModification'):
        counter += 1
        name = element.find('Name')
        value = element.find('Value')
        nameStr = ''
        valueStr = ''
        if(name is not None):
            nameStr = name.text
        if(value is not None):
            valueStr = value.text
        edtExtDict[counter] = [nameStr, valueStr]
    return None if counter == 0 else edtExtDict

def parseEnum_value(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    valueDict = {counter: ['Name', 'Label', 'Enum value']}

    for element in root.iter('AxEnumValue'):
        name = element.find('Name') 
        label = element.find('Label')
        value = element.find('Value')
        nameStr = ''
        labelStr = ''
        valueStr = ''
        if(name is not None):
            nameStr = name.text
        if(label is not None):
            labelStr = getLabel(label.text)
        if(value is not None):
            valueStr = value.text
        counter += 1
        valueDict[counter] = [nameStr, labelStr, valueStr]
    return None if counter == 0 else valueDict

def parseEnumExt(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    enumExtDict = {counter: ['Name', 'Label']}
    for element in root.iter('AxEnumValue'):
        name = element.find('Name') 
        label = element.find('Label')
        nameStr = ''
        labelStr = ''
        if(name is not None):
            nameStr = name.text
        if(label is not None):
            labelStr = getLabel(label.text)
        counter += 1
        enumExtDict[counter] = [nameStr, labelStr]
    return None if counter == 0 else enumExtDict

def parseElement_property(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    propertyDict = {counter: ['Property', 'Value']}
    for elem in list(root):
        elemTag = elem.tag.partition('}')[2] if '}' in elem.tag else elem.tag
        if(elemTag != 'Name' and (elem.text is not None and elem.text.strip() != '')):
            counter += 1
            valueText = elem.text
            if(elemTag == 'Label' or elemTag == 'DeveloperDocumentation'):
                valueText = getLabel(elem.text)
            propertyDict[counter] = [elemTag, valueText]
    return None if counter == 0 else propertyDict

def parseAggEntity_measure(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    measureDict = {counter: ['Name', 'Measurement']}
    for element in root.iter('AggregateViewDataSource'):
        counter += 1
        name = element.find('Name')
        nameStr = ''
        measure = element.find('Measurement')
        measureStr = ''
        if(name is not None):
            nameStr = name.text
        if(measure is not None):
            measureStr = measure.text
        measureDict[counter] = [nameStr, measureStr]
    return measureDict if counter != 0 else None

def parseAggEntity_field(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    fieldDict = {counter: ['Name', 'Property']}
    for element in root.iter('AxAggregateDataEntityField'):
        counter += 1
        name = element.find('Name')
        nameStr = ''
        if(name is not None):
            nameStr = name.text
        propertyStr = ''
        for property in element.iter():
            if(len([elements for elements in property.iter()]) == 1 and property.text is not None and property.tag != 'Name'):
                # remove xmlns:d3p1='Microsoft.Dynamics.AX.Metadata.V2' from tag
                propertyStr += (property.tag.partition('}')[2] if '}' in property.tag else property.tag) + ': ' + property.text + '\n'
        fieldDict[counter] = [nameStr, propertyStr.strip()]
    return None if counter == 0 else fieldDict

def parseTable_field(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    fieldDict = {counter: ['Name', 'Extended data type', 'Property']}
    for element in root.iter('AxTableField'):
        counter += 1
        name = element.find('Name')
        edt = element.find('ExtendedDataType')
        nameStr = ''
        edtStr = ''
        if(name is not None):
            nameStr = name.text
        if(edt is not None):
            edtStr = edt.text
        propertyStr = ''
        for property in element.iter():
            if(len([elements for elements in property.iter()]) == 1 and property.text is not None and property.tag != 'Name' and property.tag != 'ExtendedDataType'):
                valueText = property.text
                if(property.tag == 'Label' or property.tag == 'HelpText'):
                    valueText = getLabel(valueText)
                propertyStr += property.tag + ': ' + valueText + '\n'
        fieldDict[counter] = [nameStr, edtStr, propertyStr.strip()]
    return None if counter == 0 else fieldDict

def parseTable_fieldGroup(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    groupDict = {counter: ['Field group', 'Field', 'Label']}
    for element in root.iter('AxTableFieldGroup'):
        counter += 1
        groupName = element.find('Name').text
        label = element.find('Label')
        labelTxt = ''
        if(label is not None):
            labelTxt = getLabel(label.text)
        fields = ''
        for field in element.iter('DataField'):
            fields += field.text + '\n'
        groupDict[counter] = [groupName, fields, labelTxt]
    return None if counter == 0 else groupDict

def parseTable_index(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    idxDict = {counter: ['Index', 'Property', 'Field']}
    for element in root.iter('AxTableIndex'):
        counter += 1
        idxName = element.find('Name').text
        propertyTxt = ''
        fields = ''
        for property in element.iter():
            if(len([elements for elements in property.iter()]) == 1 
                    and property.text is not None 
                    and property.tag != 'Name' 
                    and property.tag != 'DataField'):
                propertyTxt += property.tag + ': ' + property.text + '\n'
        for field in element.iter('DataField'):
            fields += field.text + '\n'
        idxDict[counter] = [idxName, propertyTxt.strip(), fields.strip()]
    return None if counter == 0 else idxDict

def parseTable_relation(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    relationDict = {counter: ['Relation', 'Related table', 'Field', 'Related field', 'Property']}
    for element in root.iter('AxTableRelation'):
        counter += 1
        relationName = element.find('Name').text
        relatedTable = element.find('RelatedTable')
        relatedTableStr = ''
        fieldStr = ''
        relatedFieldStr = ''
        propertyStr = ''
        if(relatedTable is not None):
            relatedTableStr = relatedTable.text
        for property in element.iter():
            if(len([elements for elements in property.iter()]) == 1 
                    and property.text is not None 
                    and property.tag != 'Name' 
                    and property.tag != 'RelatedTable'):
                propertyStr += property.tag + ': ' + property.text + '\n'
        for relation in element.iter('AxTableRelationConstraint'):
            field = relation.find('Field')
            relatedField = relation.find('RelatedField')
            if(field is not None):
                fieldStr += field.text + '\n'
            if(relatedField is not None):
                relatedFieldStr += relatedField.text + '\n'
        
        relationDict[counter] = [relationName, relatedTableStr, fieldStr.strip(), relatedFieldStr.strip(), propertyStr.strip()]
    return None if counter == 0 else relationDict


def parseView_field(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    fieldDict = {counter: ['Name', 'DataSource', 'Data field', 'Property']}
    for element in root.iter('AxViewField'):
        counter += 1
        name = element.find('Name')
        datasource = element.find('DataSource')
        dataField = element.find('DataField')
        nameStr = ''
        datasourceStr = ''
        dataFieldStr = ''
        if(name is not None):
            nameStr = name.text
        if(datasource is not None):
            datasourceStr = datasource.text
        if(dataField is not None):
            dataFieldStr = dataField.text
        propertyStr = ''
        for property in element.iter():
            if(len([elements for elements in property.iter()]) == 1 
                    and property.text is not None
                    and property.tag != 'Name'
                    and property.tag != 'DataSource'
                    and property.tag != 'DataField'):
                valueText = property.text
                if(property.tag == 'Label' or property.tag == 'HelpText'):
                    valueText = getLabel(valueText)
                propertyStr += property.tag + ': ' + valueText + '\n'
        fieldDict[counter] = [nameStr, datasourceStr, dataFieldStr, propertyStr.strip()]
    return None if counter == 0 else fieldDict

def parseViewNQuery_DS(xmlFile):
    def getRange(rangeElement):
        range = ''
        for ranges in rangeElement.findall('AxQuerySimpleDataSourceRange'):
            rangefield = ranges.find('Field')
            rangeValue = ranges.find('Value')
            rangefieldStr = ''
            rangeValueStr = ''
            if(rangefield is not None):
                rangefieldStr = rangefield.text
            if(rangeValue is not None):
                rangeValueStr = rangeValue.text
            range += 'Field' + ': ' + rangefieldStr + '\n'  + 'Value' + ': ' + rangeValueStr + '\n'
        return range.strip()
    
    def getRelation(relationElement):
        notRequired = ['AxQuerySimpleDataSourceRelation', 'Name']
        relation = ''
        for relations in relationElement.findall('AxQuerySimpleDataSourceRelation'):
            for element in relations.iter():
                if(element.tag not in notRequired):
                    relation += element.tag + ': ' + element.text + '\n'
        return relation.strip()

    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    dsDict = {counter: ['DataSource', 'Table', 'Relation', 'Range']}
    viewMeta = root.find('ViewMetadata')
    if(viewMeta is not None):
        dataSources = viewMeta.find('DataSources')
    else:
        dataSources = root.find('DataSources')
    rootDS = dataSources.find('AxQuerySimpleRootDataSource')
    if(rootDS is not None):
        counter += 1
        rootDSRange = rootDS.find('Ranges')
        if(rootDSRange is not None):
            ranges = getRange(rootDSRange)
        dsDict[counter] = [rootDS.find('Name').text, rootDS.find('Table').text, '', ranges]
        for embeddedDS in rootDS.iter('AxQuerySimpleEmbeddedDataSource'):
            counter += 1
            ranges = ''
            relations = ''
            embeddedDSRange = embeddedDS.find('Ranges')
            if(embeddedDSRange is not None):
                ranges = getRange(embeddedDSRange)
            embeddedDSRelation = embeddedDS.find('Relations')
            if(embeddedDSRelation is not None):
                relations = getRelation(embeddedDSRelation)
            dsDict[counter] = [embeddedDS.find('Name').text, embeddedDS.find('Table').text, relations, ranges]

    return dsDict if counter != 0 else None

def parseQuery_groupBy(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    queryDict = {counter: ['DataSource', 'Field']}
    # groupBy = root.find('GroupBy')
    # if(groupBy is not None):
    for element in root.iter('AxQuerySimpleGroupByField'):
        counter += 1
        queryDict[counter] = [element.find('DataSource').text, element.find('Field').text]
    return queryDict if counter != 0 else None

def parseQuery_orderBy(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    queryDict = {counter: ['DataSource', 'Field']}
    # orderBy = root.find('OrderBy')
    # if(orderBy is not None):
    for element in root.iter('AxQuerySimpleOrderByField'):
        counter += 1
        queryDict[counter] = [element.find('DataSource').text, element.find('Field').text]
    return queryDict if counter != 0 else None

def parseQueryNViewExt_ds(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    dsDict = {counter: ['DataSource', 'Parent', 'Relation', 'Range']}
    for extDS in root.iter('AxQueryExtensionEmbeddedDataSource'):
        counter += 1
        parent = extDS.find('Parent').text
        ds = extDS.find('DataSource')
        tableName = ds.find('Table').text
        relation = ''
        range = ''
        for relations in ds.iter('AxQuerySimpleDataSourceRelation'):
            relation += relations.find('JoinDataSource').tag + ': '+ relations.find('JoinDataSource').text + '\n'
            if(ds.find('JoinMode') is not None):
                relation += ds.find('JoinMode').tag + ': ' + ds.find('JoinMode').text + '\n'
            relation += relations.find('Field').tag + ': ' + relations.find('Field').text + '\n'
            relation += relations.find('RelatedField').tag + ': ' + relations.find('RelatedField').text + '\n'
        for ranges in ds.iter('AxQuerySimpleDataSourceRange'):
            range += ranges.find('Field').tag + ': ' + ranges.find('Field').text + '\n'
            range += ranges.find('Value').tag + ': ' + ranges.find('Value').text + '\n'
        dsDict[counter] = [tableName, parent, relation.strip(), range.strip()]
    return dsDict if counter != 0 else None

def parseForm_design(xmlFile):
    with open(xmlFile) as f:
        soup = BeautifulSoup(f, 'xml')
    results = soup.find('Design')
    if(results):
        counter = 0
        formDesignDict = {counter: ['Property', 'Value']}
        caption = results.find('Caption')
        if(caption is not None):
            counter += 1
            formDesignDict[counter] = ['Caption', getLabel(caption.text)]
        pattern = results.find('Pattern')
        if(pattern is not None):
            counter += 1
            formDesignDict[counter] = ['Pattern', pattern.text]
        style = results.find('Style')
        if(style is not None):
            counter += 1
            formDesignDict[counter] = ['Style', style.text]

    return formDesignDict

def parseForm_datasource(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    formDSDict = {counter: ['Name', 'Parent datasource', 'Property']}
    for datasources in root.iter('AxFormDataSource'):
        counter += 1
        table = datasources.find('Table')
        joinDS = datasources.find('JoinSource')
        tableStr = ''
        joinDSStr = ''
        propertyStr = ''
        if(table is not None):
            tableStr = table.text
        if(joinDS is not None):
            joinDSStr = joinDS.text
        for property in datasources.iter():
            if(len([elements for elements in property.iter()]) == 1 
                    and property.text is not None
                    and property.tag != 'Name'
                    and property.tag != 'DataSource'
                    and property.tag != 'Table'
                    and property.tag != 'DataField'):
                valueText = property.text
                if(property.tag == 'Label' or property.tag == 'HelpText'):
                    valueText = getLabel(valueText)
                propertyStr += property.tag + ': ' + valueText + '\n'
        formDSDict[counter] = [tableStr, joinDSStr, propertyStr.strip()]
    return None if counter == 0 else formDSDict

def parseTableExt_modifiedDict(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    modifiedDict = {counter: ['Modified Property', 'Value']}
    for element in root.iter('AxPropertyModification'):
        counter += 1
        modifiedDict[counter] = [element.find('Name').text, element.find('Value').text]
    return modifiedDict if counter != 0 else None

def parseFormExt_recursive(tree_in, parent_name, counter, controlDict):
    newCounter = counter + 1
    newControlDict = controlDict
    for tags in list(tree_in):
        if(tags.tag == 'FormControl' or tags.tag == 'AxFormControl'):
            newControlDict[newCounter] = [tags.find('Name').text, tags.find('Type').text, parent_name]
            newParent = tags.find('Name').text
            newCounter += 1
            newControlDict = parseFormExt_recursive(tags, newParent, newCounter, newControlDict)
        if(tags.tag == 'Controls'):
            newControlDict = parseFormExt_recursive(tags, parent_name, newCounter, newControlDict)
    return newControlDict

def parseFormExt(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    controlDict = {0: ['Name', 'Type', 'Parent']}
    for items in root.iter('AxFormExtensionControl'):
        parent = items.find('Parent').text
        controlDict = parseFormExt_recursive(items, parent, 0, controlDict)
    return controlDict   

def parseMenu_recursive(tree_in, parent_name, menuDict):
    newMenuDict = menuDict
    for tags in list(tree_in):
        property = ''
        if(tags.tag == 'AxMenuElement'):
            for properties in list(tags):
                if(properties.tag != 'Name' and properties.tag != 'Elements' and properties.text is not None):
                    valueText = properties.text
                    if(properties.tag == 'Label'):
                        valueText = getLabel(valueText)
                    property += properties.tag + ': ' + valueText + '\n'
            parseMenu.counter += 1
            newMenuDict[parseMenu.counter] = [tags.find('Name').text, property.strip(), parent_name]
            newParent = tags.find('Name').text
            newMenuDict = parseMenu_recursive(tags, newParent, newMenuDict)
        if(tags.tag == '{Microsoft.Dynamics.AX.Metadata.V1}Elements' or tags.tag == 'Elements'):
            newMenuDict = parseMenu_recursive(tags, parent_name, newMenuDict)
    return newMenuDict

def parseMenu(xmlFile):
    parseMenu.counter = 0
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    menuDict = {0: ['Name', 'Property', 'Parent']}
    parent = root.find('{Microsoft.Dynamics.AX.Metadata.V1}Name').text
    menuDict = parseMenu_recursive(root, parent, menuDict)
    return menuDict

def parseMenuExt_recursive(tree_in, parent_name, menuDict):
    newMenuDict = menuDict
    for tags in list(tree_in):
        property = ''
        if(tags.tag == 'AxMenuElement' or tags.tag == 'MenuElement'):
            for properties in list(tags):
                if(properties.tag != 'Name' and properties.tag != 'Elements' and properties.text is not None):
                    valueText = properties.text
                    if(properties.tag == 'Label'):
                        valueText = getLabel(valueText)
                    property += properties.tag + ': ' + valueText + '\n'
            parseMenuExt.counter += 1
            newMenuDict[parseMenuExt.counter] = [tags.find('Name').text, property.strip(), parent_name]
            newParent = tags.find('Name').text
            newMenuDict = parseMenuExt_recursive(tags, newParent, newMenuDict)
        if(tags.tag == '{Microsoft.Dynamics.AX.Metadata.V1}Elements' or tags.tag == 'Elements'):
            newMenuDict = parseMenuExt_recursive(tags, parent_name, newMenuDict)
        if(tags.tag == 'AxMenuExtensionElement'):
            parentText = tags.find('Parent').text
            newMenuDict = parseMenuExt_recursive(tags, parentText, newMenuDict)
    return newMenuDict

def parseMenuExt(xmlFile):
    parseMenuExt.counter = 0
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    menuDict = {0: ['Name', 'Property', 'Parent']}
    parent = root.find('{Microsoft.Dynamics.AX.Metadata.V1}Name').text
    menuDict = parseMenuExt_recursive(root, parent, menuDict)
    return menuDict

def parseMenuItem(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    menuItemDict = {counter: ['Name', 'Object', 'Type', 'Property']}
    counter += 1
    name = root.find('{Microsoft.Dynamics.AX.Metadata.V1}Name').text
    objectStr = root.find('{Microsoft.Dynamics.AX.Metadata.V1}Object').text
    objectType = root.find('{Microsoft.Dynamics.AX.Metadata.V1}ObjectType').text if root.find('{Microsoft.Dynamics.AX.Metadata.V1}ObjectType') is not None  else 'Form'
    property = ''
    for properties in list(root):
        if(properties.tag != '{Microsoft.Dynamics.AX.Metadata.V1}Name' 
            and properties.tag != '{Microsoft.Dynamics.AX.Metadata.V1}Object' 
            and properties.tag != '{Microsoft.Dynamics.AX.Metadata.V1}ObjectType' 
            and properties.text is not None and properties.text.strip() != ''):
            valueText = properties.text
            if(properties.tag == '{Microsoft.Dynamics.AX.Metadata.V1}Label' or '{Microsoft.Dynamics.AX.Metadata.V1}HelpText'):
                valueText = getLabel(valueText)
            property += (properties.tag.partition('}')[2] if '}' in properties.tag else properties.tag) + ': ' + valueText + '\n'
    menuItemDict[counter] = [name, objectStr, objectType, property]
    return menuItemDict

def parseMenuItemExt(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    menuItemDict = {0: ['Modified Property', 'Value']}
    for element in root.iter('AxPropertyModification'):
        counter += 1
        name = element.find('Name').text
        value = element.find('Value').text
        if(name == 'Label' or name == 'HelpText'):
            value = getLabel(value)
        menuItemDict[counter] = [name, value]
    return menuItemDict

def parseAggDim_attribute(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    aggDimDict = {0: ['Name', 'Property', 'Key field']}
    for element in root.iter('AxDimensionAttribute'):
        counter += 1
        name = element.find('Name').text
        properties = ''
        for prop in list(element):
            if(prop.tag != 'Name' and prop.text is not None and prop.text.strip() != ''):
                properties += prop.tag + ': ' + prop.text + '\n'
        keys = ''
        for key in element.iter('DimensionField'):
            keys += key.text + '\n'
        aggDimDict[counter] = [name, properties.strip(), keys.strip()]
    return aggDimDict if counter != 0 else None

def parseReport_dataSet(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    counter = 0
    dsDict = {counter: [constants.NAME, constants.DS_TYPE, constants.QUERY]}
    for element in root.iter(constants.REPORTDS):
        counter += 1
        name = element.find(constants.NAME)
        dsType = element.find(DSTYPE)
        query = element.find(constants.QUERY)
        nameStr = ''
        dsTypeStr = ''
        queryStr = ''
        if(name is not None):
            nameStr = name.text
        if(dsType is not None):
            dsTypeStr = dsType.text
        if(query is not None):
            queryStr = query.text
        dsDict[counter] = [nameStr, dsTypeStr, queryStr]
    return dsDict if counter != 0 else None

# def parseWFApproval_outcome(xmlFile):
#     tree = ET.parse(xmlFile)
#     root = tree.getroot()
#     counter = 0
#     wfDict = {counter: ['Approve', 'Deny', 'Query']}