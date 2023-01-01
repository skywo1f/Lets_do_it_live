using UnityEngine;
using WebSocketSharp;
using WebSocketSharp.Server;
using System;

public class OrientationEvent
{
    public event Action<Vector3> OnOrientationUpdate;
}

public class WS_Client : MonoBehaviour
{
    public static GameObject _cube;
    private Action<Vector3> callback;
    WebSocket ws;
    [SerializeField] float speed = 50.0f;
    private Vector3 _orientation;

    // Start is called before the first frame update
    void Start()
    {

        _cube = GameObject.Find("MyCube");
        if (_cube == null)
        {
            Debug.Log("couldnt find MyCube at first");
        }

        WebSocketServer wssv = new WebSocketServer(8080);
        Action<Vector3> callback = HandleOrientationUpdate;
        MyWebSocketServer wsService = new MyWebSocketServer(callback);
        wssv.AddWebSocketService<MyWebSocketServer>("/MyWebSocket", () => wsService);
        wssv.Start();

    }
    public WS_Client(OrientationEvent orientationEvent)
    {
        callback = HandleOrientationUpdate;
    }
    private void Update()
    {
        _cube.transform.rotation = Quaternion.Euler(_orientation);
    }

    private void HandleOrientationUpdate(Vector3 orientation)
    {
        Debug.Log("tries to rotate mycube");
        Debug.Log(orientation);

            // Update the cube's orientation using the data from the event
                try
          {
            _orientation = orientation;
             Debug.Log("translates the orientation");
         }
         catch (Exception ex)
          {
             Debug.LogError("An error occurred: " + ex.Message);
          }
        

    }

}
public class MyWebSocketServer : WebSocketBehavior
{
    private Action<Vector3> callback;

    public MyWebSocketServer(Action<Vector3> callback)
    {
        this.callback = callback;
    }

    protected override void OnMessage(MessageEventArgs e)
    {

        string data = e.Data;
        string[] components = data.Split(' ');
        Debug.Log("splits components");
        float x = float.Parse(components[0]);
        float y = float.Parse(components[1]);
        float z = float.Parse(components[2]);
        Debug.Log("parses components");
        Vector3 orientation = new Vector3(x, y, z);

//        Vector3 vector = new Vector3((float)x, (float)y, (float)z);
        Debug.Log("puts them in vector3");
        try
        {

            callback?.Invoke(orientation);
            Debug.Log("invokes action");
        }
        catch (Exception ex)
        {
            Debug.LogError("An error occurred: " + ex.Message);
        }

    }
    protected override void OnOpen()
    {
        // Handle client connection here
        Debug.Log("someone connected");
    }
    protected override void OnClose(CloseEventArgs e)
    {
        // Handle client disconnection here
        Debug.Log("someone disconnected");
    }
}
