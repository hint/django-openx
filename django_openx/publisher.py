from django_openx.client import OpenXClient
from django_openx.data import OpenXObject

_client = OpenXClient().publisher
_cache = {}

class Publisher(OpenXObject):
	def add(self):
		self['publisherId'] = _client.addPublisher(dict(self))
	def delete(self):
		_client.deletePublisher(self['publisherId'])
		self['publisherId'] = None
	def modify(self):
		_client.modifyPublisher(dict(self))
	@staticmethod
	def get(publisher_id):
		if not publisher_id in _cache:
			_cache[publisher_id] = Publisher(_client.getPublisher(publisher_id))
		return _cache[publisher_id]
	@staticmethod
	def get_for_agency(agency):
		from agency import Agency
		if isinstance(agency, Agency):
			agency = agency['agencyId']
		publishers = _client.getPublisherListByAgencyId(agency)
		if publishers:
			return [Publisher(d) for d in publishers]
		else:
			return []
	@property
	def agency(self):
		from agency import Agency
		return Agency.get(self['agencyId'])
	@property
	def zones(self):
		from zone import Zone
		return Zone.get_for_publisher(self)
	class Meta:
		fields = {
			'id': 'publisherId',
			'name': 'publisherName',
			'account_id': 'accountId',
			'agency_id': 'agencyId',
			'comments': 'comments',
			'contact_name': 'contactName',
			'email_address': 'emailAddress',
			'publisher_id': 'publisherId',
			'publisher_name': 'publisherName',
		}

