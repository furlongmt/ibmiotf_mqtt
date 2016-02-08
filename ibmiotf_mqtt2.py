import ibmiotf.application
import ibmiotf.device
import os
import time
import json
	
def run_mqtt():
	if "VCAP_APPLICATION" in os.environ:
		application = json.loads(os.getenv('VCAP_APPLICATION'))
		service = json.loads(os.getenv('VCAP_SERVICES'))

		uri = application["application_uris"][0]
		
		# Check we have an IoT Foundation service bound
		if "iotf-service" not in service:
			print(" IoT Foundation service has not been bound!")
			raise Exception("IoT Foundation service has not been bound!")
			
		organization = service['iotf-service'][0]['credentials']['org']
		authKey = service['iotf-service'][0]['credentials']['apiKey']
		authToken = service['iotf-service'][0]['credentials']['apiToken']
	else:
		# Not running in Bluemix, so you need to set up your own properties for local testing.
		# Ensure you blank these out before committing/uploading the code
		uri = "localhost"

		organization = "ysc02b"
		authKey = "a-ysc02b-ws6jxd9zbd"
		authToken = "eakFKP_Z!HMHgp2i6Q"
		
	authMethod = "apikey"

	def myEventCallback(event):
		str = "%s event '%s' received from device [%s]: %s"
		print(str % (event.format, event.event, event.device, json.dumps(event.data)))


	appId = "test_device1894342"

	try: 
		options = {
			"org": organization,
			"id": appId,
			"auth-method": authMethod,
			"auth-key": authKey,
			"auth-token": authToken
		}
		subscriber = ibmiotf.application.Client(options)
	except ibmiotf.ConnectionException as e:
		print "Error in connecting to application"

	otherDeviceId = "test_app1"
	subscriber.connect()
	subscriber.deviceEventCallback = myEventCallback
	subscriber.subscribeToDeviceEvents(otherDeviceId)

	deviceId = "test_app2"
	deviceType = "test_app2"
	authMethod = "token"
	authToken = "ioWf6L2IMV*RyADqKI"
	myQosLevel = 1

	try: 
		options = {
			"org": organization,
			"type": deviceType,
			"id": deviceId,
			"auth-method": authMethod,
			"auth-token": authToken
		}
		publisher = ibmiotf.device.Client(options)
	except ibmiotf.ConnectionException as e:
		print "Device connection failed"

	publisher.connect()

	flo = float(3.4563789)

	'''
		Important Note: If the qos level is not set to 1, then not all 1000 messages will be published
	'''
	for x in range (1,1001):
		data = { 'attempting to publish' : 'new event that should be picked up from the other device', 'x' : x, 'float': flo}
		publisher.publishEvent("greeting", "json", data, myQosLevel)
		time.sleep(2)
				
	time.sleep(10)
	# Disconnect the device and application from the cloud
	publisher.disconnect()
	subscriber.disconnect()

if __name__ == '__main__':
	run_mqtt()
