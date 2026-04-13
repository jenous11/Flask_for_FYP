@extends('layouts.app')

@section('content')

<div class="max-w-3xl mx-auto">

    <div class="mb-10 text-center">
        <h1 class="text-4xl font-bold text-white mb-3">About CyberGuard</h1>
        <p class="text-gray-400">An AI-powered cyberbullying detection system built with DistilBERT</p>
    </div>

    <!-- Model Info -->
    <div class="bg-gray-900 border border-gray-800 rounded-2xl p-8 mb-6">
        <h2 class="text-xl font-bold text-white mb-4">🤖 The Model</h2>
        <p class="text-gray-300 leading-relaxed mb-4">
            CyberGuard uses a fine-tuned <span class="text-blue-400 mono">DistilBERT</span> model —
            a lightweight transformer model trained on over 45,000 social media texts.
            It classifies text into 6 categories with high accuracy.
        </p>
        <div class="grid grid-cols-3 gap-4 mt-6">
            <div class="bg-gray-800 rounded-xl p-4 text-center">
                <p class="text-2xl font-bold text-blue-400">45K+</p>
                <p class="text-gray-400 text-xs mt-1">Training samples</p>
            </div>
            <div class="bg-gray-800 rounded-xl p-4 text-center">
                <p class="text-2xl font-bold text-blue-400">6</p>
                <p class="text-gray-400 text-xs mt-1">Categories</p>
            </div>
            <div class="bg-gray-800 rounded-xl p-4 text-center">
                <p class="text-2xl font-bold text-blue-400">~87%</p>
                <p class="text-gray-400 text-xs mt-1">Accuracy</p>
            </div>
        </div>
    </div>

    <!-- Categories -->
    <div class="bg-gray-900 border border-gray-800 rounded-2xl p-8 mb-6">
        <h2 class="text-xl font-bold text-white mb-4">📊 Detection Categories</h2>
        <div class="space-y-3">
            @php
            $categories = [
                ['label' => 'Not Cyberbullying', 'desc' => 'Safe content with no harmful intent', 'color' => 'emerald'],
                ['label' => 'Gender',            'desc' => 'Harassment based on gender or sexuality', 'color' => 'purple'],
                ['label' => 'Religion',          'desc' => 'Attacks targeting religious beliefs', 'color' => 'orange'],
                ['label' => 'Other Cyberbullying','desc' => 'General harassment, sexual threats, toxic insults', 'color' => 'blue'],
                ['label' => 'Age',               'desc' => 'Discrimination based on age', 'color' => 'red'],
                ['label' => 'Ethnicity',         'desc' => 'Racism and ethnic discrimination', 'color' => 'pink'],
            ];
            @endphp
            @foreach($categories as $cat)
            <div class="flex items-start gap-4 p-3 rounded-xl hover:bg-gray-800/50 transition">
                <span class="px-2.5 py-1 rounded-full text-xs font-semibold mt-0.5 whitespace-nowrap
                    bg-{{ $cat['color'] }}-900/60 text-{{ $cat['color'] }}-300 border border-{{ $cat['color'] }}-700">
                    {{ $cat['label'] }}
                </span>
                <p class="text-gray-400 text-sm">{{ $cat['desc'] }}</p>
            </div>
            @endforeach
        </div>
    </div>

    <!-- Tech Stack -->
    <div class="bg-gray-900 border border-gray-800 rounded-2xl p-8">
        <h2 class="text-xl font-bold text-white mb-4">⚙️ Tech Stack</h2>
        <div class="grid grid-cols-2 gap-4">
            @php
            $stack = [
                ['name' => 'DistilBERT', 'desc' => 'NLP Classification Model', 'icon' => '🧠'],
                ['name' => 'Flask',      'desc' => 'Python API Backend',        'icon' => '🐍'],
                ['name' => 'Laravel',    'desc' => 'PHP Web Framework',         'icon' => '🔴'],
                ['name' => 'Tailwind CSS','desc' => 'Utility-first CSS',        'icon' => '🎨'],
            ];
            @endphp
            @foreach($stack as $tech)
            <div class="bg-gray-800 rounded-xl p-4 flex items-center gap-4">
                <span class="text-2xl">{{ $tech['icon'] }}</span>
                <div>
                    <p class="text-white font-semibold mono text-sm">{{ $tech['name'] }}</p>
                    <p class="text-gray-400 text-xs">{{ $tech['desc'] }}</p>
                </div>
            </div>
            @endforeach
        </div>
    </div>

</div>

@endsection
