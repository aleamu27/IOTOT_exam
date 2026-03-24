# IOTOT_exam
Exam in IOTOT security at Kristiania

Some key takeaways from the exam. 
- Threat modelling a real device with no source code forces you to think 
  like an attacker, not a developer

- MQTT's biggest problem isn't a bug – it was designed without security 
  in mind, and most deployments never fix that

- Building something vulnerable on purpose and attacking it yourself 
  teaches more than any textbook scenario

- The most dangerous trust boundary is rarely the obvious one – 
  on the Garmin it's the BLE channel, not the cloud
