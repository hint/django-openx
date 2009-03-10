from django_openx.client import OpenXClient
from django_openx.data import OpenXObject

class Agency(OpenXObject):
	_client = OpenXClient().agency
	_cache = {}
	
	def add(self):
		self['agencyId'] = Agency._client.addAgency(self._openx_data)
	def delete(self):
		Agency._client.deleteAgency(self['agencyId'])
		self['agencyId'] = None
	def modify(self):
		Agency._client.modifyAgency(self._openx_data)
	@staticmethod
	def get(agency_id):
		if not agency_id in Agency._cache:
			Agency._cache[agency_id] = Agency(Agency._client.getAgency(agency_id))
		return Agency._cache[agency_id]
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
			'id': 'agencyId',
			'name': 'agencyName',
			'account_id': 'accountId',
			'agency_id': 'agencyId',
			'agency_name': 'agencyName',
			'contact_name': 'contactName',
			'email_address': 'emailAddress',
			'password': 'password',
		}
		daily_statistics = {
			'daily_statistics': 'foobarDailyStatistics',
			'dailyStatistics': 'foobarDailyStatistics',
			'advertiser_statistics': 'foobarAdvertiserStatistics',
			'advertiserStatistics': 'foobarAdvertiserStatistics',
			'campaign_statistics': 'foobarCampaignStatistics',
			'campaignStatistics': 'foobarCampaignStatistics',
			'banner_statistics': 'foobarBannerStatistics',
			'bannerStatistics': 'foobarBannerStatistics',
			'publisher_statistics': 'foobarPublisherStatistics',
			'publisherStatistics': 'foobarPublisherStatistics',
			'zone_statistics': 'foobarZoneStatistics',
			'zoneStatistics': 'foobarZoneStatistics',
		}

