from django_openx.client import OpenXClient
from django_openx.data import OpenXObject

_client = OpenXClient().zone
_cache = {}

class Zone(OpenXObject):
	def add(self):
		self['zoneId'] = _client.addZone(dict(self))
	def delete(self):
		_client.deleteZone(self['zoneId'])
	def modify(self):
		_client.modifyZone(dict(self))
	@staticmethod
	def get(zone_id):
		if not zone_id in _cache:
			_cache[zone_id] = Zone(_client.getZone(zone_id))
		return _cache[zone_id]
	@staticmethod
	def get_for_publisher(publisher):
		from publisher import Publisher
		if isinstance(publisher, Publisher):
			publisher = publisher['publisherId']
		zones = _client.getZoneListByPublisherId(publisher)
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
		_client.linkBanner(self['zoneId'], banner)
	linkBanner = link_banner
	def unlink_banner(self, banner):
		from banner import Banner
		if isinstance(banner, Banner):
			banner = banner['bannerId']
		_client.unlinkBanner(self['zoneId'], banner)
	unlinkBanner = unlink_banner
	def link_campaign(self, campaign):
		from campaign import Campaign
		if isinstance(campaign, Campaign):
			campaign = campaign['campaignId']
		_client.linkCampaign(self['zoneId'], campaign)
	linkCampaign = link_campaign
	def unlink_campaign(self, campaign):
		from campaign import Campaign
		if isinstance(campaign, Campaign):
			campaign = campaign['campaignId']
		_client.unlinkCampaign(self['zoneId'], campaign)
	unlinkCampaign = unlink_campaign
	def generate_tag(self, code_type='adjs', params=[]):
		return _client.generateTags(self['zoneId'], code_type, params)
	generate_tags = generate_tag
	generateTags = generate_tag
	class Meta:
		fields = ['block', 'capping', 'comments', 'height', 'publisherId', 'sessionCapping', 'type', 'width', 'zoneId', 'zoneName']

