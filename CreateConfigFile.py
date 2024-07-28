import configparser
import os
import ConfigConstant as constants
import TDDVariable as variables

# Update config file if already exists
def updateConfig(_configPath: str):
    
    config = configparser.ConfigParser()
    config.read(_configPath)
    
    path            = config[constants.PATH]
    packages        = config[constants.PACKAGES]
    label           = config[constants.LABEL]
    document        = config[constants.DOCUMENT]
    documentSection = config[constants.DOCUMENT_SECTION]
    overview        = config[constants.OVERVIEW]
    customisation   = config[constants.CUSTOMISATION]
    
    path[constants.TEMPLATE]    = variables.TEMPLATE_TXT
    path[constants.PROJECT]     = variables.PROJECT_TXT
    path[constants.METADATA]    = variables.METADATA_TXT
    path[constants.OUTPUT]      = variables.OUTPUT_TXT
    
    packages[constants.PACKAGE] = variables.PACKAGE_NAME
    packages[constants.MODEL]   = variables.MODEL_NAME
    
    labelStr = constants.LABEL_SEPARATOR.join(variables.LABELS_LIST)
    label[constants.LABELS] = labelStr
    
    document[constants.PREPARED_FOR]    = variables.CUST_NAME
    document[constants.DEVELOPER]       = variables.DEVELOPER_NAME
    document[constants.IDD]             = variables.IDD_NAME
    
    documentSection[constants.CHANGE_RECORD]    = str(variables.CHANGE_RECORD_CHECKED)
    documentSection[constants.APPROVERS]        = str(variables.APPROVER_CHECKED)
    documentSection[constants.ESTIMATES]        = str(variables.ESTIMATES_CHECKED)
    documentSection[constants.PERFORMANCE]      = str(variables.PERFORMANCE_CHECKED)
    documentSection[constants.ASSUMPTIONS]      = str(variables.ASSUMPTIONS_CHECKED)
    documentSection[constants.REVIEWER]         = str(variables.REVIEWER_CHECKED)
    documentSection[constants.ENTRY_EXIT]       = str(variables.ENTRYANDEXIT_CHECKED)
    documentSection[constants.UNIT_TEST]        = str(variables.UNITTEST_CHECKED)
    documentSection[constants.UPGRADABILITY]    = str(variables.UPGRADABILITY_CHECKED)
    
    overview[constants.OBJECTIVE]           = variables.OBJECTIVE_TXT
    overview[constants.AUDIENCE]            = variables.AUDIENCE_TXT
    overview[constants.ACRONYM]             = variables.ACRONYM_DESC_TXT
    overview[constants.ACRONYM_DESC]        = variables.ACRONYM_DESC_TXT
    overview[constants.REFERENCE_DOC]       = variables.REF_DOCUMENT_TXT
    overview[constants.REFERENCE_DESC]      = variables.REF_DESC_TXT
    overview[constants.PURPOSE_OVERVIEW]    = variables.PURPOSE_OVERVIEW_TXT
    
    customisation[constants.CODE_COLUMN]    = str(variables.CODE_COLUMN_CHECKED)
    customisation[constants.TABLE_STYLE]    = variables.TABLE_TXT
    customisation[constants.HEADER_1]       = variables.HEADER_NUM_1_TXT
    customisation[constants.HEADER_2]       = variables.HEADER_NUM_2_TXT
    customisation[constants.HEADER_3]       = variables.HEADER_NUM_3_TXT
    customisation[constants.HEADER_4]       = variables.HEADER_NUM_4_TXT
    customisation[constants.HEADER_5]       = variables.HEADER_NUM_5_TXT
    customisation[constants.HEADER_6]       = variables.HEADER_NUM_6_TXT
    
    return config
    
