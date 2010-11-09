import xmlrpclib
from django.conf import settings
from error import OpenXError

class OpenXClient(object):
  def __init__(self):
    self.__session = None
  @property
  def _session(self):
    if self.__session is None:
      s = xmlrpclib.ServerProxy(settings.OPENX_URL, allow_none=True)
      self.__session = s.ox.logon(settings.OPENX_USERNAME, settings.OPENX_PASSWORD)
    return self.__session
  def _renew_session(self):
    self.__session = None
  def __getattr__(self, name):
    return OpenXServiceClientWrapper(self)

class OpenXServiceClientWrapper(object):
  def __init__(self, client):
    self._client = client
    self._xmlrpc_client = xmlrpclib.ServerProxy(settings.OPENX_URL, allow_none=True)
  def __getattr__(self, name):
    return OpenXServiceClient(self._client, self._xmlrpc_client, getattr(self._xmlrpc_client, name))

class OpenXServiceClient(object):
  def __init__(self, client, xmlrpc_client, xmlrpc_method):
    self._client = client
    self._xmlrpc_client = xmlrpc_client
    self._xmlrpc_method = xmlrpc_method
    
  def __getattr__(self, name):
    return OpenXServiceClient(self._client, self._xmlrpc_client, getattr(self._xmlrpc_method, name))
    
  def __call__(self, *args, **kwargs):
    try:
      return self._xmlrpc_method(self._client._session, *args, **kwargs)
    except xmlrpclib.Fault, err:
      if self.is_session_invalid(err):
        self._client._renew_session()
        try:
          return self._xmlrpc_method(self._client._session, *args, **kwargs)
        except xmlrpclib.Fault, err:
          raise OpenXError(err.faultCode, err.faultString)
      else:
        raise OpenXError(err.faultCode, err.faultString)
  
  def is_session_invalid(self, err):
    return err.faultString == 'Session ID is invalid'
