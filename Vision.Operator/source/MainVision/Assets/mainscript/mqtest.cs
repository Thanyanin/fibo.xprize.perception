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
    public GameObject body;
    public GameObject shoulderLeft;
    public GameObject shoulderRight;
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
        client = new MqttClient(IPAddress.Parse("192.168.1.102"), 1883, false, null);

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
    string trackWithRef(Quaternion refer, Quaternion track)
    {
        var x_r = refer[0];
        var y_r = refer[1];
        var z_r = refer[2];
        var w_r = refer[3];

        var x_t = track[0];
        var y_t = track[1];
        var z_t = track[2];
        var w_t = track[3];

        var w = (w_r * w_t) - (x_r * x_t) - (y_r * y_t) - (z_r * z_t);
        var x = (w_r * x_t) - (w_t * x_r) - (y_r * z_t) + (z_r * y_t);
        var y = (w_r * y_t) - (w_t * y_r) - (x_r * z_t) + (z_r * x_t);
        var z = (w_r * z_t) - (w_t * z_r) - (x_r * y_t) + (y_r * x_t);

        //if(set_zero == 1)
        //{

        //}

        return w + "," + x + "," + y + "," + z;
    }
    //string trackWithRef(Quaternion refer, Quaternion track)
    //{
    //    var x_r = refer[0];
    //    var y_r = refer[1];
    //    var z_r = refer[2];
    //    var w_r = refer[3];

    //    var x_t = track[0];
    //    var y_t = track[1];
    //    var z_t = track[2];
    //    var w_t = track[3];

    //    var w = (w_r * w_t) - (x_r * x_t) - (y_r * y_t) - (z_r * z_t);
    //    var x = (w_r * x_t) - (w_t * x_r) - (y_r * z_t) + (z_r * y_t);
    //    var y = (w_r * y_t) - (w_t * y_r) - (x_r * z_t) + (z_r * x_t);
    //    var z = (w_r * z_t) - (w_t * z_r) - (x_r * y_t) + (y_r * x_t);

    //    return w + "," + x + "," + y + "," + z;
    //}
    void OnGUI()
    {
        //if (GUI.Button(new Rect(20, 40, 80, 20), "Set Home"))
        //{
        //    Debug.Log("SetHome");




        //    //var init_ang = vrcam.transform.rotation.eulerAngles;
        //    //var cur_roll = init_ang[2];
        //    //var cur_pitch = init_ang[0];
        //    //var cur_yaw = init_ang[1];

        //    //init_roll = cur_roll;
        //    //init_pitch = cur_pitch;
        //    //init_yaw = cur_yaw;
        //    set_zero = 1;
        //    Debug.Log("SetHome Done");
        //}
        if (GUI.Button(new Rect(100, 40, 80, 20), "Send DATA"))
        {
            Debug.Log("Map Ip 192.168.3.201:1883");
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
        var ang = vrcam.transform.rotation.eulerAngles;
        var roll = ang[0];
        var pitch = ang[1];
        var yaw = ang[2];
        var q_vrcam = vrcam.transform.rotation;
        var q_body = body.transform.rotation;
        var q_shoulderLeft = shoulderLeft.transform.rotation;
        var q_shoulderRight = shoulderRight.transform.rotation;

        var bodyWithGlobal = q_body[3] + "," + q_body[0] + "," + q_body[1] + "," + q_body[2];
        var headWithBody = trackWithRef(q_body, q_vrcam);
        var sholderLeftWithBody = trackWithRef(q_body, q_shoulderLeft);
        var sholderRightWithBody = trackWithRef(q_body, q_shoulderRight);
        var headrotaion = Head.transform.localRotation;
        string s_headrotation = headrotaion[0] + "," + headrotaion[1] + "," + headrotaion[2] + "," + headrotaion[3];
        string s_rpy = headrotaion[0] + "," + headrotaion[1] + "," + headrotaion[2] + "," + headrotaion[3];
        //Debug.Log(vrcam.transform.position);
        var topic_position_roll = "/operator/roll";
        var topic_position_pitch = "/operator/pitch";
        var topic_position_yaw = "/operator/yaw";
        var topic_position_headrotation = "/operator/headrotation";
        var topic_position_bodyrotation = "/operator/bodyrotation";
        var topic_position_shoulderleftrotation = "/operator/shoulderleftrotation";
        var topic_position_shoulderrightrotation = "/operator/shoulderrightrotation";


        //Debug.Log(roll);
        //client.Publish(topic_position_roll, System.Text.Encoding.UTF8.GetBytes(roll), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
        //client.Publish(topic_position_pitch, System.Text.Encoding.UTF8.GetBytes(pitch), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
        //client.Publish(topic_position_yaw, System.Text.Encoding.UTF8.GetBytes(yaw), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
        if (state_start == 1)
        {
            client.Publish(topic_position_headrotation, System.Text.Encoding.UTF8.GetBytes(s_headrotation), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
            Debug.Log(headrotaion.eulerAngles);
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
