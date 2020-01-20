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
    Vector3 head_offset;
    Vector3 body_offset;
    Vector3 sholder_left_offset;
    Vector3 sholder_right_offset;
    Vector3 hand_left_offset;
    Vector3 hand_right_offset;
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

        head_offset = CalibrateHead.localRotation.eulerAngles;
        body_offset = CalibrateBody.localRotation.eulerAngles;

        sholder_left_offset = CalibrateSholderLeft.localRotation.eulerAngles;
        sholder_right_offset = CalibrateSholderRight.localRotation.eulerAngles;

    }

    void OnGUI()
    {
        if (GUI.Button(new Rect(20, 40, 80, 20), "Set Home"))
        {
            
            Debug.Log("SetHome..");
            temp_body = DeviceBody.localRotation.eulerAngles;
            temp_head = DeviceHead.localRotation.eulerAngles;
            temp_hand_right_rotation = DeviceHandRight.localRotation.eulerAngles;
            temp_hand_left_rotation = DeviceHandLeft.localRotation.eulerAngles;
            temp_sholder_right_rotation = DeviceSholderRight.localRotation.eulerAngles;
            temp_sholder_left_rotation = DeviceSholderLeft.localRotation.eulerAngles;
            temp_hand_right_translation = DeviceHandRight.position;
            temp_hand_left_translation = DeviceHandLeft.position;
            temp_sholder_right_translation = DeviceSholderRight.position;
            temp_sholder_left_translation = DeviceSholderLeft.position;
            Debug.Log("SetHome..Done!!");
            
        }
        
    }
    void calibrate(Transform Device, Transform Calibrate, Vector3 Temp,Vector3 offset,bool mode)
    {
        if (mode)
        {
            Calibrate.eulerAngles = new Vector3(Device.localRotation.eulerAngles.x - Temp.x + offset.x,
                                                Device.localRotation.eulerAngles.y - Temp.y + offset.y,
                                                Device.localRotation.eulerAngles.z - Temp.z + offset.z);
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
        //Debug.Log("-------------");
        Debug.Log(CalibrateBody.localEulerAngles);
        Debug.Log(CalibrateHead.localEulerAngles);
        Debug.Log(CalibrateSholderLeft.localEulerAngles);

        calibrate(DeviceBody, CalibrateBody, temp_body,new Vector3(0,0,0), true);
        calibrate(DeviceHead, CalibrateHead, temp_head, new Vector3(0, 0, 0), true);
        calibrate(DeviceSholderLeft, CalibrateSholderLeft, temp_sholder_left_rotation, new Vector3(0, -90, 0), true);
        //calibrate(DeviceSholderLeft, CalibrateSholderLeft, temp_sholder_left_translation, false);

    }


}
