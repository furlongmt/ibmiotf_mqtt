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
		authMethod = "apikey"
	else:
		# Not running in Bluemix, so you need to set up your own properties for local testing.
		# Ensure you blank these out before committing/uploading the code
		uri = "localhost"

		organization = "ysc02b"
		authKey = "a-ysc02b-2yczllbzpb"
		authToken = "HLqd(O(*h0?izO@fmP"
		authMethod = "apikey"

	def myEventCallback(event):
		str = "%s event '%s' received from device [%s]: %s"
		print(str % (event.format, event.event, event.device, json.dumps(event.data)))

	appId = "test_device189434"

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

	otherDeviceId = "test_app2"
	subscriber.connect()
	subscriber.deviceEventCallback = myEventCallback
	subscriber.subscribeToDeviceEvents(otherDeviceId)

	deviceId = "test_app1"
	deviceType = "test_app1"
	authMethod = "token"
	authToken = "aC)-xfUS13nNWVHvHB"
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
		In this example, the device is publishing 1000 events
		but not all of the callbacks are reached (Discuss with Dr. Remy)
	'''
	for x in range (1,1001):
		data = { 'hello' : 'world this is a really long string to test how much data can be sent across mqtt successfully before it cant keep up any longer', 'x' : x, 'float': flo}
		publisher.publishEvent("greeting", "json", data, myQosLevel)
		time.sleep(2)
		
	time.sleep(10)		
	# Disconnect the device and application from the cloud
	publisher.disconnect()
	subscriber.disconnect()

if __name__ == '__main__':
	run_mqtt()
