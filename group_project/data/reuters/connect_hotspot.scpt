tell application "System Events"
    tell process "SystemUIServer"
	-- Click Wi-Fi menu icon
        set wifiMenu to menu bar item 1 of menu bar 1 whose description contains "Wi-Fi"
        click wifiMenu
        
        -- Wait for the menu to expand
        delay 1
        
        -- Choose iPhone hotspot
        set hotspotName to "Harry"
        try
            click menu item hotspotName of menu 1 of wifiMenu
            delay 2 -- Wait to connect
            return "Succeed to connect to " & hotspotName
        on error
            return "Can't find hotspot " & hotspotName & ", please check iPhone whether the hotspot is avaliable"
        end try
    end tell
end tell
