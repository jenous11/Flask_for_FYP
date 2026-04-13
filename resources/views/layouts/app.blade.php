<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberGuard — Cyberbullying Detector</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
    <style>
        body { background: #0a0f1e; }
        .gradient-text { background: linear-gradient(135deg, #00d4ff, #0066ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .card { background: rgba(255,255,255,0.03); backdrop-filter: blur(10px); border: 1px solid rgba(0,212,255,0.15); }
        .btn-primary { background: linear-gradient(135deg, #00d4ff, #0066ff); transition: all 0.3s; }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,212,255,0.3); }
        .nav-link { position: relative; }
        .nav-link::after { content: ''; position: absolute; bottom: -2px; left: 0; width: 0; height: 2px; background: linear-gradient(135deg, #00d4ff, #0066ff); transition: width 0.3s; }
        .nav-link:hover::after { width: 100%; }
        .glow { box-shadow: 0 0 30px rgba(0,212,255,0.1); }
    </style>
</head>
<body class="text-white min-h-screen">

    <!-- Navbar -->
    <nav class="border-b border-cyan-900/30 px-6 py-4 sticky top-0 z-50" style="background: rgba(10,15,30,0.95); backdrop-filter: blur(20px);">
        <div class="max-w-6xl mx-auto flex items-center justify-between">
            <!-- Logo -->
            <a href="/" class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-lg btn-primary flex items-center justify-center text-lg">🛡️</div>
                <div>
                    <span class="text-lg font-bold gradient-text">CyberGuard</span>
                    <p class="text-xs text-gray-500 leading-none">Detection System</p>
                </div>
            </a>

            <!-- Nav Links -->
            <div class="flex items-center gap-8 text-sm">
                <a href="/" class="nav-link text-gray-400 hover:text-cyan-400 transition">Analyze</a>
                <a href="/history" class="nav-link text-gray-400 hover:text-cyan-400 transition">History</a>
                <a href="/dashboard" class="nav-link text-gray-400 hover:text-cyan-400 transition">Dashboard</a>
                <a href="/about" class="nav-link text-gray-400 hover:text-cyan-400 transition">About</a>
            </div>

            <!-- Status Badge -->
            <div class="flex items-center gap-2 text-xs bg-green-500/10 border border-green-500/20 text-green-400 px-3 py-1.5 rounded-full">
                <div class="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"></div>
                API Online
            </div>
        </div>
    </nav>

    <!-- Page Content -->
    <main class="max-w-6xl mx-auto px-6 py-10">
        @yield('content')
    </main>

    <!-- Footer -->
    <footer class="border-t border-cyan-900/20 mt-20 py-8">
        <div class="max-w-6xl mx-auto px-6 flex items-center justify-between text-xs text-gray-600">
            <span>© 2026 CyberGuard — ACHS College · CSIT 7th Semester</span>
            <span>Built by Students · DistilBERT · 86% Accuracy</span>
        </div>
    </footer>

</body>
</html>