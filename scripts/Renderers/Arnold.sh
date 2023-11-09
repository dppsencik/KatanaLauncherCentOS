export "DEFAULT_RENDERER=arnold"
# -- Where you have installed the KtoA plug-in --
export "KTOA_HOME=/home/foundry/ktoa/ktoa-$RENVER-kat$KATANA_LINE-linux"

# -- The KtoA bin folder is needed in PATH --
export "PATH=$PATH:$KTOA_HOME/bin"

# export "solidangle_LICENSE="
# export "ADSKFLEX_LICENSE_FILE="

rem -- This is how to load the KtoA plug-in --
export "KATANA_RESOURCES=$KATANA_RESOURCES:$KTOA_HOME"

# -- USD plugins --
export "path=$KTOA_HOME/USD/KatanaUsdPlugins/lib:$KTOA_HOME/USD/KatanaUsdPlugins/plugin/Libs:$path"
export "KATANA_RESOURCES=$KTOA_HOME/USD/KatanaUsdPlugins/plugin:$KTOA_HOME/USD/KatanaUsdArnold:$KATANA_RESOURCES"
export "PYTHONPATH=$KTOA_HOME/USD/KatanaUsdPlugins/lib/python:$PTHONPATH" 

export "ARNOLD_FNUSDPLUGIN_DIR=$KTOA_HOME/USD/Viewport"
export "FNPXR_PLUGINPATH=$FNPXR_PLUGINPATH:$ARNOLD_FNUSDPLUGIN_DIR"