# Create Config file if does not exists
def createConfig():
    
    config = configparser.ConfigParser()
    
    config.add_section(constants.PATH)
    config.add_section(constants.PACKAGES)
    config.add_section(constants.LABEL)
    config.add_section(constants.DOCUMENT)
    config.add_section(constants.DOCUMENT_SECTION)
    config.add_section(constants.OVERVIEW)
    config.add_section(constants.CUSTOMISATION)
    
    config.set(constants.PATH, constants.TEMPLATE, variables.TEMPLATE_TXT)
    config.set(constants.PATH, constants.PROJECT, variables.PROJECT_TXT)
    config.set(constants.PATH, constants.METADATA, variables.METADATA_TXT)
    config.set(constants.PATH, constants.OUTPUT, variables.OUTPUT_FILE_NAME)
    
    config.set(constants.PACKAGES, constants.PACKAGE, variables.PACKAGE_NAME)
    config.set(constants.PACKAGES, constants.MODEL, variables.MODEL_NAME)
    
    labelStr = constants.LABEL_SEPARATOR.join(variables.LABELS_LIST)
    config.set(constants.LABEL, constants.LABELS, labelStr)
    
    config.set(constants.DOCUMENT, constants.PREPARED_FOR, variables.CUST_NAME)
    config.set(constants.DOCUMENT, constants.DEVELOPER, variables.DEVELOPER_NAME)
    config.set(constants.DOCUMENT, constants.IDD, variables.IDD_NAME)
    
    config.set(constants.DOCUMENT_SECTION, constants.CHANGE_RECORD, str(variables.CHANGE_RECORD_CHECKED))
    config.set(constants.DOCUMENT_SECTION, constants.APPROVERS, str(variables.APPROVER_CHECKED))
    config.set(constants.DOCUMENT_SECTION, constants.ESTIMATES, str(variables.ESTIMATES_CHECKED))
    config.set(constants.DOCUMENT_SECTION, constants.PERFORMANCE, str(variables.PERFORMANCE_CHECKED))
    config.set(constants.DOCUMENT_SECTION, constants.ASSUMPTIONS, str(variables.ASSUMPTIONS_CHECKED))
    config.set(constants.DOCUMENT_SECTION, constants.REVIEWER, str(variables.REVIEWER_CHECKED))
    config.set(constants.DOCUMENT_SECTION, constants.ENTRY_EXIT, str(variables.ENTRYANDEXIT_CHECKED))
    config.set(constants.DOCUMENT_SECTION, constants.UNIT_TEST, str(variables.UNITTEST_CHECKED))
    config.set(constants.DOCUMENT_SECTION, constants.UPGRADABILITY, str(variables.UPGRADABILITY_CHECKED))
    
    config.set(constants.OVERVIEW, constants.OBJECTIVE, variables.OBJECTIVE_TXT)
    config.set(constants.OVERVIEW, constants.AUDIENCE, variables.AUDIENCE_TXT)
    config.set(constants.OVERVIEW, constants.ACRONYM, variables.ACRONYM_DESC_TXT)
    config.set(constants.OVERVIEW, constants.ACRONYM_DESC, variables.ACRONYM_DESC_TXT)
    config.set(constants.OVERVIEW, constants.REFERENCE_DOC, variables.REF_DOCUMENT_TXT)
    config.set(constants.OVERVIEW, constants.REFERENCE_DESC, variables.REF_DESC_TXT)
    config.set(constants.OVERVIEW, constants.PURPOSE_OVERVIEW, variables.PURPOSE_OVERVIEW_TXT)
    
    config.set(constants.CUSTOMISATION, constants.CODE_COLUMN, str(variables.CODE_COLUMN_CHECKED))
    config.set(constants.CUSTOMISATION, constants.TABLE_STYLE, variables.TABLE_TXT)
    config.set(constants.CUSTOMISATION, constants.HEADER_1, variables.HEADER_NUM_1_TXT)
    config.set(constants.CUSTOMISATION, constants.HEADER_2, variables.HEADER_NUM_2_TXT)
    config.set(constants.CUSTOMISATION, constants.HEADER_3, variables.HEADER_NUM_3_TXT)
    config.set(constants.CUSTOMISATION, constants.HEADER_4, variables.HEADER_NUM_4_TXT)
    config.set(constants.CUSTOMISATION, constants.HEADER_5, variables.HEADER_NUM_5_TXT)
    config.set(constants.CUSTOMISATION, constants.HEADER_6, variables.HEADER_NUM_6_TXT)
        
    return config
    
def startProcess():
    try:
        configPath = os.path.join(os.getcwd(), constants.CONFIG_FILE_NAME)
        
        if(os.path.exists(configPath)):
            try:
                config = updateConfig(configPath)
            except:
                config = createConfig()
        else:
            config = createConfig()
            
        with open(configPath, constants.OPEN_TEXT_MODE) as configfile:
            config.write(configfile)
    except:
        print(constants.CONFIG_ERROR)