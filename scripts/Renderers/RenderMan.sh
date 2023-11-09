export "DEFAULT_RENDERER=prman"

export "PIXAR_LICENSE_FILE=/opt/pixar/pixar.license"

# -- Location of the RenderMan Pro Server installation --
export "RMANTREE=/opt/pixar/RenderManProServer-$RENVER"

# -- Location of the PRman plugin for KATANA --
export "RFKTREE=/opt/pixar/RenderManForKatana-$RENVER/plugins/katana$KATANA_LINE"

# -- This is what is required to load the RfK plugin --
export "KATANA_RESOURCES=$KATANA_RESOURCES:$RFKTREE"

export "RMAN_SHADERPATH=$RMANTREE/lib/shad"
export "RMAN_RIXPLUGINPATH=$RMAN_RIXPLUGINPATH:$RMANTREE/lib/plugins"

export "PATH=$PATH:$KATANA_ROOT/bin"
