from envfiles.envfiles import EnvFilesError, load


__version__ = "0.1.0"

__title__ = "envfiles"
__description__ = "Simple layered loading of env files for your 12-factor app."
__url__ = "https://github.com/yeraydiazdiaz/envfiles"
__uri__ = __url__
__doc__ = __description__ + " <" + __uri__ + ">"

__author__ = "Yeray Díaz Díaz"
__email__ = "yeraydiazdiaz@gmail.com"

__license__ = "Apache 2.0"
__copyright__ = "Copyright (c) 2019 Yeray Díaz Díaz"

__all__ = ["load", "EnvFilesError"]
