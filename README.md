# Katana Launcher
This launcher allows you to manage all versions of Katana with any optional enviornment variables you may use.


## Set-up
The paths the launcher searches are defined in the config.ini file and need to be modified to your machines paths.


## Multiple 3Delight Versions
The launcher can detect multiple versions of 3Delight installed. You may specify which version can be used with which version of Katana by adding it to the end of the 3Delight folder.
```
C:\Program Files\3Delight_6.0v2
```


## Adding Custom Enviornment Variables
You may add any .bat file into the scripts folder and it will be populated as a selection upon refresh. 


## Renderers
You can add additional renderers by adding a .bat file in the renderers folder and will appear in the appropriate dropdown. 
*The renderer version functionality will be disabled when using other custom renderer scripts.*


## Available Enviornment Variables
There are few enviornment variables generated to use for custom scripts:

**KATANA_VERSION** - Full Katana version. `6.0v2`

**KATANA_LINE** - The major Katana version. `6.0`

**KATANA_ROOT** - The full path to the selected Katana. `C:\Program Files\Katana6.0v2`
