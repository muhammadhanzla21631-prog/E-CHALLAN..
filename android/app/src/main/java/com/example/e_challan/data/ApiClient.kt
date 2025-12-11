package com.example.e_challan.data

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET

data class Camera(
    val id: Int,
    val lat: Double,
    val lng: Double,
    val address: String?
)

interface ApiService {
    @GET("/api/cameras")
    suspend fun getCameras(): List<Camera>
}

object RetrofitClient {
    private const val BASE_URL = "http://10.0.2.2:8000/" // Localhost for Android Emulator

    val apiService: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}
