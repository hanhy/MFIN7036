#!/bin/bash

# Apple script path
APPLESCRIPT_PATH="$HOME/Scripts/connect_hotspot.scpt"

# Check current Wi-Fi connection status
check_connection() {
    HOTSPOT_NAME="Harry"
    CURRENT_NETWORK=$(networksetup -getairportnetwork en0 | awk -F": " '{print $2}')
    if [ "$CURRENT_NETWORK" = "$HOTSPOT_NAME" ]; then
        return 0  # Connected
    else
        return 1  # Not connected
    fi
}

# Main loop
while true
do
    if ! check_connection; then
        echo "$(date): Not connected to iPhone hotspot，trying..."
        # Use osascript to run AppleScript
        RESULT=$(osascript "$APPLESCRIPT_PATH")
        echo "$(date): $RESULT"
    else
        echo "$(date): Connected to iPhone hotspot"
    fi
    
    # Check every 5 seconds
    sleep 5
done
