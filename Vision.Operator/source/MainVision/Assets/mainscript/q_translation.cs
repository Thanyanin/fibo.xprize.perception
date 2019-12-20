using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class q_translation : MonoBehaviour
{

    public Transform ObjBodyTarget;
    public Transform ObjHeadTarget;
    public Transform ObjHeadPtr;
    public Transform ObjBodyPtr;
    public Transform CalibrateObj;
    public Transform CalibrateObjBody;
    // Start is called before the first frame update
    void Start()
    {

    }
    float temp_r;
    float temp_p;
    float temp_y;
    float temp_h_r;
    float temp_h_p;
    float temp_h_y;
    void OnGUI()
    {
        if (GUI.Button(new Rect(20, 40, 80, 20), "Set Home"))
        {
            Debug.Log("SetHome");
            temp_r = ObjBodyTarget.eulerAngles.x;
            temp_p = ObjBodyTarget.eulerAngles.y;
            temp_y = ObjBodyTarget.eulerAngles.z;
            temp_h_r = ObjHeadTarget.localEulerAngles.x;
            temp_h_p = ObjHeadTarget.localEulerAngles.y;
            temp_h_y = ObjHeadTarget.localEulerAngles.z;
            //CalibrateObj.eulerAngles = new Vector3(ObjBodyPtr.eulerAngles.x- ObjBodyPtr.eulerAngles.x, ObjBodyPtr.eulerAngles.y - ObjBodyPtr.eulerAngles.y, ObjBodyPtr.eulerAngles.y - ObjBodyPtr.eulerAngles.y);
            //ObjBody.transform.rotation = Quaternion.Euler(0,0,0); 
            CalibrateObj.localEulerAngles = new Vector3(0, 0, 0);
            CalibrateObjBody.localPosition = new Vector3(0,0,0);
            CalibrateObjBody.eulerAngles = new Vector3(ObjBodyTarget.eulerAngles.x-temp_r, ObjBodyTarget.eulerAngles.y - temp_p, ObjBodyTarget.eulerAngles.z - temp_y);

            //var init_ang = vrcam.transform.rotation.eulerAngles;
            //var cur_roll = init_ang[2];
            //var cur_pitch = init_ang[0];
            //var cur_yaw = init_ang[1];

            //init_roll = cur_roll;
            //init_pitch = cur_pitch;
            //init_yaw = cur_yaw;

            Debug.Log("SetHome Done");
        }
        
    }
    // Update is called once per frame
    void Update()
    {
        CalibrateObjBody.localEulerAngles = new Vector3(ObjBodyTarget.eulerAngles.x - temp_r, ObjBodyTarget.eulerAngles.y - temp_p, ObjBodyTarget.eulerAngles.z - temp_y);
        //มุมบวกทบเกิน
        CalibrateObj.localEulerAngles = new Vector3(ObjHeadTarget.eulerAngles.x - temp_h_r, ObjHeadTarget.eulerAngles.y - temp_h_p, ObjHeadTarget.eulerAngles.z - temp_h_y);

        //ObjHeadPtr.rotation = ObjHeadTarget.rotation;
        //ObjBodyPtr.rotation = ObjBodyTarget.rotation;
        //Debug.Log("ObjBody=" + ObjBody.rotation);
        //Debug.Log("ObjHeadPtr=" + ObjHeadPtr.localRotation);

    }


}
