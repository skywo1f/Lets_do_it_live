using UnityEngine;

public class HeatmapDisplay : MonoBehaviour
{
    public Material heatmapMaterial;
    private Texture2D texture;
    private int width = 24;
    private int height = 32;

    // Variables to store the minimum and maximum values received so far
    private float minValue = float.MaxValue;
    private float maxValue = float.MinValue;

    private void Start()
    {
        // Initialize texture
        texture = new Texture2D(width, height);
        heatmapMaterial.mainTexture = texture;
    }

    public void UpdateHeatmap(float[] irData)
    {
        Debug.Log("Updating heatmap with " + irData.Length + " values.");

        // Loop through the irData and set the pixels of the texture
        for (int i = 0; i < irData.Length; i++)
        {
            int x = i / height;
            int y = i % height;
            float value = irData[i];

            // Update the global min and max values
            minValue = Mathf.Min(minValue, value);
            maxValue = Mathf.Max(maxValue, value);

            // Convert value to color
            Color color = ValueToColor(value);

            // Set the pixel color (flipping x-coordinate)
            texture.SetPixel(width - 1 - x, y, color);
        }

        // Apply the updated pixels to the texture
        texture.Apply();
    }


    Color ValueToColor(float value)
    {
        // Normalizing the value between 0 and 1 using the min and max values
        float normalizedValue = (value - minValue) / (maxValue - minValue);

        // Interpolate between blue and red based on normalizedValue
        return Color.Lerp(Color.blue, Color.red, normalizedValue);
    }
}
