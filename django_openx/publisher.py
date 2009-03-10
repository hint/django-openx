from django_openx.client import OpenXClient
from django_openx.data import OpenXObject

class Publisher(OpenXObject):
	_client = OpenXClient().publisher
	_cache = {}
	
	def add(self):
		self['publisherId'] = Publisher._client.addPublisher(self._openx_data)
	def delete(self):
		Publisher._client.deletePublisher(self['publisherId'])
		self['publisherId'] = None
	def modify(self):
		Publisher._client.modifyPublisher(self._openx_data)
	@staticmethod
	def get(publisher_id):
		if not publisher_id in Publisher._cache:
			Publisher._cache[publisher_id] = Publisher(Publisher._client.getPublisher(publisher_id))
		return Publisher._cache[publisher_id]
	@staticmethod
	def get_for_agency(agency):
		from agency import Agency
		if isinstance(agency, Agency):
			agency = agency['agencyId']
		publishers = Publisher._client.getPublisherListByAgencyId(agency)
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
		daily_statistics = {
			'daily_statistics': 'publisherDailyStatistics',
			'dailyStatistics': 'publisherDailyStatistics',
			'advertiser_statistics': 'publisherAdvertiserStatistics',
			'advertiserStatistics': 'publisherAdvertiserStatistics',
			'campaign_statistics': 'publisherCampaignStatistics',
			'campaignStatistics': 'publisherCampaignStatistics',
			'banner_statistics': 'publisherBannerStatistics',
			'bannerStatistics': 'publisherBannerStatistics',
			'zone_statistics': 'publisherZoneStatistics',
			'zoneStatistics': 'publisherZoneStatistics',
		}

