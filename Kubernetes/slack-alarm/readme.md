# Notification of IKEA Parasoll door/window sensor to slack

This is a kubernetes deployment written in Javascript (but might be used without Kubernetes) which uses Zigbee2Mqtt to connect IKEA Parasoll window/door sensor and inform you about its state to Slack.

It uses Bolt for slack and you can set-it up following this [**tutorial**](https://slack.dev/bolt-js/tutorial/getting-started)