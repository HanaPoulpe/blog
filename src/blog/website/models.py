from wagtail.contrib.settings import models as wg_settings


@wg_settings.register_setting
class BlogSettings(wg_settings.BaseGenericSetting):
    pass
