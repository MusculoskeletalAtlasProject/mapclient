import logging
from PyInstaller.utils.hooks import collect_data_files

logger = logging.getLogger(__name__)

logger.info('Loading resources for mapclientplugins.generatesdsstep.')
datas = collect_data_files('mapclientplugins.generatesdsstep.resources')
