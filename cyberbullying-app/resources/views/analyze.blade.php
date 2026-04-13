@extends('layouts.app')

@section('content')

<!-- Hero Section -->
<div class="text-center mb-12">
    <div class="inline-flex items-center gap-2 bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs px-4 py-2 rounded-full mb-6">
        <span>🤖</span> Powered by DistilBERT — 86% Accuracy
    </div>
    <h1 class="text-5xl font-bold mb-4">
        <span class="gradient-text">Cyberbullying</span>
        <span class="text-white"> Detector</span>
    </h1>

</div>

<!-- Main Card -->
<div class="max-w-3xl mx-auto">
    <div class="card rounded-2xl p-8 glow">

        <!-- Input -->
        <form method="POST" action="/analyze">
            @csrf
            <label class="block text-sm font-medium text-gray-400 mb-3">
                📝 Enter text to analyze
            </label>
            <textarea
                name="text"
                id="textInput"
                rows="5"
                placeholder="Paste or type any text here to detect cyberbullying content..."
                class="w-full text-white border border-cyan-900/40 rounded-xl p-4 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50 resize-none transition"
                style="background: rgba(0,212,255,0.03);"
            >{{ old('text') }}</textarea>

            <!-- Character Counter -->
            <div class="flex justify-end mt-1">
                <span id="charCount" class="text-xs text-gray-500">0 characters</span>
            </div>

            @error('text')
                <p class="text-red-400 text-sm mt-2 flex items-center gap-1">
                    ⚠️ {{ $message }}
                </p>
            @enderror

            <button type="submit" id="submitBtn" class="btn-primary mt-4 w-full text-white font-semibold py-3.5 rounded-xl text-sm">
                <span id="btnText">🔍 Analyze Text</span>
                <span id="btnSpinner" class="hidden">
                    ⏳ Analyzing...
                </span>
            </button>
        </form>

        <!-- Categories Info -->
        <div class="mt-6 pt-6 border-t border-cyan-900/20">
            <p class="text-xs text-gray-500 mb-3">Detects these categories:</p>
            <div class="flex flex-wrap gap-2">
                <span class="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">✓ Not Bullying</span>
                <span class="text-xs px-2.5 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400">Gender</span>
                <span class="text-xs px-2.5 py-1 rounded-full bg-orange-500/10 border border-orange-500/20 text-orange-400">Religion</span>
                <span class="text-xs px-2.5 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400">Other</span>
                <span class="text-xs px-2.5 py-1 rounded-full bg-red-500/10 border border-red-500/20 text-red-400">Age</span>
                <span class="text-xs px-2.5 py-1 rounded-full bg-pink-500/10 border border-pink-500/20 text-pink-400">Ethnicity</span>
            </div>
        </div>
    </div>

    <!-- Result Card -->
    @if(session('result'))
    @php
        $result = session('result');
        $status = session('status');
    @endphp

    <div class="card rounded-2xl p-8 mt-6 glow">
        <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-bold text-white">📊 Analysis Result</h2>
            <span class="text-xs px-3 py-1 rounded-full
                @if($result['label'] == 'Not Cyberbullying') bg-emerald-500/10 border border-emerald-500/20 text-emerald-400
                @elseif($result['label'] == 'Gender') bg-purple-500/10 border border-purple-500/20 text-purple-400
                @elseif($result['label'] == 'Religion') bg-orange-500/10 border border-orange-500/20 text-orange-400
                @elseif($result['label'] == 'Age') bg-red-500/10 border border-red-500/20 text-red-400
                @elseif($result['label'] == 'Ethnicity') bg-pink-500/10 border border-pink-500/20 text-pink-400
                @else bg-blue-500/10 border border-blue-500/20 text-blue-400
                @endif">
                {{ $result['label'] }}
            </span>
        </div>

        <!-- Confidence -->
        <div class="flex items-center gap-4 mb-6 p-4 rounded-xl" style="background: rgba(0,212,255,0.05);">
            <div class="text-4xl font-bold" style="background: {{ $result['is_bullying'] ? 'linear-gradient(135deg, #ff4444, #ff0000)' : 'linear-gradient(135deg, #00ff88, #00cc44)' }}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{{ $result['confidence'] }}%</div>
            <div>
                <p class="text-white font-medium">{{ $result['label'] }}</p>
                <p class="text-gray-500 text-sm">Confidence Score</p>
            </div>
            <div class="ml-auto text-3xl">
                @if($result['label'] == 'Not Cyberbullying') ✅
                @else ⚠️
                @endif
            </div>
        </div>

        <!-- All Probabilities -->
        <div class="space-y-3">
            <p class="text-xs text-gray-500 font-medium uppercase tracking-wider">All Category Probabilities</p>
            @foreach($result['all_probs'] as $label => $prob)
            <div>
                <div class="flex justify-between text-xs mb-1">
                    <span class="text-gray-400">{{ $label }}</span>
                    <span class="text-gray-300 font-medium">{{ $prob }}%</span>
                </div>
                <div class="w-full rounded-full h-1.5" style="background: rgba(255,255,255,0.05);">
                    <div class="h-1.5 rounded-full" style="width: {{ $prob }}%; background: {{ $label == 'Not Cyberbullying' ? 'linear-gradient(135deg, #00ff88, #00cc44)' : 'linear-gradient(135deg, #ff4444, #ff0000)' }}"></div>
                </div>
            </div>
            @endforeach
        </div>
    </div>
    @endif

</div>

<!-- Scripts -->
<script>
    // Character counter
    const textarea = document.getElementById('textInput');
    const charCount = document.getElementById('charCount');

    textarea.addEventListener('input', function() {
        const count = this.value.length;
        charCount.textContent = count + ' characters';
        charCount.style.color = count > 500 ? '#f87171' : '#6b7280';
    });

    // Update count on page load (for old input)
    charCount.textContent = textarea.value.length + ' characters';

    // Loading spinner
    document.querySelector('form').addEventListener('submit', function() {
        document.getElementById('btnText').classList.add('hidden');
        document.getElementById('btnSpinner').classList.remove('hidden');
        document.getElementById('submitBtn').disabled = true;
        document.getElementById('submitBtn').style.opacity = '0.7';
    });
</script>

@endsection