from client import OpenXClient

_client = OpenXClient().advertiser

class Advertiser(dict):
	def add(self):
		self['advertiserId'] = _client.addAdvertiser(dict(self))
	def delete(self):
		_client.deleteAdvertiser(self['advertiserId'])
	def modify(self):
		_client.modifyAdvertiser(dict(self))
	@staticmethod
	def get(publisher_id):
		return Advertiser(_client.getAdvertiser(publisher_id))
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
