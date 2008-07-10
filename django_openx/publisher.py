from client import OpenXClient

_client = OpenXClient().publisher

class Publisher(dict):
	def add(self):
		self['publisherId'] = _client.addPublisher(dict(self))
	def delete(self):
		_client.deletePublisher(self['publisherId'])
	def modify(self):
		_client.modifyPublisher(dict(self))
	@staticmethod
	def get(publisher_id):
		return Publisher(_client.getPublisher(publisher_id))
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

