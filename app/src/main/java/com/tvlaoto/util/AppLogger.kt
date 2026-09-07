package com.tvlaoto.util

import android.content.Context
import android.os.Build
import java.io.File
import java.io.FileOutputStream
import java.io.PrintWriter
import java.io.StringWriter
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * File-based logger that writes debug logs to app's internal data directory.
 * Log file: /data/data/com.tvlaoto/files/logs/app_log.txt
 *
 * Also logs to Android logcat via android.util.Log for development.
 */
object AppLogger {

    private const val TAG = "AFlix"
    private const val LOG_DIR = "logs"
    private const val LOG_FILE = "app_log.txt"
    private const val MAX_LOG_SIZE = 2 * 1024 * 1024L // 2MB max, rotate after

    private var logFile: File? = null
    private val dateFormat = SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS", Locale.US)

    /**
     * Initialize logger. Call from Application.onCreate()
     */
    fun init(context: Context) {
        try {
            // Use external files dir — accessible without root via:
            // adb pull /sdcard/Android/data/com.tvlaoto/files/logs/app_log.txt
            val logDir = File(
                context.getExternalFilesDir(null) ?: context.filesDir,
                LOG_DIR
            )
            if (!logDir.exists()) logDir.mkdirs()
            logFile = File(logDir, LOG_FILE)

            // Rotate if too large
            logFile?.let {
                if (it.exists() && it.length() > MAX_LOG_SIZE) {
                    val backup = File(logDir, "app_log_old.txt")
                    backup.delete()
                    it.renameTo(backup)
                    logFile = File(logDir, LOG_FILE)
                }
            }

            // Write session header
            val header = buildString {
                appendLine("=".repeat(60))
                appendLine("=== AFlix TV Session Start ===")
                appendLine("=== ${dateFormat.format(Date())} ===")
                appendLine("=== Device: ${Build.MANUFACTURER} ${Build.MODEL} ===")
                appendLine("=== Android: ${Build.VERSION.RELEASE} (SDK ${Build.VERSION.SDK_INT}) ===")
                appendLine("=== ABI: ${Build.SUPPORTED_ABIS.joinToString()} ===")
                appendLine("=== RAM: ${Runtime.getRuntime().maxMemory() / 1024 / 1024}MB max ===")
                appendLine("=".repeat(60))
            }
            appendToFile(header)

            // Set up uncaught exception handler
            val defaultHandler = Thread.getDefaultUncaughtExceptionHandler()
            Thread.setDefaultUncaughtExceptionHandler { thread, throwable ->
                e("CRASH", "Uncaught exception in thread ${thread.name}", throwable)
                defaultHandler?.uncaughtException(thread, throwable)
            }

            i("AppLogger", "Logger initialized: ${logFile?.absolutePath}")
        } catch (e: Exception) {
            android.util.Log.e(TAG, "Failed to init logger", e)
        }
    }

    fun d(tag: String, message: String) {
        log("D", tag, message)
        android.util.Log.d(TAG, "[$tag] $message")
    }

    fun i(tag: String, message: String) {
        log("I", tag, message)
        android.util.Log.i(TAG, "[$tag] $message")
    }

    fun w(tag: String, message: String) {
        log("W", tag, message)
        android.util.Log.w(TAG, "[$tag] $message")
    }

    fun e(tag: String, message: String, throwable: Throwable? = null) {
        val fullMsg = if (throwable != null) {
            val sw = StringWriter()
            throwable.printStackTrace(PrintWriter(sw))
            "$message\n${sw}"
        } else {
            message
        }
        log("E", tag, fullMsg)
        android.util.Log.e(TAG, "[$tag] $message", throwable)
    }

    private fun log(level: String, tag: String, message: String) {
        try {
            val timestamp = dateFormat.format(Date())
            val line = "[$timestamp] $level/$tag: $message\n"
            appendToFile(line)
        } catch (_: Exception) {
            // Silent fail — don't crash app for logging
        }
    }

    private fun appendToFile(text: String) {
        try {
            logFile?.let { file ->
                FileOutputStream(file, true).use { fos ->
                    fos.write(text.toByteArray(Charsets.UTF_8))
                    fos.flush()
                }
            }
        } catch (_: Exception) {
            // Silent fail
        }
    }

    /**
     * Get the log file path for display/sharing
     */
    fun getLogFilePath(): String {
        return logFile?.absolutePath ?: "N/A"
    }

    /**
     * Get last N lines of log for in-app viewing
     */
    fun getRecentLogs(lines: Int = 50): String {
        return try {
            logFile?.let { file ->
                if (!file.exists()) return "No logs yet"
                val allLines = file.readLines()
                allLines.takeLast(lines).joinToString("\n")
            } ?: "Logger not initialized"
        } catch (e: Exception) {
            "Error reading logs: ${e.message}"
        }
    }

    /**
     * Clear all logs
     */
    fun clearLogs() {
        try {
            logFile?.let {
                it.writeText("")
                i("AppLogger", "Logs cleared")
            }
        } catch (_: Exception) {}
    }
}

