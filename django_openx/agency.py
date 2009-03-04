from django_openx.client import OpenXClient
from django_openx.data import OpenXObject

_client = OpenXClient().agency
_cache = {}

class Agency(OpenXObject):
	def add(self):
		self['agencyId'] = _client.addAgency(dict(self))
	def delete(self):
		_client.deleteAgency(self['agencyId'])
	def modify(self):
		_client.modifyAgency(dict(self))
	@staticmethod
	def get(agency_id):
		if not agency_id in _cache:
			_cache[agency_id] = Agency(_client.getAgency(agency_id))
		return _cache[agency_id]
	@property
	def publishers(self):
		from publisher import Publisher
		return Publisher.get_for_agency(self)
	@property
	def advertisers(self):
		from advertiser import Advertiser
		return Advertiser.get_for_agency(self)
	class Meta:
		fields = {
			'account_id': 'accountId',
			'agency_id': 'agencyId',
			'agency_name': 'agencyName',
			'contact_name': 'contactName',
			'email_address': 'emailAddress',
			'password': 'password',
		}

