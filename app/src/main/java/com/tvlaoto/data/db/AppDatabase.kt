package com.tvlaoto.data.db

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Database
import androidx.room.RoomDatabase

@Entity(tableName = "app_state")
data class AppState(
    @PrimaryKey val id: Int = 1,
    val lastFilterTab: String
)

@Dao
interface AppStateDao {
    @Query("SELECT * FROM app_state WHERE id = 1")
    suspend fun getAppState(): AppState?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun saveAppState(state: AppState)
}

@Database(entities = [AppState::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun appStateDao(): AppStateDao
}
