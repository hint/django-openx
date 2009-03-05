from django_openx.client import OpenXClient
from django_openx.data import OpenXObject

_client = OpenXClient().advertiser
_cache = {}

class Advertiser(OpenXObject):
	def add(self):
		self['advertiserId'] = _client.addAdvertiser(dict(self))
	def delete(self):
		_client.deleteAdvertiser(self['advertiserId'])
		self['advertiserId'] = None
	def modify(self):
		_client.modifyAdvertiser(dict(self))
	@staticmethod
	def get(advertiser_id):
		if not advertiser_id in _cache:
			_cache[advertiser_id] = Advertiser(_client.getAdvertiser(advertiser_id))
		return _cache[advertiser_id]
	@staticmethod
	def get_for_agency(agency):
		from agency import Agency
		if isinstance(agency, Agency):
			agency = agency['agencyId']
		advertisers = _client.getAdvertiserListByAgencyId(agency)
		if advertisers:
			return [Advertiser(d) for d in advertisers]
		else:
			return []
	@property
	def agency(self):
		from agency import Agency
		return Agency.get(self['agencyId'])
	@property
	def campaigns(self):
		from campaign import Campaign
		return Campaign.get_for_advertiser(self)
	class Meta:
		fields = {
			'id': 'advertiserId',
			'name': 'advertiserName',
			'account_id': 'accountId',
			'advertiser_id': 'advertiserId',
			'advertiser_name': 'advertiserName',
			'agency_id': 'agencyId',
			'comments': 'comments',
			'contact_name': 'contactName',
			'email_address': 'emailAddress',
		}

