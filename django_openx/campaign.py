from django_openx.client import OpenXClient
from django_openx.data import OpenXObject

class Campaign(OpenXObject):
	_client = OpenXClient().campaign
	_cache = {}
	
	def add(self):
		self['campaignId'] = Campaign._client.ox.addCampaign(self._openx_data)
	def delete(self):
		Campaign._client.ox.deleteCampaign(self['campaignId'])
		self['campaignId'] = None
	def modify(self):
		Campaign._client.ox.modifyCampaign(self._openx_data)
	@staticmethod
	def get(campaign_id):
		if not campaign_id in Campaign._cache:
			Campaign._cache[campaign_id] = Campaign(Campaign._client.ox.getCampaign(campaign_id))
		return Campaign._cache[campaign_id]
	@staticmethod
	def get_for_advertiser(advertiser):
		from advertiser import Advertiser
		if isinstance(advertiser, Advertiser):
			advertiser = advertiser['advertiserId']
		campaigns = Campaign._client.ox.getCampaignListByAdvertiserId(advertiser)
		if campaigns:
			return [Campaign(d) for d in campaigns]
		else:
			return []
	@property
	def advertiser(self):
		from advertiser import Advertiser
		return Advertiser.get(self['advertiserId'])
	def link_zone(self, zone):
		from zone import Zone
		if not isinstance(zone, Zone):
			zone = Zone.get(zone)
		return zone.link_campaign(self)
	linkZone = link_zone
	def unlink_zone(self, zone):
		from zone import Zone
		if not isinstance(zone, Zone):
			zone = Zone.get(zone)
		return zone.unlink_campaign(self)
	unlinkZone = unlink_zone
	class Meta:
		fields = {
			'id': 'campaignId',
			'name': 'campaignName',
			'advertiser_id': 'advertiserId',
			'block': 'block',
			'campaign_id': 'campaignId',
			'campaign_name': 'campaignName',
			'capping': 'capping',
			'clicks': 'clicks',
			'comments': 'comments',
			'end_date': 'endDate',
			'impressions': 'impressions',
			'priority': 'priority',
			'revenue': 'revenue',
			'revenue_type': 'revenueType',
			'session_capping': 'sessionCapping',
			'start_date': 'startDate',
			'target_clicks': 'targetClicks',
			'target_conversions': 'targetConversions',
			'target_impressions': 'targetImpressions',
			'weight': 'weight',
		}
		daily_statistics = {
			'daily_statistics': 'campaignDailyStatistics',
			'dailyStatistics': 'campaignDailyStatistics',
			'banner_statistics': 'campaignBannerStatistics',
			'bannerStatistics': 'campaignBannerStatistics',
			'publisher_statistics': 'campaignPublisherStatistics',
			'publisherStatistics': 'campaignPublisherStatistics',
			'zone_statistics': 'campaignZoneStatistics',
			'zoneStatistics': 'campaignZoneStatistics',
		}

