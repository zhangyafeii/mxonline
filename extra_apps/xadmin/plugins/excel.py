# coding:utf-8

from django.template import loader

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView


# excel 导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        nodes.append(
            loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context={'context':context}))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)
