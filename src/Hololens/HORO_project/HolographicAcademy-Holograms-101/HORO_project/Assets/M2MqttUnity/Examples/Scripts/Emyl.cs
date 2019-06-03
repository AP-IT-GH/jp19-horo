using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using M2MqttUnity;

namespace M2MqttUnity.Examples
{
    public class Emyl : M2MqttUnityClient
    {
        Boolean send = false;
        // Start is called before the first frame update

        protected override void OnConnected()
        {
            base.OnConnected();
            send = true;
            Debug.Log("connected");

        }
        protected override void Start()
        {
            Debug.Log("start is begonnen");
            brokerAddress = "192.168.0.69";
            brokerPort = 1883;
            autoConnect = true;
            base.Start();
            Debug.Log("start is uitgevoerd");
        }

        // Update is called once per frame
        protected override void Update()
        {
            base.Update();
            if (client != null)
            {
                if (send){
                    Coordinaten coordinaten = new Coordinaten();
                    coordinaten.Y = 12;
                    coordinaten.X = 23;
                    string json = JsonUtility.ToJson(coordinaten);
                    client.Publish("test_channel", System.Text.Encoding.UTF8.GetBytes(json), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, false);
                    Debug.Log("tis verzonden");
                    send = false;
                }
                
            }
        }
    }
    public class Coordinaten
    {
        public int X;
        public int Y;
    }
}