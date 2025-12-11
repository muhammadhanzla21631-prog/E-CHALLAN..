package com.example.e_challan

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import com.example.e_challan.data.Camera
import com.example.e_challan.data.RetrofitClient
import com.example.e_challan.ui.theme.EChallanTheme
import com.google.android.gms.maps.model.CameraPosition
import com.google.android.gms.maps.model.LatLng
import com.google.maps.android.compose.GoogleMap
import com.google.maps.android.compose.Marker
import com.google.maps.android.compose.MarkerState
import com.google.maps.android.compose.rememberCameraPositionState
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            EChallanTheme {
                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                    MapScreen()
                }
            }
        }
    }
}

@Composable
fun MapScreen() {
    val defaultLocation = LatLng(31.5204, 74.3587) // Lahore, Pakistan (Example)
    val cameraPositionState = rememberCameraPositionState {
        position = CameraPosition.fromLatLngZoom(defaultLocation, 12f)
    }
    
    var cameras by remember { mutableStateOf<List<Camera>>(emptyList()) }
    val scope = rememberCoroutineScope()

    LaunchedEffect(true) {
        scope.launch {
            try {
                cameras = RetrofitClient.apiService.getCameras()
            } catch (e: Exception) {
                Log.e("MapScreen", "Error fetching cameras", e)
            }
        }
    }

    GoogleMap(
        modifier = Modifier.fillMaxSize(),
        cameraPositionState = cameraPositionState
    ) {
        cameras.forEach { camera ->
            Marker(
                state = MarkerState(position = LatLng(camera.lat, camera.lng)),
                title = "Camera ${camera.id}",
                snippet = camera.address ?: "Traffic Camera"
            )
        }
    }
}


