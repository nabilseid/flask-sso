from urllib.parse import urlsplit
from config import ProductionConfig, StagingConfig, TestingConfig, DevelopmentConfig

url_prefix = ['dev', 'staging', 'testing', 'localhost']

def get_config(env='testing'):
    """
    return config that is compatible with current env
    
    Parameters
    ----------
    env: str
        current environment. 
        Possible values
            dev:       development 
            staging:   staging
            testing:   testing
            localhost: testing 
            prod:      production -> not know infered

    Return 
    ------
    configs[env]: Config

    Notes
    ----
    env are extracted form referer address. There is no explicit indication
    of the env in production, thus we infer if the referer address doesn't
    indicate the other envs then it must be production.
    """

    configs = {
        'dev': DevelopmentConfig,
        'staging': StagingConfig,
        'testing': TestingConfig,
        'localhost': TestingConfig,
        'prod': ProductionConfig,
    }

    return configs[env] if env != None else None

def get_env_from_url(url):
    """
    extract env from url prefix

    Parameters
    ----------
    url: str
        referer url

    Return
    ------
    env: str
        application env

    Notes
    -----
    Unless for production all other env have refere url as
        env.address.domain
    """
    
    split_url = urlsplit(url)
    net_loc = split_url.netloc
    host = net_loc.split(':')[0]
    env = host.split('.')[0]
    
    if env in url_prefix:
        return env

    return 'prod'
