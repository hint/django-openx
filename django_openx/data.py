def object_property(field_name):
	def setter(self, value):
		self._field_dict[field_name] = value
	def getter(self):
		return self._field_dict.get(field_name, None)
	return property(getter, setter)

class OpenXObjectMeta(type):
	def __new__(cls, name, bases, attrs):
		if 'Meta' in attrs:
			meta = attrs.pop('Meta')
			
			fields = getattr(meta, 'fields', [])
			for field in fields:
				attrs[field] = object_property(field)
		
		return super(OpenXObjectMeta, cls).__new__(cls, name, bases, attrs)

class OpenXObjectBase(object):
	def __init__(self):
		self._field_dict = {}
	def __getitem__(self, name):
		return self._field_dict.get(name, None)
	def __setitem__(self, name, value):
		self._field_dict[name] = value

class OpenXObject(OpenXObjectBase):
	__metaclass__ = OpenXObjectMeta

