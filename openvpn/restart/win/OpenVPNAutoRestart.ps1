echo "Checking connection..."
if (-Not (Test-Connection -ComputerName "YOUR_VPN_SERVER_PRIVATE_IP" -Quiet)){
	echo "Restarting OpenVPN"
	Restart-Service -SERVICENAME OpenVPNService
}
