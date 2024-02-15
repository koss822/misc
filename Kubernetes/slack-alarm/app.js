/*
info 2024-02-11 13:35:06MQTT publish: topic 'zigbee2mqtt/0x142d41fffe5820ac', payload '{"battery":100,"battery_low":false,"contact":false,"linkquality":255,"tamper":false,"update":{"installed_version":16777241,"latest_version":16777241,"state":"idle"}}'
info 2024-02-11 13:35:08MQTT publish: topic 'zigbee2mqtt/0x142d41fffe5820ac', payload '{"battery":100,"battery_low":false,"contact":true,"linkquality":255,"tamper":false,"update":{"installed_version":16777241,"latest_version":16777241,"state":"idle"}}'
*/

const { App } = require('@slack/bolt');
var enabled = false;


const mqttServer = process.env.MQTT_SERVER;
const mqttTopic = process.env.MQTT_TOPIC;
const mqtt = require('mqtt');
const client = mqtt.connect(mqttServer);

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
  // Socket Mode doesn't listen on a port, but in case you want your app to respond to OAuth,
  // you still need to listen on some port!
  port: process.env.PORT || 3000
});

// Listens to incoming messages that contain "hello"
app.message('hello', async ({ message, say }) => {
  // say() sends a message to the channel where the event was triggered
  await say({
    blocks: [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": `Hey there <@${message.user}>!`
        },
        "accessory": {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Click Me"
          },
          "action_id": "button_click"
        }
      }
    ],
    text: `Hey there <@${message.user}>!`
  });
});

app.message('alarm', async ({ message, say }) => {
    // say() sends a message to the channel where the event was triggered
    await say({
      blocks: [
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Alarm"
			},
			"accessory": {
				"type": "radio_buttons",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "enable"
						},
						"value": "enable"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "disable"
						},
						"value": "disable"
					}
				],
				"action_id": "alarm"
			}
		}
      ],
      text: `Hey there <@${message.user}>!`
    });
  });

  app.action('alarm', async ({ body, ack, say }) => {
    // Acknowledge the action
    let enabledValue = body.actions[0].selected_option.value;
    await ack();
    await say(`<@${body.user.id}> alarm ${enabledValue}`);
    enabled = enabledValue == 'enable' ? true : false;
  });

client.on('connect', () => {
    console.log('Connected to MQTT Broker');
    
    client.subscribe(mqttTopic, function (err) {
      if (!err) {
        console.log(`Subscribed to topic ${mqttTopic}`);
      } else {
        console.log(`Failed to subscribe to topic ${mqttTopic}`);
      }
    });
  });
  
client.on('message', (topic, message) => {
if (topic === mqttTopic && enabled) {
    const data = JSON.parse(message);
    console.log("Contact: ", data.contact);
    app.client.chat.postMessage({channel:"home", text:`Door ${data.contact ? "closed": "opened"}`})
}
});


(async () => {
  // Start your app
  await app.start();
  await app.client.chat.postMessage({channel:"home", text:"Alarm started in disabled state, type alarm to change"})
  console.log('⚡️ Alarm app is running!');
})();