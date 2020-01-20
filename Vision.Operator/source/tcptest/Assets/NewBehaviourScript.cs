using System.Collections;
using System.Collections.Generic;
using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
using System.Linq;

public class NewBehaviourScript : MonoBehaviour
{

    #region private members 	
    private TcpClient socketConnection;
    private Thread clientReceiveThread;
    Texture2D tex;
    int size_x = 1920;// 640
    int size_y = 1080;// 240
    byte[] temp;
    public Material targetMat;

    int imageSize = 0;
    byte[] img;
    byte[] buff;
    byte[] temp_buff;
    int state = 0;
    int trick = 0;
    #endregion
    // Use this for initialization 	
    void Start()
    {

        tex = new Texture2D(size_x, size_y, TextureFormat.RGBA32, false, false);
        tex.filterMode = FilterMode.Point;
        tex.wrapMode = TextureWrapMode.Clamp;

        imageSize = size_x * size_y * 4;
        temp = new byte[imageSize];
        buff = new byte[imageSize * 2];
        temp_buff = new byte[imageSize * 2];

        // init pixels wit bright color
        for (int i = 0; i < imageSize; i += 4)
        {
            temp[i] = 255;
            temp[i + 1] = 0;
            temp[i + 2] = 255;
        }
        img = temp;
        tex.LoadRawTextureData(img);
        tex.Apply(false);
        targetMat.mainTexture = tex;
        ConnectToTcpServer();
    }
    // Update is called once per frame
    string PrintBytes(byte[] byteArray)
    {
        var sb = new StringBuilder("new byte[] { ");
        for (var i = 0; i < byteArray.Length; i++)
        {
            var b = byteArray[i];
            sb.Append(b);
            if (i < byteArray.Length - 1)
            {
                sb.Append(", ");
            }
        }
        sb.Append(" }");
        return sb.ToString();
    }
    void FixedUpdate()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            SendMessage();
        }
        if (trick == 1)
        {
            tex.LoadRawTextureData(img);
            tex.Apply(false);
            GetComponent<Renderer>().material.mainTexture = tex;
            trick = 0;
        }
    }
    /// <summary> 	
    /// Setup socket connection. 	
    /// </summary> 	
    private void ConnectToTcpServer()
    {
        try
        {
            clientReceiveThread = new Thread(new ThreadStart(ListenForData));
            clientReceiveThread.IsBackground = true;
            clientReceiveThread.Start();
        }
        catch (Exception e)
        {
            Debug.Log("On client connect exception " + e);
        }
    }
    /// <summary> 	
    /// Runs in background clientReceiveThread; Listens for incomming data. 	
    /// </summary>    
    //private void updateframe(byte[] img)
    //{

    //    // Create a 16x16 texture with PVRTC RGBA4 format
    //    // and fill it with raw PVRTC bytes.
    //    Texture2D tex = new Texture2D(10, 10, TextureFormat.RGB24, false);
    //    // Raw PVRTC4 data for a 16x16 texture. This format is four bits
    //    // per pixel, so data should be 16*16/2=128 bytes in size.
    //    // Texture that is encoded here is mostly green with some angular
    //    // blue and red lines.
    //    byte[] pvrtcBytes = new byte[]
    //    {
    //        0x30, 0x32, 0x32, 0x32, 0xe7, 0x30, 0xaa, 0x7f, 0x32, 0x32, 0x32, 0x32, 0xf9, 0x40, 0xbc, 0x7f,
    //        0x03, 0x03, 0x03, 0x03, 0xf6, 0x30, 0x02, 0x05, 0x03, 0x03, 0x03, 0x03, 0xf4, 0x30, 0x03, 0x06,
    //        0x32, 0x32, 0x32, 0x32, 0xf7, 0x40, 0xaa, 0x7f, 0x32, 0xf2, 0x02, 0xa8, 0xe7, 0x30, 0xff, 0xff,
    //        0x03, 0x03, 0x03, 0xff, 0xe6, 0x40, 0x00, 0x0f, 0x00, 0xff, 0x00, 0xaa, 0xe9, 0x40, 0x9f, 0xff,
    //        0x5b, 0x03, 0x03, 0x03, 0xca, 0x6a, 0x0f, 0x30, 0x03, 0x03, 0x03, 0xff, 0xca, 0x68, 0x0f, 0x30,
    //        0xaa, 0x94, 0x90, 0x40, 0xba, 0x5b, 0xaf, 0x68, 0x40, 0x00, 0x00, 0xff, 0xca, 0x58, 0x0f, 0x20,
    //        0x00, 0x00, 0x00, 0xff, 0xe6, 0x40, 0x01, 0x2c, 0x00, 0xff, 0x00, 0xaa, 0xdb, 0x41, 0xff, 0xff,
    //        0x00, 0x00, 0x00, 0xff, 0xe8, 0x40, 0x01, 0x1c, 0x00, 0xff, 0x00, 0xaa, 0xbb, 0x40, 0xff, 0xff,
    //    };
    //    // Load data into the texture and upload it to the GPU.

    //    tex.LoadRawTextureData(img);
    //    tex.Apply();
    //    // Assign texture to renderer's material.
    //    GetComponent<Renderer>().material.mainTexture = tex;

    //}

    private void ListenForData()
    {
        try
        {
            socketConnection = new TcpClient("192.168.2.222", 1150);
            Byte[] bytes = new Byte[3147264];
            int startind = -1;
            int endid = -1;
            int lastind = 0;
            while (true)
            {
                // Get a stream object for reading 				
                using (NetworkStream stream = socketConnection.GetStream())
                {
                    int length;
                    // Read incomming stream into byte arrary. 					
                    while ((length = stream.Read(bytes, 0, bytes.Length)) != 0)
                    {
                        var incommingData = new byte[length];
                        //Array.Copy(bytes, 0, incommingData, 0, length);
                        Array.Copy(bytes, 0, buff, state, length);
                        // Convert byte array to string message. 
                        //print( PrintBytes(incommingData));

                        string serverMessage = Encoding.ASCII.GetString(buff);
                        //Debug.Log("server message received as: " + serverMessage);
                        //Debug.Log(length);

                        state += length;
                        Debug.Log(state);
                        if (startind < 0)
                        {
                            if (serverMessage.IndexOf("[HEADER]") != -1)
                            {
                                print("state = 0");
                                startind = serverMessage.IndexOf("[HEADER]");

                                endid = -1;
                            }
                        }
                        else
                        {
                            endid = serverMessage.IndexOf("[HEADER]", startind + 20);
                            if (endid > startind)
                            {
                                Array.Copy(buff, startind + 8, img, 0, endid - startind - 8);
                                Array.Copy(buff, endid, temp_buff, 0, state - endid);
                                buff = Enumerable.Repeat<byte>(0, imageSize * 2).ToArray();
                                Array.Copy(temp_buff, 0, buff, 0, state - endid);
                                state = 0;
                                trick = 1;
                            }
                        }

                    }
                }
            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("Socket exception: " + socketException);
        }
    }
    /// <summary> 	
    /// Send message to server using socket connection. 	
    /// </summary> 	
    private void SendMessage()
    {
        if (socketConnection == null)
        {
            return;
        }
        try
        {
            // Get a stream object for writing. 			
            NetworkStream stream = socketConnection.GetStream();
            if (stream.CanWrite)
            {
                string clientMessage = "READY";
                // Convert string message to byte array.                 
                byte[] clientMessageAsByteArray = Encoding.ASCII.GetBytes(clientMessage);
                // Write byte array to socketConnection stream.                 
                stream.Write(clientMessageAsByteArray, 0, clientMessageAsByteArray.Length);
                Debug.Log("Client sent his message - should be received by server");
            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("Socket exception: " + socketException);
        }
    }

}
