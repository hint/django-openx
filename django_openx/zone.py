from client import OpenXClient

_client = OpenXClient().zone

class Zone(dict):
	def add(self):
		self['zoneId'] = _client.addZone(dict(self))
	def delete(self):
		_client.deleteZone(self['zoneId'])
	def modify(self):
		_client.modifyZone(dict(self))
	@staticmethod
	def get(publisher_id):
		return Zone(_client.getZone(publisher_id))
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
	def unlink_banner(self, banner):
		from banner import Banner
		if isinstance(banner, Banner):
			banner = banner['bannerId']
		_client.unlinkBanner(self['zoneId'], banner)
	def link_campaign(self, campaign):
		from campaign import Campaign
		if isinstance(campaign, Campaign):
			campaign = campaign['campaignId']
		_client.linkCampaign(self['zoneId'], campaign)
	def unlink_campaign(self, campaign):
		from campaign import Campaign
		if isinstance(campaign, Campaign):
			campaign = campaign['campaignId']
		_client.unlinkCampaign(self['zoneId'], campaign)
	def generate_tags(self, code_type='adjs', params=[]):
		return _client.generateTags(self['zoneId'], code_type, params)