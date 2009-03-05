#from django.db.models import signals
from django.db.models.fields import PositiveIntegerField
from django.utils.translation import ugettext_lazy as _

class OpenXFieldBase(PositiveIntegerField):
	def __init__(self, *args, **kwargs):
		kwargs['blank'] = kwargs.get('null', True)
		kwargs['blank'] = kwargs.get('blank', True)
		super(OpenXFieldBase, self).__init__(*args, **kwargs)
	
	def contribute_to_class(self, cls, name):
		super(OpenXFieldBase, self).contribute_to_class(cls, name)
		setattr(cls, self.name, self)
		#signals.post_save.connect(self._save, cls, True)
	
	def __get__(self, instance, owner=None):
		if instance is None:
			raise AttributeError(_('%s can only get value on instances.') % self.name)
		obj = self._get_instance_cache(instance)
		if isinstance(obj, (int, long)):
			obj = self._openx_class.get(obj)
			self._set_instance_cache(instance, obj)
		return obj
	
	def __set__(self, instance, value):
		if instance is None:
			raise AttributeError(_('%s can only be set on instances.') % self.name)
		if not value is None and not isinstance(value, (self._openx_class, int, long)):
			raise AttributeError(_('%s can only be set to defined type.') % self.name)
		self._set_instance_cache(instance, value)
	
	#def _save(self, **kwargs): #signal, sender, instance):
		#perhaps save advertiser back to openx
	
	def __delete__(self, instance):
		self._set_instance_cache(instance, None)
	
	def _get_instance_cache(self, instance):
		return getattr(instance, '_%s_cache' % self.attname, None)
	
	def _set_instance_cache(self, instance, value):
		setattr(instance, '_%s_cache' % self.attname, value)
	
	def get_internal_type(self):
		return 'PositiveIntegerField'
	
	def to_python(self, value):
		if value is None or value is 0:
			return None
		if isinstance(value, self._openx_class):
			return int(value.id)
		else:
			try:
				return int(value)
			except ValueError:
				return None
	
	_openx_class = None

class AdvertiserField(OpenXFieldBase):
	from django_openx import Advertiser as _openx_class

class AgencyField(OpenXFieldBase):
	from django_openx import Agency as _openx_class

class BannerField(OpenXFieldBase):
	from django_openx import Banner as _openx_class

class CampaignField(OpenXFieldBase):
	from django_openx import Campaign as _openx_class

class PublisherField(OpenXFieldBase):
	from django_openx import Publisher as _openx_class

class ZoneField(OpenXFieldBase):
	from django_openx import Zone as _openx_class

