from datetime import date, timedelta

def object_property(field_key):
	def setter(self, value):
		self._openx_data[field_key] = value
	def getter(self):
		return self._openx_data.get(field_key, None)
	return property(getter, setter)

def object_daily_statistics(call):
	def _return_daily_statistics(self, start=None, end=None):
		if start is None:
			start = date.today()
		if end is None:
			end = start
		return getattr(self.__class__._client, call)(self.id, start, end)
	return _return_daily_statistics

class OpenXObjectMeta(type):
	def __new__(cls, name, bases, attrs):
		if 'Meta' in attrs:
			meta = attrs.pop('Meta')
			
			fields = getattr(meta, 'fields', {})
			for key, name in fields.items():
				attrs[key] = object_property(name)
				attrs[name] = object_property(name)
			attrs['_openx_fields'] = fields
			
			daily_statistics = getattr(meta, 'daily_statistics', {})
			for key, name in daily_statistics.items():
				attrs[key] = object_daily_statistics(name)
			attrs['_openx_daily_statistics'] = fields
		
		return super(OpenXObjectMeta, cls).__new__(cls, name, bases, attrs)

class OpenXObjectBase(object):
	def __init__(self, data = {}):
		self._openx_data = data
	def __getitem__(self, name):
		if name in self._openx_fields:
			name = self._openx_fields[name]
		return self._openx_data.get(name, None)
	def __setitem__(self, name, value):
		if name in self._openx_fields:
			name = self._openx_fields[name]
		self._openx_data[name] = value

class OpenXObject(OpenXObjectBase):
	__metaclass__ = OpenXObjectMeta

if __name__ == '__main__':
	class Test(OpenXObject):
		class Meta:
			fields = {
				'advertiser_id': 'advertiserId',
			}
	obj = Test()
	print dir(obj)
	print obj.advertiser_id
	print obj.advertiserId
	print obj['advertiser_id']
	print obj['advertiserId']
	obj.advertiser_id = 15
	print obj.advertiser_id
	print obj.advertiserId
	print obj['advertiser_id']
	print obj['advertiserId']
	obj.advertiserId = 16
	print obj.advertiser_id
	print obj.advertiserId
	print obj['advertiser_id']
	print obj['advertiserId']
	obj['advertiser_id'] = 17
	print obj.advertiser_id
	print obj.advertiserId
	print obj['advertiser_id']
	print obj['advertiserId']
	obj['advertiserId'] = 18
	print obj.advertiser_id
	print obj.advertiserId
	print obj['advertiser_id']
	print obj['advertiserId']

