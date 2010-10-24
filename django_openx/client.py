import xmlrpclib
from django.conf import settings

class OpenXClient(object):
	def __init__(self):
		self.__session = None
	@property
	def _session(self):
		if self.__session is None:
			s = xmlrpclib.ServerProxy(settings.OPENX_URL)
			self.__session = s.ox.logon(settings.OPENX_USERNAME, settings.OPENX_PASSWORD)
		return self.__session
	def _renew_session(self):
		self.__session = None
	def __getattr__(self, name):
		return OpenXServiceClientWrapper(self)

class OpenXServiceClientWrapper(object):
	def __init__(self, client):
		self._client = client
		self._xmlrpc_client = xmlrpclib.ServerProxy(settings.OPENX_URL)
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
			return self._xmlrpc_method(self ._client._session, *args, **kwargs)
		except:
			self ._client._renew_session()
			try:
				return self._xmlrpc_method(self._client.ox._session, *args, **kwargs)
			except:
				raise # Exception

