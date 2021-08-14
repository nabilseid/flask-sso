from src.config import ProductionConfig, StagingConfig,
                       TestingConfig, DevelopmentConfig 

def get_config(env='testing'):
    """
    return config that is compatible with current env
    
    Parameters
    ----------
    env: str
        current environment. 
        Possible values
            dev:      development 
            staging:  staging
            testing:  testing
            api:      production

    Return 
    ------
    configs[env]: Config
    """

    configs = {
        'dev': DevelopmentConfig,
        'staging': StagingConfig,
        'testing': TestingConfig,
        'api': ProductionConfig,
    }

    return configs[env]

