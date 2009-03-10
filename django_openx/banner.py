from django_openx.client import OpenXClient
from django_openx.data import OpenXObject

class Banner(OpenXObject):
	_client = OpenXClient().banner
	_cache = {}
	
	def __init__(self, data={}, **kwargs):
		data.update(kwargs)
		if 'aImage' in data and not isinstance(data['aImage'], dict):
			del data['aImage']
		super(Banner, self).__init__(data)
	def add(self):
		self['bannerId'] = Banner._client.addBanner(self._openx_data)
		if 'aImage' in self:
			del self['aImage']
	def delete(self):
		Banner._client.deleteBanner(self['bannerId'])
		self['bannerId'] = None
	def modify(self):
		Banner._client.modifyBanner(self._openx_data)
		if 'aImage' in self:
			del self['aImage']
	@staticmethod
	def get(banner_id):
		if not banner_id in Banner._cache:
			Banner._cache[banner_id] = Banner(Banner._client.getBanner(banner_id))
		return Banner._cache[banner_id]
	@staticmethod
	def get_for_campaign(campaign):
		from campaign import Campaign
		if isinstance(campaign, Campaign):
			campaign = campaign['campaignId']
		banners = Banner._client.getBannerListByCampaignId(campaign)
		if banners:
			return [Banner(d) for d in banners]
		else:
			return []
	@property
	def campaign(self):
		from campaign import Campaign
		return Campaign.get(self['campaignId'])
	def link_zone(self, zone):
		from zone import Zone
		if not isinstance(zone, Zone):
			zone = Zone.get(zone)
		return zone.link_banner(self)
	linkZone = link_zone
	def unlink_zone(self, zone):
		from zone import Zone
		if not isinstance(zone, Zone):
			zone = Zone.get(zone)
		return zone.unlink_banner(self)
	unlinkZone = unlink_zone
	def set_image_raw(self, filename, content, editswf=False):
		import xmlrpclib
		self['aImage'] = {
			'filename': filename,
			'content': xmlrpclib.Binary(content),
			'editswf': editswf,
		}
	def set_image(self, filename, editswf=False):
		import os.path
		if not os.path.exists(filename):
			raise Exception
		basename = os.path.basename(filename)
		fh = open(filename, 'rb')
		content = fh.read()
		fh.close()
		self.set_image_raw(basename, content, editswf)
	def get_targeting(self):
		return Banner._client.getBannerTargeting(self.id)
	def set_targeting(self, targeting):
		# TODO: Validate value and test method
		return Banner._client.setBannerTargeting(self.id)
	class Meta:
		fields = {
			'id': 'bannerId',
			'name': 'bannerName',
			'text': 'bannerText',
			'a_backup_image': 'aBackupImage',
			'adserver': 'adserver',
			'a_image': 'aImage',
			'banner_id': 'bannerId',
			'banner_name': 'bannerName',
			'banner_text': 'bannerText',
			'block': 'block',
			'campaign_id': 'campaignId',
			'capping': 'capping',
			'comments': 'comments',
			'height': 'height',
			'html_template': 'htmlTemplate',
			'image_url': 'imageURL',
			'session_capping': 'sessionCapping',
			'status': 'status',
			'storage_type': 'storageType',
			'target': 'target',
			'transparent': 'transparent',
			'url': 'url',
			'weight': 'weight',
			'width': 'width',
		}
		daily_statistics = {
			'daily_statistics': 'bannerDailyStatistics',
			'dailyStatistics': 'bannerDailyStatistics',
			'publisher_statistics': 'bannerPublisherStatistics',
			'publisherStatistics': 'bannerPublisherStatistics',
			'zone_statistics': 'bannerZoneStatistics',
			'zoneStatistics': 'bannerZoneStatistics',
		}

