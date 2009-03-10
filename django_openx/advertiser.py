from django_openx.client import OpenXClient
from django_openx.data import OpenXObject

class Advertiser(OpenXObject):
	_client = OpenXClient().advertiser
	_cache = {}
	
	def add(self):
		self['advertiserId'] = Advertiser._client.addAdvertiser(self._openx_data)
	def delete(self):
		Advertiser._client.deleteAdvertiser(self['advertiserId'])
		self['advertiserId'] = None
	def modify(self):
		self._client.modifyAdvertiser(self._openx_data)
	@staticmethod
	def get(advertiser_id):
		if not advertiser_id in Advertiser._cache:
			Advertiser._cache[advertiser_id] = Advertiser(Advertiser._client.getAdvertiser(advertiser_id))
		return Advertiser._cache[advertiser_id]
	@staticmethod
	def get_for_agency(agency):
		from agency import Agency
		if isinstance(agency, Agency):
			agency = agency['agencyId']
		advertisers = Advertiser._client.getAdvertiserListByAgencyId(agency)
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
		daily_statistics = {
			'daily_statistics': 'advertiserDailyStatistics',
			'dailyStatistics': 'advertiserDailyStatistics',
			'campaign_statistics': 'advertiserCampaignStatistics',
			'campaignStatistics': 'advertiserCampaignStatistics',
			'banner_statistics': 'advertiserBannerStatistics',
			'bannerStatistics': 'advertiserBannerStatistics',
			'publisher_statistics': 'advertiserPublisherStatistics',
			'publisherStatistics': 'advertiserPublisherStatistics',
			'zone_statistics': 'advertiserZoneStatistics',
			'zoneStatistics': 'advertiserZoneStatistics',
		}

