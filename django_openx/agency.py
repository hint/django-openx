from client import OpenXClient

_client = OpenXClient().agency

class Agency(dict):
	def add(self):
		self['agencyId'] = _client.addAgency(dict(self))
	def delete(self):
		_client.deleteAgency(self['agencyId'])
	def modify(self):
		_client.modifyAgency(dict(self))
	@staticmethod
	def get(agency_id):
		return Agency(_client.getAgency(agency_id))
	@property
	def publishers(self):
		from publisher import Publisher
		return Publisher.get_for_agency(self)
	@property
	def advertisers(self):
		from advertiser import Advertiser
		return Advertiser.get_for_agency(self)

