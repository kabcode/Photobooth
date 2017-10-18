##################
# wifi detection #
##################
import wifi
import photobooth_script

# searching for available wifi networks
def searchWifi():
    cells = wifi.Cell.all('wlan0')
    return cells

# select a wifi from list by ssid
def selectFromWifiList(ssid):
    wifilist = searchWifi()

    for cell in wifilist:
        if (cell.ssid == ssid):
            return cell
    print 'Not found: ' + ssid
    return False

# connect to selected wifi
def connectToWifi(ssid, password=None):
    cell = selectFromWifiList(ssid)
    print 'Connecting to...' + cell.ssid

    if cell:
    
        # if wifi is encrypted
        if cell.encrypted:
            photobooth_script.open_input_dialog(cell.ssid)
            if password:
                scheme = addWifi(cell, password)

                try:
                    scheme.activate()

                #wrong password
                except wifi.exceptions.ConnectionsError:
                    return 'Wrong password'
                return cell
            else:
                return 'No password provided'
        
        # no wifi encryption        
        else:
            scheme = addWifi(cell)

            try:
                scheme.activate()
            except wifi.exceptions.ConnectionError:
                return('Connection error')
            return cell

    # no cell returned
    else:
        return 'Selected wifi not found'

# add wifi to known wifi list
def addWifi(cell, password=None):
    if not cell:
        return False

    scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
    scheme.save()
    return scheme

# run wifi-detection directly
if __name__ == '__main__':
    cells = searchWifi()

    i = 0
    for cell in cells:
        print '['+str(i)+']:\t' + cell.ssid
        print '\t\t' + str(cell.quality)
        print '\t\t' + str(cell.signal)
        i=i+1

    # get number from user and try to connect to selected wifi
    
    
    

