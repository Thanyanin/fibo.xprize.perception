using UnityEngine;
using System.Collections;
using System.Net;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using uPLibrary.Networking.M2Mqtt.Utility;
using uPLibrary.Networking.M2Mqtt.Exceptions;

using System;

public class mqtest : MonoBehaviour
{
    public GameObject vrcam;
    public GameObject Head;
    public GameObject Body;
    public GameObject shoulderLeft;
    public GameObject shoulderRight;
    public string server_ip = "192.168.2.102";
    private MqttClient client;
    float init_roll = 0;
    float init_pitch = 0;
    float init_yaw = 0;
    int state_start = 0;
    int set_zero = 0;
    float cur_time = 0;
    
    // Use this for initialization
    void Start()
    {
        // create client instance 
        client = new MqttClient(IPAddress.Parse(server_ip), 1883, false, null);

        // register to message received
        client.MqttMsgPublishReceived += client_MqttMsgPublishReceived;

        string clientId = Guid.NewGuid().ToString();
        client.Connect(clientId);

        // subscribe to the topic "/home/temperature" with QoS 2
        client.Subscribe(new string[] { "hello/world" }, new byte[] { MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE });

        StartCoroutine(Example());

    }
    void client_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
    {

        Debug.Log("Received: " + System.Text.Encoding.UTF8.GetString(e.Message));
    }
    string packmsg(Transform obj,bool mode)
    {
        string packed_msg;
        if (mode)
        {
            //rotation pack
            packed_msg = obj.localRotation.x.ToString("F4") + "," + obj.localRotation.y.ToString("F4") + "," + obj.localRotation.z.ToString("F4") + "," + obj.localRotation.w.ToString("F4");
        }
        else
        {
            //translation pack
            packed_msg = obj.localPosition.x.ToString("F4") + "," + obj.localPosition.y.ToString("F4") + "," + obj.localPosition.z.ToString("F4");
        }
        Debug.Log(obj.name + ": " + packed_msg);
        return packed_msg;
    }
   
    void OnGUI()
    {
        if (GUI.Button(new Rect(100, 40, 80, 20), "Send DATA"))
        {
            Debug.Log("Map Ip "+ server_ip);
            Debug.Log("start sending");
            state_start = 1;
            Debug.Log("sent");
        }
        if (GUI.Button(new Rect(180, 40, 80, 20), "Stop"))
        {
            Debug.Log("stop sending...");

            state_start = 0;
            Debug.Log("stop");
        }
    }
    IEnumerator Example()
    {
        cur_time = Time.time;
        yield return 0;
        
        var headrotaion = Head.transform.localRotation;
        var bodyrotaion = Body.transform.localRotation;
        string s_headrotation = headrotaion.x + "," + headrotaion.y + "," + headrotaion.z + "," + headrotaion.w;
        string s_bodyrotation = bodyrotaion.x + "," + bodyrotaion.y + "," + bodyrotaion.z + "," + bodyrotaion.w;

        
        
        var topic_position_roll = "/operator/roll";
        var topic_position_pitch = "/operator/pitch";
        var topic_position_yaw = "/operator/yaw";
        var topic_position_headrotation = "/operator/head/rotation";
        var topic_position_bodyrotation = "/operator/body/rotation";
        var topic_position_shoulderleftrotation = "/operator/shoulderleft/rotation";
        var topic_position_shoulderrightrotation = "/operator/shoulderright/rotation";


        if (state_start == 1)
        {
            //client.Publish(topic_position_headrotation, System.Text.Encoding.UTF8.GetBytes(s_headrotation), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
            client.Publish(topic_position_headrotation, System.Text.Encoding.UTF8.GetBytes(packmsg(Head.transform,true)), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);

            Debug.Log(Head.transform.localEulerAngles);
            //client.Publish(topic_position_rotation, System.Text.Encoding.UTF8.GetBytes(all), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
            //client.Publish(topic_position_headrotation, System.Text.Encoding.UTF8.GetBytes(headWithBody), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
            //client.Publish(topic_position_bodyrotation, System.Text.Encoding.UTF8.GetBytes(bodyWithGlobal), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
            //client.Publish(topic_position_shoulderleftrotation, System.Text.Encoding.UTF8.GetBytes(sholderLeftWithBody), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
            //client.Publish(topic_position_shoulderrightrotation, System.Text.Encoding.UTF8.GetBytes(sholderRightWithBody), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
        }
        
        //Debug.Log("sent");
        
        
    }

    // Update is called once per frame
    void Update()
    {
        if(Time.time-cur_time > 0.02)
        {
            StartCoroutine(Example());
        }
        


    }
}
