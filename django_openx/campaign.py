from client import OpenXClient

_client = OpenXClient().campaign
_cache = {}

class Campaign(dict):
	def add(self):
		self['campaignId'] = _client.addCampaign(dict(self))
	def delete(self):
		_client.deleteCampaign(self['campaignId'])
	def modify(self):
		_client.modifyCampaign(dict(self))
	@staticmethod
	def get(campaign_id):
		if not campaign_id in _cache:
			_cache[campaign_id] = Campaign(_client.getCampaign(campaign_id))
		return _cache[campaign_id]
	@staticmethod
	def get_for_advertiser(advertiser):
		from advertiser import Advertiser
		if isinstance(advertiser, Advertiser):
			advertiser = advertiser['advertiserId']
		campaigns = _client.getCampaignListByAdvertiserId(advertiser)
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
