using System;
using System.Collections.Concurrent;
using UnityEngine;
using WebSocketSharp.Server;

public class WebSocketInitializer : MonoBehaviour
{
    private WebSocketSharp.Server.WebSocketServer server;
    private ConcurrentQueue<Action> actionsToExecuteOnMainThread = new ConcurrentQueue<Action>();
    public HeatmapDisplay heatmapDisplay;

    void Start()
    {
        // Initialize the WebSocket server.
        server = new WebSocketSharp.Server.WebSocketServer("ws://0.0.0.0:8083");

        // Add the WebSocketService
        server.AddWebSocketService<MyWebSocketServer>("/MyWebSocketServer", () => new MyWebSocketServer((data) =>
        {
            // Queue the action to be executed on the main thread
            actionsToExecuteOnMainThread.Enqueue(() =>
            {
                // This code is executed on the main thread
                heatmapDisplay.UpdateHeatmap(data);
            });
        }));

        // Start the server.
        server.Start();
    }

    void Update()
    {
        // Execute all code enqueued to run on the main thread
        while (actionsToExecuteOnMainThread.TryDequeue(out var action))
        {
            action();
        }
    }

    void OnApplicationQuit()
    {
        // Stop the WebSocket server when the application is closed.
        if (server != null)
        {
            server.Stop();
        }
    }
}
