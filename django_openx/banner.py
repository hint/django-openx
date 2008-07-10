from client import OpenXClient

_client = OpenXClient().banner

class Banner(dict):
	def __init__(self, data={}, **kwargs):
		data.update(kwargs)
		if 'aImage' in data and not isinstance(data['aImage'], dict):
			del data['aImage']
		super(Banner, self).__init__(data)
	def add(self):
		self['bannerId'] = _client.addBanner(dict(self))
		if 'aImage' in self:
			del self['aImage']
	def delete(self):
		_client.deleteBanner(self['bannerId'])
	def modify(self):
		_client.modifyBanner(dict(self))
		if 'aImage' in self:
			del self['aImage']
	@staticmethod
	def get(publisher_id):
		return Banner(_client.getBanner(publisher_id))
	@staticmethod
	def get_for_campaign(campaign):
		from campaign import Campaign
		if isinstance(campaign, Campaign):
			campaign = campaign['campaignId']
		banners = _client.getBannerListByCampaignId(campaign)
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
	def unlink_zone(self, zone):
		from zone import Zone
		if not isinstance(zone, Zone):
			zone = Zone.get(zone)
		return zone.unlink_banner(self)
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
