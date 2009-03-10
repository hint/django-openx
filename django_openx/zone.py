from django_openx.client import OpenXClient
from django_openx.data import OpenXObject

class Zone(OpenXObject):
	_client = OpenXClient().zone
	_cache = {}
	
	def add(self):
		self['zoneId'] = Zone._client.addZone(self._openx_data)
	def delete(self):
		Zone._client.deleteZone(self['zoneId'])
		self['zoneId'] = None
	def modify(self):
		Zone._client.modifyZone(self._openx_data)
	@staticmethod
	def get(zone_id):
		if not zone_id in Zone._cache:
			Zone._cache[zone_id] = Zone(Zone._client.getZone(zone_id))
		return Zone._cache[zone_id]
	@staticmethod
	def get_for_publisher(publisher):
		from publisher import Publisher
		if isinstance(publisher, Publisher):
			publisher = publisher['publisherId']
		zones = Zone._client.getZoneListByPublisherId(publisher)
		if zones:
			return [Zone(d) for d in zones]
		else:
			return []
	@property
	def publisher(self):
		from publisher import Publisher
		return Publisher.get(self['publisherId'])
	def link_banner(self, banner):
		from banner import Banner
		if isinstance(banner, Banner):
			banner = banner['bannerId']
		Zone._client.linkBanner(self['zoneId'], banner)
	linkBanner = link_banner
	def unlink_banner(self, banner):
		from banner import Banner
		if isinstance(banner, Banner):
			banner = banner['bannerId']
		Zone._client.unlinkBanner(self['zoneId'], banner)
	unlinkBanner = unlink_banner
	def link_campaign(self, campaign):
		from campaign import Campaign
		if isinstance(campaign, Campaign):
			campaign = campaign['campaignId']
		Zone._client.linkCampaign(self['zoneId'], campaign)
	linkCampaign = link_campaign
	def unlink_campaign(self, campaign):
		from campaign import Campaign
		if isinstance(campaign, Campaign):
			campaign = campaign['campaignId']
		Zone._client.unlinkCampaign(self['zoneId'], campaign)
	unlinkCampaign = unlink_campaign
	def generate_tag(self, code_type='adjs', params=[]):
		return Zone._client.generateTags(self['zoneId'], code_type, params)
	generate_tags = generate_tag
	generateTags = generate_tag
	class Meta:
		fields = {
			'id': 'zoneId',
			'name': 'zoneName',
			'block': 'block',
			'capping': 'capping',
			'comments': 'comments',
			'height': 'height',
			'publisher_id': 'publisherId',
			'session_capping': 'sessionCapping',
			'type': 'type',
			'width': 'width',
			'zone_id': 'zoneId',
			'zone_name': 'zoneName',
		}
		daily_statistics = {
			'daily_statistics': 'zoneDailyStatistics',
			'dailyStatistics': 'zoneDailyStatistics',
			'advertiser_statistics': 'zoneAdvertiserStatistics',
			'advertiserStatistics': 'zoneAdvertiserStatistics',
			'campaign_statistics': 'zoneCampaignStatistics',
			'campaignStatistics': 'zoneCampaignStatistics',
			'banner_statistics': 'zoneBannerStatistics',
			'bannerStatistics': 'zoneBannerStatistics',
		}

