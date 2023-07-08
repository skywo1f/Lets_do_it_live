using UnityEngine;
using WebSocketSharp;
using WebSocketSharp.Server;

public class WebSocketServerInitializer : MonoBehaviour
{
    private WebSocketServer webSocketServer;

    void Start()
    {
        webSocketServer = new WebSocketServer(8080);
        webSocketServer.AddWebSocketService<MyWebSocketServer>("/MyWebSocket", () => new MyWebSocketServer(HandleIRDataUpdate));
        webSocketServer.Start();
    }

    private void HandleIRDataUpdate(float[] irData)
    {
        Debug.Log("Received IR data");
        // Here you can use the received irData to update the heatmap or any other game objects.
        // You might want to have a reference to your HeatmapDisplay script and call its UpdateHeatmap method here.
    }

    void OnApplicationQuit()
    {
        if (webSocketServer != null)
        {
            webSocketServer.Stop();
        }
    }
}
