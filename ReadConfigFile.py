import configparser
import os
import ConfigConstant as constants
import TDDVariable as variables

def readConfigFile():
    try:
        configFile = os.path.join(os.getcwd(), constants.CONFIG_FILE_NAME)
        
        if(os.path.exists(configFile) == False):
            return
        
        config = configparser.ConfigParser()
        config.read(configFile)
        
        path            = config[constants.PATH]
        packages        = config[constants.PACKAGES]
        label           = config[constants.LABEL]
        document        = config[constants.DOCUMENT]
        documentSection = config[constants.DOCUMENT_SECTION]
        overview        = config[constants.OVERVIEW]
        customisation   = config[constants.CUSTOMISATION]
        
        variables.TEMPLATE_TXT  = path[constants.TEMPLATE]
        variables.PROJECT_TXT   = path[constants.PROJECT]
        variables.METADATA_TXT  = path[constants.METADATA]
        variables.OUTPUT_TXT    = path[constants.OUTPUT]
        
        variables.PACKAGE_NAME  = packages[constants.PACKAGE]
        variables.MODEL_NAME    = packages[constants.MODEL]
        
        variables.LABELS_LIST   = label[constants.LABELS]
        
        variables.CUST_NAME         = document[constants.PREPARED_FOR]
        variables.DEVELOPER_NAME    = document[constants.DEVELOPER]
        variables.IDD_NAME          = document[constants.IDD]
        
        variables.CHANGE_RECORD_CHECKED = documentSection[constants.CHANGE_RECORD] == constants.TRUE_VALUE
        variables.APPROVER_CHECKED      = documentSection[constants.APPROVERS] == constants.TRUE_VALUE
        variables.ESTIMATES_CHECKED     = documentSection[constants.ESTIMATES] == constants.TRUE_VALUE
        variables.PERFORMANCE_CHECKED   = documentSection[constants.PERFORMANCE] == constants.TRUE_VALUE
        variables.ASSUMPTIONS_CHECKED   = documentSection[constants.ASSUMPTIONS] == constants.TRUE_VALUE
        variables.REVIEWER_CHECKED      = documentSection[constants.REVIEWER] == constants.TRUE_VALUE
        variables.ENTRYANDEXIT_CHECKED  = documentSection[constants.ENTRY_EXIT] == constants.TRUE_VALUE
        variables.UNITTEST_CHECKED      = documentSection[constants.UNIT_TEST] == constants.TRUE_VALUE
        variables.UPGRADABILITY_CHECKED = documentSection[constants.UPGRADABILITY] == constants.TRUE_VALUE
        
        variables.OBJECTIVE_TXT         = overview[constants.OBJECTIVE]
        variables.AUDIENCE_TXT          = overview[constants.AUDIENCE]
        variables.ACRONYM_DESC_TXT      = overview[constants.ACRONYM]
        variables.ACRONYM_DESC_TXT      = overview[constants.ACRONYM_DESC]
        variables.REF_DOCUMENT_TXT      = overview[constants.REFERENCE_DOC]
        variables.REF_DESC_TXT          = overview[constants.REFERENCE_DESC]
        variables.PURPOSE_OVERVIEW_TXT  = overview[constants.PURPOSE_OVERVIEW]
        
        variables.CODE_COLUMN_CHECKED   = customisation[constants.CODE_COLUMN] == constants.TRUE_VALUE
        variables.TABLE_TXT             = customisation[constants.TABLE_STYLE]
        variables.HEADER_NUM_1_TXT      = customisation[constants.HEADER_1]
        variables.HEADER_NUM_2_TXT      = customisation[constants.HEADER_2]
        variables.HEADER_NUM_3_TXT      = customisation[constants.HEADER_3]
        variables.HEADER_NUM_4_TXT      = customisation[constants.HEADER_4]
        variables.HEADER_NUM_5_TXT      = customisation[constants.HEADER_5]
        variables.HEADER_NUM_6_TXT      = customisation[constants.HEADER_6]
        
    except:
        print(constants.CONFIG_READ_ERROR)
        