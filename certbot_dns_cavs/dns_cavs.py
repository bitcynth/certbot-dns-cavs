import logging

import zope.interface
import requests
import json

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    description = 'Obtain certs using DNS TXT with Cynthia ACME Validation Service (CAVS)'
    ttl = 30
    
    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=10)
        add('credentials', help='CAVS .ini file.')
    
    def more_info(self):
        return self.description
    
    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'CAVS .ini file',
            {
                'token': 'API token for CAVS'
            }
        )
    
    def _perform(self, domain, validation_name, validation):
        self._get_cavs_client().add_record(domain, validation_name, validation)
    
    def _cleanup(self, domain, validation_name, validation):
        self._get_cavs_client().cleanup_record(domain, validation_name, validation)

    def _get_cavs_client(self):
        return _CAVSClient(self.credentials.conf('token'))

class _CAVSClient(object):
    def __init__(self, token):
        logger.debug('creating CAVS client')
        self.base_url = 'https://acme-validation-service.cynthia.re/'
        self.token = token
    
    def _api_req(self, endpoint, payload):
        resp = requests.post(f'{self.base_url}api/v1/{endpoint}', json=payload)
        if resp.status_code != 200:
            raise errors.PluginError(f'HTTP error during api req: {resp.status_code}')
    
    def add_record(self, domain, validation_name, validation):
        payload = {
            'token': self.token,
            'domain': domain,
            'validation_name': validation_name,
            'validation_token': validation
        }
        self._api_req('add_validation_record', payload)
    
    def cleanup_record(self, domain, validation_name, validation):
        payload = {
            'token': self.token,
            'domain': domain,
            'validation_name': validation_name,
            'validation_token': validation
        }
        self._api_req('cleanup_validation_record', payload)
