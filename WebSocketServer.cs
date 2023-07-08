using WebSocketSharp;
using WebSocketSharp.Server;
using System;
using UnityEngine;

public class MyWebSocketServer : WebSocketBehavior
{
    private Action<float[]> callback;

    public MyWebSocketServer(Action<float[]> callback)
    {
        this.callback = callback;
    }

    // Note: OnMessage should only accept one argument of type MessageEventArgs
    protected override void OnMessage(MessageEventArgs e)
    {
        string data = e.Data;
        Debug.Log("Received data: " + data); // Log the received data
        string[] components = data.Split(' ');
        float[] irData = Array.ConvertAll(components, float.Parse);
        try
        {
            callback?.Invoke(irData);
        }
        catch (Exception ex)
        {
            Debug.LogError("An error occurred: " + ex.Message);
        }
    }

    protected override void OnOpen()
    {
        Debug.Log("someone connected");
    }

    protected override void OnClose(CloseEventArgs e)
    {
        Debug.Log("someone disconnected");
    }
}

