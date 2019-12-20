using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class q_translation : MonoBehaviour
{

    public Transform DeviceBody;
    public Transform DeviceHead;
    public Transform DeviceSholderLeft;
    public Transform DeviceSholderRight;
    public Transform DeviceHandLeft;
    public Transform DeviceHandRight;

    public Transform CalibrateBody;
    public Transform CalibrateHead;
    public Transform CalibrateSholderLeft;
    public Transform CalibrateSholderRight;
    public Transform CalibrateHandLeft;
    public Transform CalibrateHandRight;

    Vector3 temp_body;
    Vector3 temp_head;
    Vector3 temp_sholder_left_rotation;
    Vector3 temp_sholder_left_translation;
    Vector3 temp_sholder_right_rotation;
    Vector3 temp_sholder_right_translation;
    Vector3 temp_hand_left_rotation;
    Vector3 temp_hand_left_translation;
    Vector3 temp_hand_right_rotation;
    Vector3 temp_hand_right_translation;

    // Start is called before the first frame update
    void Start()
    {
        temp_body = new Vector3(0, 0, 0);
        temp_head = new Vector3(0, 0, 0);
        temp_sholder_left_rotation = new Vector3(0, 0, 0);
        temp_sholder_left_translation = new Vector3(0, 0, 0);
        temp_sholder_right_rotation = new Vector3(0, 0, 0);
        temp_sholder_right_translation = new Vector3(0, 0, 0);
        temp_hand_left_rotation = new Vector3(0, 0, 0);
        temp_hand_left_translation = new Vector3(0, 0, 0);
        temp_hand_right_rotation = new Vector3(0, 0, 0);
        temp_hand_right_translation = new Vector3(0, 0, 0);
    }
    
    void OnGUI()
    {
        if (GUI.Button(new Rect(20, 40, 80, 20), "Set Home"))
        {
            
            Debug.Log("SetHome..");
            temp_body = DeviceBody.eulerAngles;
            temp_head = DeviceHead.eulerAngles;
            temp_hand_right_rotation = DeviceHandRight.eulerAngles;
            temp_hand_left_rotation = DeviceHandLeft.eulerAngles;
            temp_sholder_right_rotation = DeviceSholderRight.eulerAngles;
            temp_sholder_left_rotation = DeviceSholderLeft.eulerAngles;
            temp_hand_right_translation = DeviceHandRight.position;
            temp_hand_left_translation = DeviceHandLeft.position;
            temp_sholder_right_translation = DeviceSholderRight.position;
            temp_sholder_left_translation = DeviceSholderLeft.position;
            Debug.Log("SetHome..Done!!");
            
        }
        
    }
    void calibrate(Transform Device, Transform Calibrate, Vector3 Temp,bool mode)
    {
        if (mode)
        {
            Calibrate.eulerAngles = new Vector3(Device.eulerAngles.x - Temp.x,
                                                Device.eulerAngles.y - Temp.y,
                                                Device.eulerAngles.z - Temp.z);
        }
        else
        {
            Calibrate.position = new Vector3(Device.position.x - Temp.x,
                                                Device.position.y - Temp.y,
                                                Device.position.z - Temp.z);
        }
    }
    // Update is called once per frame
    void Update()
    {
        Debug.Log("-------------");
        Debug.Log(CalibrateBody.localEulerAngles);
        Debug.Log(CalibrateHead.localEulerAngles);
        calibrate(DeviceBody, CalibrateBody, temp_body, true);
        calibrate(DeviceHead, CalibrateHead, temp_head, true);

    }


}
