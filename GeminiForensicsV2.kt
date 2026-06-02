package com.gemini.toolkit

import java.io.File

/**
 * Defines the interface for all Forensic Modules within the V2 Framework.
 */
interface ForensicModule {
    val name: String
    fun execute(args: Array<String>)
}

/**
 * The core Orchestrator for the V2 Toolkit.
 */
class GeminiForensicsV2 {
    private val modules = mutableListOf<ForensicModule>()

    fun registerModule(module: ForensicModule) {
        modules.add(module)
    }

    fun run(moduleName: String, args: Array<String>) {
        val module = modules.find { it.name == moduleName }
        if (module != null) {
            module.execute(args)
        } else {
            println("Module '$moduleName' not found.")
        }
    }
}

/**
 * Temporary bridge to maintain existing functionality while migrating.
 */
class LegacyLinguisticModule : ForensicModule {
    override val name = "linguistic-parity"

    override fun execute(args: Array<String>) {
        if (args.size < 2) {
            println("Usage: gemini-v2 linguistic-parity <native_text> <translit_text>")
            return
        }
        val core = V2Core()
        core.analyze(args[0], args[1])
    }
}

/**
 * Module for number sequence analysis.
 */
class SequenceAnalysisModule : ForensicModule {
    override val name = "sequence"

    override fun execute(args: Array<String>) {
        if (args.size < 1) {
            println("Usage: gemini-v2 sequence <start_val> [steps] [lang]")
            return
        }
        val startVal = args[0].toLong()
        val steps = args.getOrNull(1)?.toInt() ?: 10
        val lang = args.getOrNull(2) ?: "en"

        val core = V2Core()
        val sequence = core.generateSequenceNative(startVal, steps, lang)
        
        println("Sequence: ${sequence.joinToString(", ")}")
    }
}

/**
 * Module for image page scanner.
 */
class PageScannerModule : ForensicModule {
    override val name = "scanner"

    override fun execute(args: Array<String>) {
        if (args.size < 2) {
            println("Usage: gemini-v2 scanner <left_img_path> <right_img_path>")
            return
        }
        val core = V2Core()
        val results = core.findPageOverlapNative(args[0], args[1])
        
        println("Scan Results -> Overlap: ${results[0]}, V-Shift: ${results[1]}, Diff: ${results[2]}")
    }
}

class V2Core {
    companion object {
        init {
            val libPath = System.getProperty("user.dir") + "/v2_linguistic_core/target/release/libv2_linguistic_core.so"
            System.load(libPath)
        }
    }

    external fun calculateMetricsNative(native: String, translit: String): FloatArray
    external fun generateSequenceNative(startVal: Long, steps: Int, lang: String): LongArray
    external fun findPageOverlapNative(left: String, right: String): FloatArray

    fun analyze(nativePath: String, translitPath: String) {
        val nFile = File(nativePath)
        val tFile = File(translitPath)

        if (!nFile.exists() || !tFile.exists()) {
            println("[ERROR] Source files not found.")
            return
        }

        val metrics = calculateMetricsNative(nFile.readText(), tFile.readText())
        
        // Metrics mapping:
        // 0: Expansion Ratio
        // 1: Native Entropy, 2: Native Sent Avg
        // 3: Translit Entropy, 4: Translit Sent Avg
        // 5: Parity Ratio, 6: Native Info Load
        
        println("\n=== Gemini Forensics V2 (Rust-Powered) ===")
        println("1. Global Parity")
        println("   - Expansion Ratio:      ${"%.4f".format(metrics[0])}")
        println("   - Parity Ratio Adjustment: ${"%.2f".format(metrics[5])}")
        
        println("\n2. Native Topological Volume")
        println("   - Entropy Density:      ${"%.4f".format(metrics[1])} bits/char")
        println("   - Avg Sentence Chars:   ${"%.1f".format(metrics[2])}")
        println("   - Sentence Info Load:   ${"%.2f".format(metrics[6])} bits")
        
        println("\n3. Translit Topological Volume")
        println("   - Entropy Density:      ${"%.4f".format(metrics[3])} bits/char")
        println("   - Avg Sentence Chars:   ${"%.1f".format(metrics[4])}")
        println("==========================================\n")
    }
}

fun main(args: Array<String>) {
    val orchestrator = GeminiForensicsV2()
    orchestrator.registerModule(LegacyLinguisticModule())
    orchestrator.registerModule(SequenceAnalysisModule())
    orchestrator.registerModule(PageScannerModule())

    if (args.isEmpty()) {
        println("Usage: gemini-v2 <module_name> [args...]")
        return
    }

    orchestrator.run(args[0], args.drop(1).toTypedArray())
}
